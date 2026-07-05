# Render-Artifact Verification Grounding for PABCD C Phase

| Field | Value |
|-------|-------|
| Date | 2026-07-05 |
| Status | Proposed |
| Provenance | [fivetaku/fablize](https://github.com/fivetaku/fablize) (MIT), pack: [`packs/verification-grounding-pack.txt`](https://github.com/fivetaku/fablize/blob/main/packs/verification-grounding-pack.txt) |
| Transfer evidence | Fable-vs-Opus controlled A/B comparison graded this procedure as transferable/verified; adoption-candidate #3 from the fablize review |

---

## 1. Problem Statement

The PABCD C phase (dev-pabcd SKILL.md section 3, "C -- Check") currently gates on:

1. File consistency
2. `npx tsc --noEmit` (TypeScript projects)
3. Structure-doc updates
4. Completion summary

These gates verify **well-formedness** (syntax, types, structure) but not
**behavioral correctness** of render artifacts. An HTML page, SVG chart, game UI,
or animation can pass tsc and all static checks while being visually broken at
runtime: overlapping elements, blank canvas, console errors swallowed by the build,
CSS that renders nothing in a real viewport.

The fablize pack articulates the core distinction: *"A static parse confirms the
file is well-formed -- it does NOT confirm the artifact looks or behaves correctly.
Well-formed and correct are different claims."*

Today, C→D attestation requires `checkOutput` (a pasted tsc/test tail) and
`exitCode:0`, but nothing proves the artifact was actually **rendered and
observed**. A developer who writes a chart component, sees tsc pass, and ships
without ever opening the page is exhibiting the same gap this rule closes.

---

## 2. Proposal: Rule Text (insert-ready)

The following rule is designed for insertion into dev-pabcd/SKILL.md section 3
"C -- Check", after the existing four-step checklist and before the `bgtask`
paragraph about long external gates.

```markdown
**DEFAULT (C-RENDER-GROUNDING-01):** When the work-phase produces an artifact whose
correctness can only be confirmed by running or rendering it (HTML page, SVG, game,
UI, chart, animation, script with observable visual/interactive output), C phase MUST
include a render-grounding loop before C->D attestation:

1. **RUN** the artifact in its natural execution environment. Web artifacts: headless
   browser screenshot (Playwright, Chrome `--headless --screenshot`), or serve and
   navigate. SVG: render to PNG. Scripts: execute and capture stdout/stderr.
   Animations/games: drive far enough that motion/state actually starts.
2. **OBSERVE** the output. Read the screenshot back (a produced-but-unread screenshot
   is not observation). Check the console for runtime errors. Confirm layout,
   visibility, and behavior match intent.
3. **FIX** any defect the observation reveals, then re-run and re-observe.

Trigger condition: "Could this artifact look wrong or behave wrong in a way that
only shows when it runs?" If yes, the grounding loop applies.

Stop condition: one clean observation of the rendered output is enough. Re-render
only after a change (each defect gets one fix and one re-check). Do not accumulate
redundant observations of unchanged state -- the goal is "I saw it work," not "I
checked it N times."

Defaults (HEURISTIC -- deviate with a stated reason): web screenshots at 1280x720;
stateful artifacts (games, wizards) are driven until the first interactive state
change is observed. Evidence depth scales with work class: C2-C3 record the
observation as attestation narrative; C4 (STRICT) additionally persists the
screenshot file to the devlog.

The observation screenshot/output becomes valid `checkOutput` evidence in the C->D
attestation. When this rule applies, the attestation `did` field must reference the
render observation (e.g. "screenshot confirmed layout renders correctly at 1280x720,
no console errors").

This rule does NOT replace test/tsc gates; it supplements them for the render
modality. Pure logic, configuration, and prose artifacts that have their own test
suite are excluded -- for those, the existing spec-satisfaction gate suffices.
```

**Rule ID:** `DEFAULT, C-RENDER-GROUNDING-01`

---

## 3. Scope Guard

### Trigger by work class

| Class | Render grounding applicability |
|-------|-------------------------------|
| C0-C1 | Already satisfied by "smallest proof" if the proof IS a render observation. No additional ceremony required -- if you opened it and saw it work, that counts. |
| C2 | Applies when the work-phase outcome IS a render artifact (the "targeted gate" row). Skip for backend-only C2. |
| C3-C4 | Mandatory when the work-phase outcome includes any render artifact. |

### Over-gating prevention

Fablize measured ~1/3 false-positive nags on its *stop gate* when it fired on task
depth alone (deep-classified turns that changed nothing were still told to "add
observable proof"; see `scripts/gate/verify_state.py` comments and
`docs/MEASUREMENT_PROTOCOL.md` in the fablize repo). The transferable lesson: gate on
what actually happened, not on how the task was classified. This rule therefore
triggers on **artifact type + change**, not on task complexity:

- Trigger: the diff introduces or modifies a file whose correctness requires
  rendering (HTML, SVG, canvas JS, CSS that defines layout, game logic, animation
  keyframes, chart data bindings).
- No trigger: backend services, CLI tools with text output already captured by test
  gates, config files, documentation, pure TypeScript logic with unit tests.

---

## 4. Integration Points

### Anchor in dev-pabcd/SKILL.md section 3 C

Insert after the existing numbered checklist (lines 276-280 of the initiative
copy at `pabcd_initiative/skills/dev-pabcd/SKILL.md`; lines 213-217 in the
cli-jaw copy at `~/.cli-jaw/skills_ref/dev-pabcd/SKILL.md`):

```
### C — Check
Final sanity check:
1. Verify all files saved and consistent
2. Run `npx tsc --noEmit` (if TypeScript project)
3. Update project structure docs if applicable
4. Report completion summary
```

The new rule block goes immediately after item 4, before the paragraph beginning
"Long external gates (CI runs, deploys) inside cli-jaw..."

### dev-testing cross-reference

Add a one-line pointer in dev-testing/SKILL.md section 1.4 "Harness Selector" table:

```
| rendered artifact (visual) | render-grounding loop (dev-pabcd C-RENDER-GROUNDING-01) | static parse alone |
```

This aligns with the existing row pattern: Problem | Primary Harness | Avoid.

### C->D attestation interaction

The C→D attestation form (section 2.1) already accepts freeform `checkOutput`. When
C-RENDER-GROUNDING-01 applies, the render observation (screenshot path, console
output, or description of what was observed) becomes the `checkOutput` value. No
schema change needed -- the existing form accommodates it. The `did` field should
mention the render observation alongside any tsc/test results.

---

## 5. Non-Goals

- **No hook/enforcement layer.** Automated enforcement (observation ledger, CI-gated
  screenshot diffing) is adoption-candidate #1 from the fablize review, tracked
  separately. This rule is agent-self-applied, same as existing C-phase gates.
- **No style/creativity injection.** Fablize ships neither: style mimicry was graded
  negligible/unverified (not shipped), and open-ended creative detail was graded as
  model capability, not transferable procedure. This rule is purely a verification
  modality -- it does not prescribe aesthetic standards.
- **No visual regression baseline system.** Establishing golden-screenshot baselines
  and pixel-diff CI gates is out of scope (belongs in dev-testing if adopted later).

---

## 6. Open Questions — RESOLVED (user interview, 2026-07-05)

1. **Viewport size**: HEURISTIC default 1280x720; the agent may deviate with a stated
   reason. Not a hard DEFAULT — artifact diversity outranks uniformity.
2. **Evidence persistence**: attestation narrative is sufficient for C2-C3. C4
   escalates to STRICT: the observation screenshot is persisted to the devlog for
   durable audit. (Combined resolution with Q4.)
3. **Drive depth for stateful artifacts**: HEURISTIC default — drive until the first
   interactive state change is observed (game started, first wizard transition);
   deviate with a stated reason.
4. **STRICT for C4**: yes — persisted screenshot evidence required at C4, DEFAULT
   (narrative) for C2-C3. Matches the section 9 depth-by-class scaling.

Enforcement-layer decisions from the same interview (deployment scope, soft-warning
gate mode) are recorded in the sibling doc `01_harness_porting.md` section 6. Note:
the enforcement decision supersedes this doc's section 5 first bullet — a soft-warning
enforcement layer WILL ship in the same pass (all three harnesses), so "no
hook/enforcement layer" now reads "no BLOCKING enforcement layer".

---

## 7. Adoption Checklist

- [x] Finalize rule text after open-question resolution (2026-07-05, WP1)
- [x] Insert C-RENDER-GROUNDING-01 into `dev-pabcd/SKILL.md` section 3 C — initiative + instance copies done (WP1); cli-jaw repo copy in WP2
- [x] Add harness-selector row to `dev-testing/SKILL.md` section 1.4 — initiative + instance copies done (WP1); cli-jaw repo copy in WP2
- [x] Update section 9 depth table in dev-pabcd to note render grounding in the C column for C2-C4 (footnote under table, both copies, WP1)
- [ ] Add a worked example to `dev-pabcd/references/` showing attestation with render evidence
- [ ] Verify the rule does not conflict with existing `dev-frontend` visual-testing guidance
- [ ] Test with a real C3 render-artifact work-phase (end-to-end dry run)
