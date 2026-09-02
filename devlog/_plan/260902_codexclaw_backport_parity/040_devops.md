---
created: 2026-09-02
status: done
tags: [pabcd-initiative, backport, dev-devops]
---
# 040 `dev-devops`

One skill, one commit, its own phase. It earned separation because every rule in it is
about *evidence for a claim about CI or a release* — the class of claim this very unit kept
getting wrong — and because it is the phase whose rules were then immediately exercised
against real gates in the cli-jaw half.

Branch `feat/skills-devops-backport`, PR #5, based on #4's head.

## Rule count, measured

`169 → 186`, **+17**. 4 files, +391/-1.

## Commit

`7646780` — release proof, freeze gates, branch lifecycle, CI evidence.

Rules: `DEVOPS-AUTH-01`, `DEVOPS-RELEASE-PROOF-01`, `DEVOPS-FREEZE-SHA-01`,
`DEVOPS-GATE-WEAKEN-01`, `DEVOPS-REVIEW-THREADS-01`, `DEVOPS-GATE-OWNER-01`,
`DEVOPS-BRANCH-AUTODELETE-01`, `DEVOPS-BRANCH-DELETE-EVIDENCE-01`,
`DEVOPS-BRANCH-SNAPSHOT-01`, `DEVOPS-WORKTREE-DIRTY-01`, plus the evidence rules appended
to `ci-cd-deploy.md` (§6) and `sre-foundations.md` (§7), and the new
`references/branch-lifecycle.md`.

## Structure: appended sections, not a new skill

Ten rules went into `SKILL.md`; the rest were appended as numbered sections to two existing
reference files rather than creating new ones. The router table gains one entry
(`branch-lifecycle.md`) instead of five, which is the point — a router that lists a file per
rule stops being a router.

## The rules that then bound this unit's own work

Worth recording, because a ported rule that is never exercised is just text:

- **`DEVOPS-GATE-WEAKEN-01`** decided how the `browserslist` advisory was handled in
  cli-jaw. Writing an allowlist entry would have been easier than an upgrade and would have
  greened the PR; the rule is why the upgrade happened instead (cli-jaw #501). It also
  decided the shape of the attestation gate — enforcement levels pre-declared rather than
  tightened after the fact (cli-jaw #500).
- **`DEVOPS-EXACT-HEAD-01`** is why criterion (f) is reported as unmet rather than
  "green modulo a known issue". The gates are red on the pushed heads; that is the fact,
  whatever the cause.
- **`DEVOPS-WORKTREE-DIRTY-01`** is why the concurrent session's uncommitted edits were
  stashed and restored around every branch switch in the shared cli-jaw checkout instead of
  being worked around.

## Verification

- Census gap 0 for `dev-devops`.
- Neutrality scan clean. This skill was the highest risk for leakage — release rules tend
  to name a specific CI provider — so the scan output was read rather than trusted.
