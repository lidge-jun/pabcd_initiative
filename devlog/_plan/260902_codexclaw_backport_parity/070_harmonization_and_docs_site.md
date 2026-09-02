---
created: 2026-09-02
status: done
tags: [pabcd-initiative, harmonization, docs-site, needs-human]
---
# 070 Harmonization and docs-site sync

Final work-phase. Two jobs: settle the `UNIT-RESIDENCE-01` question 002 opened, and
regenerate the published docs so they reflect the ported tree.

## `UNIT-RESIDENCE-01`: NEEDS_HUMAN, not a fix

002 recorded this as an internal contradiction to fix in 020. It is not one, and the
correction is recorded there rather than quietly dropped.

Three statements exist:

| Where | Says |
|---|---|
| this repo, `dev/SKILL.md` | the numbered record doc is "mandatory for **ALL** work" |
| this repo, `dev-pabcd/SKILL.md` | "Ceremony scales with class (§9); **residence does not.** C0-C1 fast-path work skips the PABCD ceremony but MUST leave a numbered record doc in its owning unit" |
| codexclaw, `dev/SKILL.md:48-50` | C0 patches are **exempt**; C1 records **only when a unit already exists** |

The first two **agree**, and the `dev-pabcd` sentence agrees on purpose: it names the
thing that scales and the thing that does not, in one breath. Reading "ceremony scales
with class" as licence to relax residence collapses exactly the distinction that
sentence exists to draw. This repository is internally consistent.

So the divergence is with codexclaw, and this side states its position with a reason
while codexclaw's is a relaxation. Porting the relaxation would weaken a deliberate
rule, which is a semantic decision about how much ceremony a C0 typo owes — not a port.
**Left unported and escalated.** The question for a human is whether "every piece of
development work leaves a numbered record" is worth its cost on one-line fixes, and that
is a judgment about this methodology's own standards, not something the census can
settle.

## docs-site regenerated

`docs-site/build.py` generates HTML from the skills tree rather than being maintained by
hand, so "sync" here means running it. 104 files changed; the substance was checked
rather than assumed:

- **New reference pages exist** — `dev-stacked-prs.html`, `dev-logging.html`,
  `dev-devops-branch-lifecycle.html`, `dev-uiux-design-conversational-ai.html`.
- **New rules reach the published pages** — spot-checked `DEVOPS-FREEZE-SHA-01`,
  `AUDIT-LOOP-01`, `DEV-STACK-01`, `TEST-FLAKE-ELIMINATE-01`; each resolves to at least
  one generated page.
- **This unit is published** as `pages/devlog/260902_codexclaw_backport_parity.html`.
- Search index rebuilt: 39 entries.

The bulk of the 104 is navigation and search-index churn that a full regeneration
produces on every page. That is expected from a whole-site build; what mattered was
confirming the new content is actually in it rather than counting files.

## Unit close-out

| Phase | Outcome |
|---|---|
| 010 in-tree design-evidence capture | DONE — 19 gap closures, 2 commits |
| 020 core (`dev`, `dev-pabcd`) | DONE — 34 rules |
| 030 verification family | DONE — 15 rules + 13 runtime references (1165 lines) |
| 040 `dev-devops` | DONE — 17 rules + `branch-lifecycle.md` |
| 050 frontend / UI-UX | DONE — 49 rules, `asset-requirements.md` rewritten 80 → 585 lines |
| 060 remainder | DONE — 8 rules; `dev-architecture` reported **NOOP** (full parity, ahead on content) |
| 070 this doc | DONE — divergence escalated, docs-site regenerated |

Terminal outcome for the skills half: **DONE.** Gap census 121 → **0**, 241 rule ids
against codexclaw's 233 dev-family set, agent-neutrality scan clean by committed script,
and the six repository-original rules intact through every commit.

One item is **NEEDS_HUMAN**: the `UNIT-RESIDENCE-01` divergence above.

## Three corrections this unit made to itself

Worth keeping together, because they share one failure shape — concluding from two
documents read against each other instead of reading the load-bearing sentence in full,
or from a sample instead of a census.

1. **`DIVERGE-TIER-01`** (001) read as absent from codexclaw and therefore a candidate
   for removal. It lives in codexclaw's `loop` skill, outside the dev-family scope the
   census uses. `gap-census.sh` now separates the two classes mechanically.
2. **cli-jaw's document numbering** (002) claimed "not one file uses 2-digit". Real
   numbers: 492 three-digit against 107 two-digit, the latter concentrated in 2026-06
   units. A loop that listed only recent units generalized. The conclusion survived and
   is better supported by the true numbers than the false ones.
3. **`UNIT-RESIDENCE-01`** (this doc) called an internal contradiction; the two documents
   agree and say so explicitly.

Each was caught by widening the measurement rather than by rereading the reasoning, which
is the practical lesson: when a drift claim rests on a comparison, check it against the
tree.
