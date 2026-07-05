# WP2-4 — Three-Repo Port (cli-jaw / codexclaw / jawcode), Parallel

| Field | Value |
|-------|-------|
| Date | 2026-07-05 |
| Work-phases | WP2 cli-jaw · WP3 codexclaw · WP4 jawcode (parallel opus-4-6 implementers, per-repo parallel auditors) |
| Mode | Soft-warning everywhere (interview decision); no blocking paths |
| Git | No commits by this pipeline. cli-jaw + jawcode changes live uncommitted in their working trees; codexclaw changes were absorbed into another session's commit `4ef5ddf` (see Incident) plus one uncommitted boss fix |

## Heuristic attestations (FSM substitute)

- **B→C** `did` (per repo):
  - **cli-jaw**: skills_ref rule text (submodule) + STATE_PROMPTS['C'] Stage 1.5 +
    builder.ts summary line + `checkRenderGroundingAdvisory()` in attestation.ts
    (GateResult gains optional `advisory`; always `ok:true`) + 8 new tests
    (ATT-RENDER-001..008). Deviation: RENDER_ARTIFACT_PATTERN regex needed
    `(?:\b|\.)` anchor for dot-prefixed extensions.
  - **codexclaw**: skills/pabcd C-phase rule + PHASE_DIRECTIVES.C directive +
    `render-observations.ts` ledger (`.codexclaw/render-observations.jsonl`,
    rows: observation | artifact-modified) + hook JSON + handleStop advisory
    (additionalContext for interactive; appended reason in goal mode) + 23 tests.
    Deviation: bare `.js` excluded from artifact set (too broad); extension set is
    .html/.svg/.css/.jsx/.tsx.
  - **jawcode**: orchestrate-c.md Stage 3 (render grounding; verdict renumbered
    Stage 4) + `render_grounding_status` on PabcdCtx + zod schema (lenient reads) +
    c→d warning via existing `{ok:true, reason}` channel + `--render-observed` /
    `--render-not-applicable` flags + NEXT_HINTS. Deviation: reused existing
    `reason` field rather than new types (most faithful channel).
- **C→D** `checkOutput`:
  - cli-jaw: `tsc --noEmit` clean; phase-attestation 28/28, wiring 3/3,
    state-machine 40/40. exitCode 0.
  - codexclaw: build.mjs OK (78 files); render-observations 23/23; full
    pabcd-state suite 341/341; gate.mjs OK. exitCode 0.
  - jawcode: targeted tests 49/49; `check:types` clean; full jwc-runtime suite
    512 pass / 8 fail — all 8 pre-existing (verified identical on stashed clean
    tree). exitCode 0 on targeted gates.
- **Audits**: 3 parallel per-repo auditors, all **PASS** (one trivial line-wrap
  note in cli-jaw skills_ref §9 footnote). Soft-warning invariant verified per
  repo AND boss-spot-checked in the diffs (`ok: true` on every new path).

## Incident: cross-session commit + dead capture path (codexclaw)

While WP3 ran, another agent session committed `4ef5ddf` ("hook diet 17->10"),
which (a) absorbed our uncommitted WP3 changes into its commit, and (b) moved
`post-tool-use-detecting-edit-shapes.json` to `hooks/_deprecated/`. Our
artifact-modified capture rode that hook's CLI event — with it deprecated,
`hasRenderArtifactModified()` could never see data and the Stop advisory was
**silently dead**: exactly the "enforcement that claims L2 but is actually L1"
failure the porting recipe step (d) warns about.

**Boss fix (C1 patch, direct):** added `apply_patch` to the
render-observations hook matcher and routed the
`post-tool-use-render-observation` CLI event to also call
`handleRenderArtifactCapture` (both handlers self-filter by tool_name).
Re-verified: build OK, render-observations 23/23, gate.mjs OK, dist rebuilt
(fix present in dist/cli.js). This fix is uncommitted in the codexclaw tree.

## D summary — terminal state: DONE

C-RENDER-GROUNDING-01 is live across all four surfaces: initiative + instance
skill copies (WP1), cli-jaw (L1 skills_ref + L1 STATE_PROMPTS + L3 attest
advisory), codexclaw (L1 skill/directive + L2 observation ledger + L2 Stop
advisory), jawcode (L1 prompt + L3 status field warning + verdict flags).
All enforcement soft-warning; no blocking path added anywhere (audited + boss
spot-checked).

**Pessimistic close-out (LOOP-PESSIMIST-01):**
- What did NOT get done: no e2e test for the apply_patch-via-render-hook routing
  (unit tests cover the handlers, not the new matcher routing); jawcode carries 8
  pre-existing unrelated test failures; per-project extension-set config surface
  not built (recorded as future work in WP3 deviations).
- Hypothesis that died: "parallel repo work is isolated per repo" — cross-SESSION
  interference (another instance committing our working tree and deprecating our
  dependency mid-flight) is a live hazard the plan did not model.
- Evidence this direction is wrong would be: warnings firing on non-render
  work-phases (FP), or ledgers showing observations recorded but screenshots never
  read. Both need real usage data — none exists yet.

## Addendum — boss patch-quality review (2026-07-05, post-D)

A direct boss read of all three diffs (end-to-end surfacing traced, not just diff
shape) found three defects the per-repo auditors missed — all of the same family:
**the warning existed but could never reach anyone**.

1. **cli-jaw — advisory produced but dropped.** `GateResult.advisory` had zero
   consumers; `routes/orchestrate.ts` branched on `gate.ok` only, so the ok:true
   advisory never left the server. Fix: surface `advisory` in the transition
   success JSON (+ `TransitionResult.advisory` type). Gates: tsc clean, 68/68
   tests, `npm run build` (dist contract) run.
2. **jawcode — warning condition unreachable.** The c→d warning required
   `render_grounding_status === 'pending'`, but nothing could ever SET 'pending'
   (flags only set observed/not_applicable). The stage-header chip even
   anticipated pending — the setter was simply missing. Fix: `--render-pending`
   flag (mutually exclusive with the other two) + orchestrate-c.md Stage 3 now
   instructs arming it when grounding is in-scope. Gates: check:types clean,
   49/49 targeted tests.
3. **codexclaw — ledger had no cycle scoping.** Append-only forever + "any row
   ever" checks meant one historical observation row suppressed the Stop advisory
   for the project's lifetime (and stale artifact rows mis-triggered it). Fix:
   `resetRenderLedger()` truncates the ledger on every transition into P (cycle
   start) + 2 new tests. Gates: build OK, 25/25 + 21/21.

Minor accepted findings (recorded, not fixed): cli-jaw `\b(ui|game)\b` trigger
words and the broad observation vocabulary (`render`, `opened`, `displayed`) make
the attest advisory a coarse heuristic — acceptable for warn-only under the
laziness threat model; jawcode's recordVerdict render-flag paths have no direct
test coverage (type-checked only).

Meta-lesson for the initiative: diff-shaped audits verify "the code was written";
only end-to-end tracing verifies "the signal reaches the agent." All three misses
were invisible-signal bugs — the next port checklist should include an explicit
"trace the warning to the consumer" step.

## Follow-ups

- Commits: cli-jaw + jawcode working-tree changes and the codexclaw fix are
  intentionally uncommitted (no-proactive-commit policy); commit on user request,
  per-fork, `[agent]` prefix, submodule 2-step for cli-jaw skills_ref.
- Measure per-harness warning FP rates before any gate hardening (doc 01 §6).
- Consider a codexclaw e2e hook test for the apply_patch matcher routing.
