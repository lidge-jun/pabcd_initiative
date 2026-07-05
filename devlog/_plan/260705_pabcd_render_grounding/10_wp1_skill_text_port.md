# WP1 — Rule Finalization + Skill-Text Port (initiative + instance copies)

| Field | Value |
|-------|-------|
| Date | 2026-07-05 |
| Work-phase | WP1 of 4 (WP2-4 = cli-jaw / codexclaw / jawcode repo ports, parallel) |
| Runtime | cli-jaw FSM unavailable (server down, `port undefined`) — degraded per porting recipe step 4 to heuristic worklog attestations in this file |
| Class | C2 (doc/skill-text edits, no code) |

## Heuristic attestations (FSM substitute)

- **P→A** `did`: plan = `00_render_grounding_c_phase.md` (finalized rule text incl.
  interview decisions: HEURISTIC defaults 1280x720/first-state-change, C2-C3
  narrative / C4 STRICT screenshot) + `01_harness_porting.md` section 2 anchors.
  Anchor lines re-verified against both target SKILL.md copies before editing.
- **A→B** `did`: plan audited by 3 parallel opus-4-6 auditors during doc 01
  authoring (5 real issues found and fixed) + boss spot-checks (jawcode
  canTransitionPabcd c→d fall-through confirmed by direct read; dev-testing §1.4
  table shape confirmed in both copies).
- **B→C** `did`: boss wrote all edits directly (no worker mutation):
  1. `devlog/.../00_render_grounding_c_phase.md` — rule text finalized (defaults +
     evidence-scaling paragraph added to the §2 insert-ready block).
  2. `pabcd_initiative/skills/dev-pabcd/SKILL.md` — rule inserted in §3 C after
     item 4; §9 depth-table footnote added.
  3. `~/.cli-jaw/skills_ref/dev-pabcd/SKILL.md` (instance) — same two edits.
  4. `pabcd_initiative/skills/dev-testing/SKILL.md` — §1.4 Harness Selector row.
  5. `~/.cli-jaw/skills_ref/dev-testing/SKILL.md` (instance) — same row.
- **C→D** `checkOutput`: grep -c "C-RENDER-GROUNDING-01" → dev-pabcd copies: 2 each
  (C section + §9 footnote); dev-testing copies: 1 each. diff of the two dev-pabcd
  C-section insert blocks → IDENTICAL. exitCode 0.

## D summary

Rule C-RENDER-GROUNDING-01 is live in the initiative agent-neutral copy and the
instance copy (both dev-pabcd + dev-testing). The cli-jaw REPO copy
(`700_projects/cli-jaw/skills_ref/`) is owned by WP2 (same verbatim text handed to
the implementer) so repo and instance stay in sync.

**Pessimistic close-out (LOOP-PESSIMIST-01):** nothing failed this phase, but (a)
the rule text is now duplicated across 4+ copies with no sync mechanism — drift is
the standing risk (same risk the initiative already carries for the whole dev
family); (b) evidence that this direction is wrong would be: soft warnings firing
on non-render work-phases (false positives) or agents satisfying the rule with
unread screenshots — both only measurable after WP2-4 ship enforcement.

## Follow-ups

- WP2-4 running as parallel opus-4-6 workflow (implement → audit → fix), no git
  commits — working-tree only, boss verifies on completion.
- Post-deploy: measure per-harness warning FP rates before any gate hardening
  (recorded tradeoff, doc 01 §6).
