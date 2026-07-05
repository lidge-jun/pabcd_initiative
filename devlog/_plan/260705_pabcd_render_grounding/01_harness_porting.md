# Harness Porting Guide: C-RENDER-GROUNDING-01

| Field | Value |
|-------|-------|
| Date | 2026-07-05 |
| Status | Proposed |
| Sibling | [00_render_grounding_c_phase.md](./00_render_grounding_c_phase.md) (rule text, scope guard, integration points) |
| Provenance | [fivetaku/fablize](https://github.com/fivetaku/fablize) (MIT); hooks/gate_post_tool.py + hooks/gate_stop.py + packs/verification-grounding-pack.txt |

---

## 1. Layer Taxonomy

| Layer | Enforces | Cannot | cli-jaw | codexclaw | jawcode | fablize (CC plugin) |
|-------|----------|--------|---------|-----------|---------|---------------------|
| **L1** Prompt/skill text | Agent self-applies rule by reading it | Nothing deterministic; silent skip is invisible | Yes (SKILL.md + STATE_PROMPTS + builder.ts) | Yes (PHASE_DIRECTIVES.C + SKILL.md) | Yes (orchestrate-c.md + goal SKILL.md) | Yes (verification-grounding-pack.txt) |
| **L2** Deterministic hooks | Observed facts from tool results; can block or record | Cannot force agent to initiate an action; cannot verify semantic correctness | Partial (pipeline.ts post-response, friction.ts error ledger -- no tool-call observation) | Full (PostToolUse/Stop/PreToolUse/SessionStart/UserPromptSubmit/PostCompact/SubagentStop) | Limited (UserPromptSubmit + Stop only; no PostToolUse) | Full (PostToolUse gate_post_tool.py, Stop gate_stop.py, UserPromptSubmit router.sh) |
| **L3** FSM/state gates | Transition refusal without structural evidence | Form-only: cannot verify evidence is truthful | Yes (attestation.ts checkAttestationGate; C->D requires non-empty checkOutput + did + exitCode:0) | Yes (attest.ts validateAttest; GATED_TRANSITIONS covers P>A,A>B,B>C,C>D) | Yes (orchestrate-state.ts canTransitionPabcd; BUT C->D returns {ok:true} unconditionally today) | No (no PABCD FSM in plain Claude Code) |
| **L4** Independent verifiers | Adversarial re-check; builder cannot self-attest | Token cost; verifier itself is prompt-bound | Yes (dispatch workers + worker-monitor + batch verdicts) | Yes (spawn_agent/SubagentStop evidence gate) | Yes (actor-registry: 7 role agents, restricted-role-agent-bash enforcement) | No native dispatch surface |

**Key insight**: fablize operates at L2+L1. The sibling doc proposes L1-only (section 5: "No hook/enforcement layer"). This guide maps WHERE L2+ attaches when the initiative closes that gap.

**Shared residual across all harnesses:** Whether the work-phase produced a render artifact is a semantic judgment ("Could this look wrong in a way that only shows when it runs?"). No FSM can evaluate this; trigger classification remains L1 honor-system everywhere. The gate can over-fire (require render evidence for ALL C->D, ~1/3 false-positive per fablize measurement) or trust the agent to self-classify (under-fire). The sibling doc's artifact-type+change trigger is the current mitigation.

---

## 2. Per-Harness Porting Spec

### 2.1 cli-jaw (server-orchestrated PABCD)

**Evidence paths:** `src/orchestrator/state-machine.ts` (STATE_PROMPTS, VALID_TRANSITIONS, canTransition), `src/orchestrator/attestation.ts` (checkAttestationGate, form-only C->D), `src/orchestrator/pipeline.ts` (post-response processing), `src/orchestrator/gateway.ts` (UserPromptSubmit router), `src/orchestrator/friction.ts` (error-pattern ledger), `src/prompt/builder.ts` (system prompt injection), `src/prompt/context-hooks.ts` (runtime data injection).

**Attachment points:**
1. **L1 (three surfaces):** (a) Insert rule into `skills_ref/dev-pabcd/SKILL.md` section 3 C after item 4. (b) Add "Stage 1.5: Render Grounding" to STATE_PROMPTS['C'] in `src/orchestrator/state-machine.ts` (lines 580-622) between Stage 1 Mechanical and Stage 2 Scrutiny -- this is what the agent reads on entering C. (c) Update `src/prompt/builder.ts` compact PABCD summary (lines 564-571) to mention render grounding exists.
2. **L3 (low-effort):** Extend `checkAttestationGate` in `src/orchestrator/attestation.ts` to warn (not hard-reject) when the `did` field lacks render-observation keywords AND the session touched HTML/SVG/CSS files. Form-only heuristic, but raises the bar above pure L1.
3. **L2 (future):** Add tool-call scanning in `src/orchestrator/pipeline.ts` post-response processing for render commands (playwright, screenshot, chrome --headless, pdftoppm). Record in a ledger; feed into the L3 gate. Closes the fabrication gap.
4. **L4 (optional):** Dispatch a read-only worker to render and screenshot the artifact independently. Infrastructure exists (`src/orchestrator/distribute.ts`); no C-phase worker pattern exists yet.

**Adaptation:** The agent-neutral copy CANNOT reference L3 gate fields (renderObserved, checkOutput pattern); instead: "your C->D attestation `did` must reference the render observation; if your runtime gates attestation content, include evidence in the gate-required field." cli-jaw's STATE_PROMPTS string has no agent-neutral equivalent, so the SKILL.md rule text must be self-contained there. The --force emergency hatch (`routes/orchestrate.ts` line 964) bypasses all gates including any future render gate -- accepted residual.

**Degradation:** L2 observation ledger is unavailable (server has no local hook runner). Degrades to L3 form-only attestation. The gate cannot verify the agent actually rendered vs. fabricated a description. Accepted per threat model ("laziness, not malice"). Additional residuals: (1) boss-token stripping (agent poses as human, gets free pass) -- accepted; closing it would break legitimate human free pass. (2) --force emergency hatch bypasses all gates -- accepted per SKILL.md threat model.

---

### 2.2 codexclaw (Codex-native hooks + file-state FSM)

**Evidence paths:** `plugins/codexclaw/components/pabcd-state/src/hook.ts` (PHASE_DIRECTIVES.C, handleStop, PostToolUsePayload), `plugins/codexclaw/components/pabcd-state/src/fsm.ts` (VALID_TRANSITIONS, canEnter), `plugins/codexclaw/components/pabcd-state/src/attest.ts` (validateAttest, Attestation interface, GATED_TRANSITIONS), `plugins/codexclaw/components/pabcd-state/src/state.ts` (Flags), `plugins/codexclaw/components/pabcd-state/src/subagent-evidence.ts` (SubagentStop evidence gate), `plugins/codexclaw/.codex-plugin/plugin.json` (17 hook registrations across 7 events).

**Attachment points:**
1. **L1:** Add rule to `skills/pabcd/SKILL.md` C-phase section AND to PHASE_DIRECTIVES.C in `components/pabcd-state/src/hook.ts` (lines 176-184) -- the injected directive every C-phase turn receives.
2. **L2 (primary, fablize-analogous):** New PostToolUse hook JSON (`hooks/post-tool-use-tracking-render-observations.json`, matcher `^(view_image|browser:control-in-app-browser|chrome:control-chrome|computer-use:computer-use)$`). Records render-observation events to session state. Confirms tool was called but cannot parse truncated tool_response (hook.ts line 698 documents this Codex-rs limitation).
3. **L2 (Stop gate):** Extend `handleStop` in hook.ts (lines 628-665): when phase===C AND edit-shape ledger shows render-artifact files modified AND render-observation ledger is empty, append advisory block reason. Direct analog of fablize's gate_stop.py.
4. **L3:** Extend `Attestation` interface in `attest.ts` with optional `renderEvidence` field, or add `renderObserved` flag to `Flags` in `state.ts` checked by `canEnter('D')`. Strongest gate but most code change.
5. **L4:** Define `agents/visual-verifier.toml` combining reviewer's adversarial stance with browser-use capability. SubagentStop evidence gate (`subagent-evidence.ts`) already enforces EVIDENCE_RECORDED file before completion.

**Adaptation:** Tool names differ from Claude Code: reference `view_image`, `browser:control-in-app-browser`, `chrome:control-chrome`, `computer-use:computer-use`. Hook output uses JSON envelopes (`{hookSpecificOutput}` for injection, `{decision:"block"}` for Stop). PostToolUse carries only truncated tool_response -- hook can confirm tool invocation but not observation quality. No file-write hook event exists; extend edit-shape PostToolUse hook (`matcher ^apply_patch$`) to detect render-artifact extensions.

**Degradation:** Cannot verify observation was meaningful (truncated tool_response is a fundamental Codex-rs limitation -- no structured tool result schema with success/error/content fields). L2 confirms "tool was called" not "output was read and evaluated." The L4 verifier faces the same truncation constraint. No file-write hook event exists, so detecting that an HTML/SVG file was created requires extending the existing edit-shape PostToolUse hook. Over-gating prevention: gate on artifact-type+change (sibling doc section 3), not task depth (fablize's ~1/3 false-positive rate).

---

### 2.3 jawcode (native orchestrate runtime + role agents)

**Evidence paths:** `packages/coding-agent/src/prompts/jaw/orchestrate-c.md` (3-stage verification prompt), `packages/coding-agent/src/jwc-runtime/orchestrate-state.ts` (canTransitionPabcd -- C->D unconditionally ok at line 158), `packages/coding-agent/src/jwc-runtime/orchestrate-runtime.ts` (phase entry, nextCtxFor), `packages/coding-agent/src/jwc-runtime/goal-engine.ts` (quality-gate validator: validateSurfaceArtifactCompatibility, requireLiveSurfaceProof), `packages/coding-agent/src/jwc-runtime/actor-registry.ts` (role agents per stage), `packages/coding-agent/src/hooks/native-skill-hook.ts` (UserPromptSubmit + Stop only), `packages/coding-agent/src/defaults/jwc/skills/browse/SKILL.md` (headless Chromium).

**Attachment points:**
1. **L1 (primary):** Extend `packages/coding-agent/src/prompts/jaw/orchestrate-c.md` -- add render grounding as conditional Stage 1.5 or Stage 4 before the auto-advance instruction ("all green -> run jwc orchestrate d yourself"). Cross-reference in goal SKILL.md mandatory-completion-gate section (items 6-8 already require browser+screenshot for GUI/web surfaces -- note that C-phase now requires it too, not just Goal completion).
2. **L3 (strongest, native to jawcode's architecture):** Add `render_grounding_status: 'pending'|'observed'|'not_applicable'` field to `PabcdCtx` in `orchestrate-state.ts`. Gate C->D on it (currently line 158 returns `{ok:true}` unconditionally). Add verdict subcommand `orchestrate verdict --render-observed` or `--render-not-applicable` in `orchestrate-runtime.ts`. This follows the existing pattern: `p_review_passed` gates P->A, `audit_status` gates A->B, `verification_status` gates B->C.
3. **L1:** Update pabcd-stage-header.ts NEXT_HINTS for stage C (line 33) with render-grounding reminder when context indicates render artifacts.
4. **L4:** Extend `c:mechanical-check-reviewer` actor lane to include render verification; the executor.md `<goal_red_team_mode>` already models the pattern ("browser automation plus screenshot or image verdict").

**Adaptation:** jawcode lacks plugin PostToolUse hooks entirely (hook surface is UserPromptSubmit + Stop only, compiled into the runtime). Fablize's observation-ledger pattern requires adding a new hook event to `packages/agent/src/agent-loop.ts` -- a significant runtime change. Instead, leverage jawcode's strength: the deterministic FSM gate. The L3 gate is architecturally native and follows the existing gating pattern across all forward edges. The browse SKILL.md documents headless Chromium screenshot capabilities; the C prompt references it as execution mechanism.

**Degradation:** Without PostToolUse, the harness cannot verify the agent actually read a screenshot back. The L3 gate catches "model tried to skip verdict recording" (hard stop) but observation quality remains L1-trust. Trigger detection (whether the diff includes render-relevant files) must be done by the model or a future deterministic classifier in orchestrate-runtime C-phase entry -- not available today.

---

### 2.4 Plain Claude Code + fablize-style plugin (remote reference)

**Reference paths (github.com/fivetaku/fablize):**
- `hooks/router.sh` -- UserPromptSubmit keyword routing (classifies task depth, sets grounding flags)
- `hooks/gate_post_tool.py` + `scripts/gate/verify_state.py` -- PostToolUse observation ledger (records tool results, not agent claims)
- `hooks/gate_stop.py` -- blocks Stop when deep+changed+unverified
- `packs/verification-grounding-pack.txt` -- L1 prompt pack

**This IS the reference implementation.** Fablize operates at L2 (observation ledger) + L1 (pack injection). For projects using fablize: no change needed. For projects wanting PABCD render grounding without fablize: extract the observation-ledger pattern into standalone `.claude/hooks.json` PostToolUse + Stop entries.

**Degradation:** No PABCD FSM (no L3). The Stop gate fires on all stops, not only C->D, using task-depth classification as proxy -- producing the measured ~1/3 false-positive rate. The sibling doc's artifact-type+change trigger mitigates this when ported.

---

## 3. Port Status per Copy

| Copy | Location | L1 | L2 | L3 | Status |
|------|----------|----|----|----|----|
| Initiative agent-neutral | `pabcd_initiative/skills/dev-pabcd/SKILL.md` | DONE | N/A | N/A | **DONE 2026-07-05** (WP1; + instance copy + dev-testing rows) |
| cli-jaw skills_ref | `~/.cli-jaw/skills_ref/dev-pabcd/SKILL.md` + repo submodule | DONE | N/A (no local hooks) | DONE (attest advisory, soft) | **DONE 2026-07-05** (WP1+WP2, uncommitted in repo) |
| cli-jaw STATE_PROMPTS | `cli-jaw/src/orchestrator/state-machine.ts` | DONE (Stage 1.5) | -- | -- | **DONE 2026-07-05** (WP2, uncommitted) |
| codexclaw cxc-pabcd | `codexclaw/plugins/codexclaw/skills/pabcd/SKILL.md` | DONE (+PHASE_DIRECTIVES.C) | DONE (ledger + Stop advisory) | Deferred (attest field not needed for warn-only) | **DONE 2026-07-05** (WP3; absorbed into `4ef5ddf` + boss routing fix, see 20_wp2-4 doc) |
| codexclaw Stop hook | `codexclaw/.../stop-checking-pabcd-continuation.json` → handleStop | -- | DONE (advisory, never block) | -- | **DONE 2026-07-05** |
| jawcode orchestrate-c | `jawcode/.../prompts/jaw/orchestrate-c.md` | DONE (Stage 3) | N/A (no plugin hooks) | DONE (status field, warn-only ok:true) | **DONE 2026-07-05** (WP4, uncommitted) |
| Plain Claude Code | `.claude/` or project CLAUDE.md | -- | Fablize covers it | N/A | NO CHANGE NEEDED |

Execution record + attestations: `10_wp1_skill_text_port.md`, `20_wp2-4_three_repo_port.md`.

---

## 4. Principle Delta Worth Porting (not just wording)

1. **Well-formed != correct for render artifacts.** Static parse (tsc, lint) confirms the file is valid syntax; it does NOT confirm the artifact looks or behaves correctly. The run/observe/fix loop closes this modality gap.
2. **Observation is reading, not producing.** A screenshot taken but never read back into context is not observation. The agent must consume the output, not just generate it.
3. **Gate on what happened, not how the task was classified.** Fablize measured ~1/3 false-positive nags when firing on task depth alone. Trigger on artifact-type + change instead.

---

## 5. Generalized Porting Recipe

For any future discipline adoption (not just render grounding):

1. **Classify by minimum enforcing layer.** L1 if honor-system suffices. L2 if observed facts required. L3 if transition gating required. L4 if adversarial independence required. C-RENDER-GROUNDING-01: L1 minimum, L2 ideal, L3 compatible.
2. **Write agent-neutral rule in initiative copy first.** `pabcd_initiative/skills/dev-pabcd/SKILL.md` uses generic `orchestrate <phase>` with the Runtime adapter block. No harness-specific commands or paths.
3. **Adapt per harness idiom.** Map to native surfaces (hooks, FSM gates, stage prompts, dispatch). Use each harness's vocabulary. Model new hooks on existing hook patterns in that harness.
4. **Degrade explicitly.** When a harness lacks the minimum layer: document the degradation, drop to next-lower available layer, never fabricate enforcement. A rule claiming L2 blocking that is actually L1 misleads the operator.
5. **Verify with each fork's own gates; local commits only.** Run native verification (codexclaw: `bun test`; jawcode: `bun run check`; cli-jaw: server tests). Never push a port to a fork's remote without maintainer request. "Ports are adapted, never blind-copied" (README.md line 24).

---

## 6. Non-Goals and Open Questions

**Non-goals:** Unifying hook APIs across harnesses. Automated cross-harness testing. Shipping L2 enforcement immediately (sibling doc section 5 defers it). Replacing fablize (it remains the L2 reference for plain Claude Code).

**Open questions — RESOLVED (user interview, 2026-07-05):**
1. **codexclaw ledger location**: separate `.codexclaw/render-observations.jsonl` —
   avoids bloating the session-state read on every hook invocation. (Agent decision,
   recorded; technical detail, not user-intent.)
2. **jawcode L1 vs L3**: BOTH ship in the first pass — `render_grounding_status` on
   PabcdCtx plus the verdict subcommand — but in **warning mode**: an unrecorded
   status at C->D emits a warning reason while still returning `{ok:true}`. Never a
   refusal in this pass.
3. **Extension set**: starting set `.html`, `.svg`, `.css` (layout-defining), canvas/
   animation/chart JS, `.jsx`/`.tsx` layout components; per-project configurable.
   (Agent decision, recorded.)
4. **codexclaw Stop trigger**: artifact-type+change, aligned with the sibling doc
   section 3 decision. Depth-only classification is rejected — fablize's own
   measurement (~1/3 FP) discredits it. (Repo-resolved; asking again would have
   contradicted an already-recorded decision.)
5. **cli-jaw gate mode**: soft warning. Applies uniformly: ALL enforcement in this
   pass is soft-warning across all three harnesses (user decision).

**Enforcement deployment decision (same interview):** all three harnesses receive
their enforcement layer simultaneously in this pass — cli-jaw attest-warning,
codexclaw L2 ledger + Stop advisory, jawcode L3 status field — all in soft-warning
mode, alongside L1 rule text everywhere.

**Recorded deviations / accepted tradeoffs:**
- *Deviation from fablize*: fablize blocks with a 2-block cap; we ship warn-only.
  Deliberate — the block threat model (laziness) is partially covered by PABCD's
  existing attestation ceremony; warnings avoid deadlock risk entirely.
- *Accepted tradeoff vs measure-then-adopt*: simultaneous 3-harness deployment trades
  false-positive cause isolation for speed. Mitigation: each harness's warning events
  are observable in its own logs/ledger, so per-harness FP rates remain measurable
  post-deploy; revisit gate hardening only after that data exists. A hard reject risks blocking legitimate transitions where the agent correctly judged the artifact did not need render observation.

---

## 7. Per-Harness Adoption Checklist

### Initiative copy (agent-neutral)
- [x] Finalize rule text after open-question resolution
- [x] Insert C-RENDER-GROUNDING-01 into `pabcd_initiative/skills/dev-pabcd/SKILL.md` section 3 C

### cli-jaw
- [x] Insert rule text into `skills_ref/dev-pabcd/SKILL.md` section 3 C
- [x] Add "Stage 1.5: Render Grounding" to STATE_PROMPTS['C'] in `state-machine.ts`
- [x] Update builder.ts compact PABCD summary to mention render grounding
- [x] Document render observation as valid `checkOutput` evidence
- [x] Extend `checkAttestationGate` with the render-observation soft warning (warn, never reject)

### codexclaw
- [x] Insert rule text into `skills/pabcd/SKILL.md` C-phase section
- [x] Add C-RENDER-GROUNDING-01 to PHASE_DIRECTIVES.C in `hook.ts`
- [x] Implement PostToolUse render-observation hook (`post-tool-use-tracking-render-observations.json`)
- [x] Extend Stop hook to check render ledger when render artifacts in diff
- [x] Add tests in `components/pabcd-state/test/` for observation tracking

### jawcode
- [x] Extend `orchestrate-c.md` with render-grounding sub-gate
- [x] Add `render_grounding_status` field to PabcdCtx in `orchestrate-state.ts` (decided 2026-07-05: ships in warning mode — unrecorded status warns at C->D but never refuses)
- [x] Add `orchestrate verdict --render-observed` / `--render-not-applicable` subcommand in `orchestrate-runtime.ts`

### Plain Claude Code (fablize-style)
- [x] No change needed -- fablize already covers this; document compatibility
