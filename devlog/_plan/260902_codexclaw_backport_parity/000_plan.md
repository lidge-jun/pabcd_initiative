---
created: 2026-09-02
status: active
tags: [pabcd-initiative, skills, codexclaw-backport, parity, cxc-loop]
---
# 260902 Codexclaw Backport — Skill Parity Across the Ecosystem

Trigger: the ecosystem drifted. Skill upgrades accumulated in `codexclaw`
(`plugins/codexclaw/skills/`, 28 skill directories) while the two upstream
homes stayed where they were — this repository's `skills/` (13 agent-neutral
skills) and `cli-jaw/skills_ref`'s `jaw-dev*` family (15 skills). The same
session also refreshes `cli-jaw`'s stale model catalog from `opencodex` and
`codexclaw`; that half is recorded in `cli-jaw`'s own devlog unit, not here.

Run as a `cxc-loop`: one work-phase per full PABCD cycle, this docs-only cycle
first (LOOP-DOCS-FIRST-01), parallel read-only investigation delegated to
`grok-4.6` subagents, all writes and commits owned by the main session.

## The lineage decides the direction of the port

`README.md` (lines 6-9, 38-39, 48-50) fixes the ecosystem's shape, and it is
not a tree with codexclaw at the root:

- `cli-jaw/skills_ref` is the **live deploy source**. This repository's
  `skills/` is a snapshot taken from it at the 2026-07-02 75-grade upgrade,
  then made agent-neutral — "This is a COPY".
- This repository is the **canonical methodology home**: agent-neutral, no
  host-CLI commands, `orchestrate <phase>` left abstract so any runtime can
  bind it.
- `codexclaw` (`cxc-*`) and `jawcode` (`jwc`) are **downstream adaptations**.
  "Ports are adapted, never blind-copied."

So the work is a **back-port**: content that grew in a downstream adaptation
has to travel back into the canonical home and into the live deploy source.
That is not the usual direction, and it is the reason the two targets need
different treatment rather than the same patch:

| Target | Vocabulary contract | Port style |
|---|---|---|
| `pabcd_initiative/skills/` | agent-neutral; no `cxc`, no `.codexclaw/`, no hook names | additive only |
| `cli-jaw/skills_ref/jaw-dev*` | cli-jaw's own surface (`jaw orchestrate`, `jaw-*` ids) | adapted translation |

## The precedent that constrains this unit

This exact back-port was attempted once and reverted. On 2026-07-12, within
five minutes:

- `7d196d6` `sync(skills): deploy improved dev-* skills from codexclaw session
  260711-12` — a wholesale sync, 39 files, **+3536 / -1188**. It replaced
  `SKILL.md` bodies rather than appending to them.
- `ec6ae5c` `Revert "sync(skills): deploy improved dev-* skills..."` — reverted
  at 17:52.
- `46bfa38` `feat(skills): port new rules from codexclaw (agent-neutral,
  additive only)` — landed at 17:57. 11 files, **+376 / -0**.

The 1188 deleted lines are the finding. A wholesale sync overwrites the
agent-neutral rewriting that is the whole point of this repository, so the
accepted shape is the third commit's: append whole named rule sections, add
whole new reference files, delete nothing. `4e4db8e` and `56ce13a` then did a
harmonization pass (dev-is-canonical, role boundary, bidirectional cross-refs)
that later ports must not undo.

Consequence for this unit: **additive only, and nothing that 46bfa38 already
landed gets re-landed.** The 46bfa38 subset (+376) is far smaller than the
reverted sync (+3536), so a large amount of codexclaw content is still
unported — deliberately, because it needed agent-neutral rewriting first. That
backlog is what the decade docs below enumerate.

## Scope, measured

Full census in `001_rule_gap_census.md`, reproducible via `gap-census.sh`:
codexclaw's 13 dev-family skills carry **233** named rule ids;
`pabcd_initiative` carries 120 and is missing **121**; `cli-jaw`'s `jaw-dev*`
family carries 147 and is missing **91**. 86 rules are needed by both.

Two census results change this roadmap rather than merely sizing it:

