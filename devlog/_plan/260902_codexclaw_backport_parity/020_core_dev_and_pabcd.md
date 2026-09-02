---
created: 2026-09-02
status: done
tags: [pabcd-initiative, backport, dev, dev-pabcd]
---
# 020 Core: `dev` and `dev-pabcd`

First implementation phase. The two skills every other one routes through, so they go
first: a rule added later cannot be referenced by a router table that already shipped.

Branch `feat/skills-core-backport`, PR #3, based on the roadmap branch rather than `main`
so the stack stays linear.

## Rule count, measured

`120 → 154` unique rule ids in `skills/`, **+34**. Counted with the census script's
pattern against the branch heads, not by summing what the commits claim.

## Commits, and why they split this way

Six, one concern each, in dependency order:

| Commit | Concern |
|---|---|
| `2364769` | git discipline and stacked-PR rules (`DEV-GIT-COMMIT-01`, `DEV-GIT-PUSH-01`, `DEV-STACK-01..05`) |
| `39f824d` | friction, edit-shape, recall, browse-ladder (`DEV-FRICTION-01`, `DEV-EDIT-SHAPE-01`, `DEV-RECALL-01`, `DEV-BROWSE-NATIVE-01`, `SEARCH-BROWSE-01`, `QA-TOOL-LADDER-01`) |
| `a739eab` | A becomes a bounded loop; plan-quality and dispatch rules (`AUDIT-LOOP-01`, `LEAN-REVIEW-01`, `PLAN-VERIFIER-REAL-01`, `PLAN-FIELD-CHAIN-01`, `PLAN-BYPASS-NAMED-01`, `PLAN-TRACK-01`, `DISPATCH-*`) |
| `a1a1542` | `LEXICO-SPLIT-01` moves to three-digit prefixes |
| `3159ec5` | orchestration invariants; docs-first becomes the default (`ORCH-MANDATE-01`, `ORCH-ARTIFACT-01`, `ATTEST-SHAPE-01`, `SESSION-IDENTITY-01`, `LOOP-DOCS-FIRST-01`) |
| `3b7a716` | sub-agent skill injection and discovery (`DEV-SKILL-INJECT-01`, `DEV-SKILL-DISCOVERY-01`) |

7 files, +710/-19. The deletions are router-table lines rewritten to point at new reference
files, not removed rules — the additive constraint holds.

## Two decisions this phase settled

**Three-digit prefixes.** codexclaw uses three digits; this repository mixed two and
three. `a1a1542` migrated `dev-pabcd` and `dev-scaffolding` and states the rule, so the
convention is now enforced by the text rather than by whoever wrote the last doc. The user
chose three digits explicitly when asked.

**`ATTEST-SHAPE-01` describes the runtime as it is.** The attestation keys the rule names
were, at porting time, silently dropped by cli-jaw's parser, so the rule tells agents to
carry the plan-unit pointer inside `did`. That was accurate rather than aspirational. The
runtime half was fixed separately (cli-jaw #500), which is why the wording is worth
revisiting now but was not wrong when written.

## Verification

- Census: gap for these two skills reaches 0 against codexclaw's dev-family set.
- Neutrality scan: clean — no `cxc `, `codexclaw`, or FSM CLI invocation in the ported text.
- No `skills/` content deleted: `git diff --stat` shows deletions only on rewritten router
  lines, checked per commit.
