---
created: 2026-09-02
status: done
tags: [pabcd-initiative, backport, dev-debugging, dev-testing, dev-code-reviewer]
---
# 030 Verification family: debugging, testing, code review

The three skills that decide whether work is finished. Grouped into one phase because they
share a single subject — what counts as evidence — and splitting them would have put
`TEST-ORACLE-INDEPENDENCE-01` in a different review from
`REVIEW-GUARD-REMOVAL-01`, which is the same idea seen from two sides.

Branch `feat/skills-verification-backport`, PR #4, based on #3's head.

## Rule count, measured

`154 → 169`, **+15**. 17 files, +1472/-14.

The line count is dominated by references rather than rules: 13 new per-runtime debugging
guides, 1165 lines. A rule count alone would have made this phase look like the smallest
one when it is the largest by content.

## Commits

| Commit | Concern |
|---|---|
| `7f0d861` | RCA evidence gate, toggle proof, and 13 runtime references (`DEBUG-RCA-EVIDENCE-01`, `DEBUG-TOGGLE-PROOF-01`) |
| `9760604` | oracle-integrity rules, row reachability, the flake policy (`TEST-ROW-REACHABLE-01`, `TEST-PROMPT-SEAM-01`, `TEST-ORACLE-INDEPENDENCE-01`, `TEST-PRECEDENCE-FIXTURE-01`, `TEST-CI-GREEN-01`, `TEST-CU-QA-01`) |
| `ad2684f` | guard-removal, worktree, retired-capability review rules (`REVIEW-GUARD-REMOVAL-01`, `REVIEW-WORKTREE-01`, `REVIEW-REMOVED-BACKEND-01`) |

## The one replacement in an otherwise additive port

`ci-pipeline.md` had a 15-line "Flaky Test Quarantine Strategy". codexclaw's canonical
`TEST-FLAKE-*` policy is 90 lines and covers what those 15 said plus attribution,
stability windows, and elimination. Keeping both would have left two policies disagreeing
about when a quarantine expires.

So this is the phase's one **replacement** rather than an append, and it is recorded here
because "additive only" is the unit's stated constraint. The test applied: does the new
text say everything the old text said? Checked line by line before removing — the old
strategy's three substantive claims (quarantine needs an owner, needs an expiry, and needs
a linked defect) all appear in the replacement as `TEST-FLAKE-QUARANTINE-01` and
`TEST-FLAKE-ELIMINATE-01`.

## Runtime references generalized, not copied

The 13 guides (node, python, rust, go, c-cpp, jvm, swift, ruby, beam, nextjs-react,
node-backend, vite-vitest, playwright) came from codexclaw with provenance stripped: tool
names that only exist in that host were replaced with the capability they provide, so a
reader on a different runtime is told what to look for rather than what to type.

## Verification

- Census gap 0 for all three skills.
- Neutrality scan clean, including the 13 new reference files — this is where host-specific
  tool names were most likely to leak, since debugging guides are inherently tool-shaped.