- **`cli-jaw` is ahead of the canonical repository on frontend.**
  `jaw-dev-frontend` has 71 of codexclaw's 79 `FE-*` rules; `dev-frontend` here
  has 36. 33 of the 35 rules only this repository needs are frontend/UX rules
  `cli-jaw` already shipped, and its `dev-debugging/references/runtimes/` tree
  exists there and not here. So `cli-jaw`, not codexclaw, is the better source
  for those ports: its text has already survived one adaptation and one review.
- **`dev-devops` never travelled at all.** codexclaw has 19 `DEVOPS-*` rules;
  both targets have 1. That is not drift, it is a whole skill upgrade that never
  left, and it earns its own work-phase below.

## Uncommitted work already in the tree

`git status --porcelain` shows 22 files that belong to this unit, not to some
other session:

- modified: `skills/dev-frontend/SKILL.md` + 8 files under
  `skills/dev-frontend/references/core/`
- modified: `skills/dev-uiux-design/SKILL.md` + 6 files under
  `skills/dev-uiux-design/references/`
- untracked: `dev-frontend/references/core/{reference-capture,section-level-sourcing,top-bar}.md`,
  `dev-uiux-design/references/{compositional-patterns,design-award-sources,design-trends}.md`

16 modified + 6 new, `+164 / -13`. Three of the new files
(`reference-capture.md`, `top-bar.md`, and the `dev-uiux-design` additions)
appear in the reverted sync's file list, so this is the same back-port resumed
by hand and never committed. It is **already-ported content**: the gap analysis
for `dev-frontend` and `dev-uiux-design` compares codexclaw against the
WORKING TREE, not against `HEAD`, or the port double-applies. These files
become the bottom commit of the stack.

## The dependency graph is two deep, and that is measured

PHASE-SPLIT-01 forbids effort buckets, so the phase order has to come from real
dependency edges. The edges here are textual: a ported rule that cites another
rule id dangles if the cited rule has not landed. Computed by intersecting
(rules each non-core skill cites) ∩ (rules core owns) ∩ (rules still missing
from the target):

| Skill | Needs from core — `pabcd_initiative` | Needs from core — `cli-jaw` |
|---|---|---|
| `dev-scaffolding` | `LOOP-DOCS-FIRST-01` | `LOOP-DOCS-FIRST-01` |
| `dev-code-reviewer` | `AUDIT-LOOP-01`, `DEV-STACK-05` | `AUDIT-LOOP-01`, `DEV-STACK-05` |
| `dev-devops` | `DEV-STACK-03` | `DEV-STACK-03` |
| `dev-testing` | `QA-TOOL-LADDER-01` | — |
| `dev-debugging` | `QA-TOOL-LADDER-01` | — |
| `dev-frontend` | `FE-AI-TELL-01` | — |
| `dev-uiux-design` | `FE-AI-TELL-01` | — |
| `dev-architecture`, `dev-backend`, `dev-data`, `dev-security` | — | — |

Every edge points at the core (`dev` + `dev-pabcd`). **No edge runs between two
non-core skills.** The genuine dependency structure is therefore two layers,
not five: core, then everything else in parallel, with four skills independent
even of the core.

That is the finding the stack shape has to respect. Serializing
`dev-devops` behind `dev-testing` would be a false merge order — exactly the
anti-pattern DEV-STACK-01 names — because neither consumes the other.

## Work-phase map

One decade doc = one work-phase = one full PABCD cycle. Never two in one B.

| Doc | Work-phase | Depends on | Independently proves |
|---|---|---|---|
| `010` | Commit the in-tree `dev-frontend` / `dev-uiux-design` port | — | the resumed hand-port is captured and attributed |
| `020` | Core: `dev` + `dev-pabcd` (19 + 15 rules) | 010 | every cited rule id in later phases resolves |
| `030` | Verification: `dev-testing`, `dev-code-reviewer`, `dev-debugging` (15) | 020 | the gates the core names are checkable |
| `040` | `dev-devops` (17) | 020 | the never-ported CI/release family exists |
| `050` | `dev-frontend`, `dev-uiux-design` (49) | 020 | the largest surface, sourced from `cli-jaw` |
| `060` | `dev-architecture`, `dev-backend`, `dev-data`, `dev-security`, `dev-scaffolding` (8) | 020 | no dangling reference remains anywhere |
| `070` | Harmonization + `docs-site` sync | 020-060 | ownership and cross-ref invariants survived |

`010` is a separate work-phase because its provenance differs: it is
pre-existing hand-written work, and folding it into `020` would leave a
reviewer unable to tell which lines were hand-authored and which were
back-ported in this session.

`040` gets its own phase despite being mechanically simple. `dev-devops` is the
family most likely to carry codexclaw-specific CI details (workflow names,
branch-protection specifics), so its de-codexclaw-ing needs a dedicated audit
rather than a share of a mixed phase.

`070` is the only phase that genuinely depends on more than the core: it
verifies cross-references across everything the other phases landed.

## Stack shape

Seven work-phases, but the dependency graph above says the stack cannot honestly
be seven deep. Published shape — six layers, linear:

```
feat/skills-remainder-harmonize   → PR 6 (base: PR 5 head)   060 + 070
feat/skills-frontend-backport     → PR 5 (base: PR 4 head)   050
feat/skills-devops-backport       → PR 4 (base: PR 3 head)   040
feat/skills-verification-backport → PR 3 (base: PR 2 head)   030
feat/skills-core-backport         → PR 2 (base: PR 1 head)   020
docs/backport-roadmap-260902      → PR 1 (base: main)        000 + 001 + 010
──────────────────────────────────  main
```

PR 1 is the roadmap plus the in-tree capture, and it is a real review boundary
rather than a formality: it is where the *convention* is agreed — additive-only,
agent-neutral, `cli-jaw` as the source for frontend, the census script as the
gate. Every layer above it is an application of that convention, so reviewing
the convention after five layers of it have landed is the wrong order. It also
means the bottom layer is reviewable and mergeable today, before the content
work is drafted.

Two decisions in that shape are worth naming, because both trade against a rule
rather than following one:

**Layers 2-4 are serialized by choice, not by dependency.** `030`, `040`, and
`050` each depend only on the core. Parallel PRs off PR 1 would be the literal
DEV-STACK-01 answer. A linear stack is chosen anyway because `070` has to sit on
top of all of them, and a diamond — three parallel PRs re-converging into one —
has no bottom-up merge order at all. The cost is honest: merging PR 2 does not
require PR 3 or PR 4, so a reviewer who wants PR 3 first can merge it and let
GitHub retarget the rest. The stack expresses review order, and the PR bodies
say so rather than implying a dependency that the census disproves.

**Five layers is at the depth DEV-STACK-01 says to think hard about.** Accepted
because each layer is one coherent rule family with its own audit, and the
alternative — landing the bottom half first, then stacking the rest — costs a
second planning cycle for no reviewability gain. If any layer's cascade turns
out to be expensive, the fallback is exactly that: ship PR 1-2, land them, then
re-stack.

Merge stays user-authorized (DEV-STACK-04). Cascades use
`git rebase --update-refs` and `--force-with-lease`, never bare `--force`
(DEV-STACK-02).

## Out of scope

- No changes to `codexclaw`. It is the source and is read-only for this unit.
  It currently carries its own uncommitted work (`ast-grep`,
  `dev-diagram-viewer`) which must not be disturbed.
- No changes to `opencodex` runtime.
- `jawcode` is a third downstream adaptation and is not in this session's
  scope; if the back-port creates a `jawcode` obligation, it goes to
  `backlog/`, not into this unit.
- No merges. No version bumps. No release promotion.

## Terminal outcomes

`DONE` requires: every ported rule traceable to a codexclaw source file and
line; no `cxc`/`.codexclaw`/hook vocabulary anywhere in `skills/`; nothing from
`46bfa38` re-landed; the docs-site parity check passing; stacked PRs open with
correct base refs. `NOOP` per work-phase if that skill turns out to already
have parity. `NEEDS_HUMAN` if a rule encodes a semantic divergence between the
ecosystems rather than a wording difference — those are decisions, not ports.
