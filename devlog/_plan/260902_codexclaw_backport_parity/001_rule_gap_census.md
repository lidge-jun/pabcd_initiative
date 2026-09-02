---
created: 2026-09-02
status: active
tags: [pabcd-initiative, skills, census, codexclaw-backport]
---
# 001 Rule-Id Census — What Actually Drifted

Method: named rules in this ecosystem carry `FAMILY-TOPIC-NN` ids
(`DEV-GIT-COMMIT-01`, `FE-RENDER-PATH-02`). Counting ids is an exact parity
signal — a rule either has an id in a tree or it does not — so the gap can be
measured rather than estimated. Reproduce with `gap-census.sh` in this
directory; every number below is its output.

Trees read at working-tree state, not `HEAD`. That matters for
`pabcd_initiative`, whose 22 uncommitted `dev-frontend` / `dev-uiux-design`
files already carry part of the port (000, "Uncommitted work already in the
tree"); counting `HEAD` would overstate its gap.

## Inventory

| Tree | Scope counted | Rule ids |
|---|---|---|
| `codexclaw/plugins/codexclaw/skills` | the 13 dev-family skills only | **233** |
| `pabcd_initiative/skills` | all 13 skills | **120** |
| `cli-jaw/skills_ref/jaw-dev*` | the 15 `jaw-dev*` skills | **147** |

`codexclaw` carries 28 skill directories; only the 13 with counterparts in both
targets are counted. The 15 excluded (`loop`, `qa`, `search`, `orchestrate`,
`recall`, `remote`, `interview`, `skill-hub`, `worktree-guardian`, `ast-grep`,
`goalplan`, `kwrite`, `lunasearch`, `repo-map`, `dev-diagram-viewer`) are
codexclaw-runtime surfaces. Their rules are out of scope by construction: a
skill that documents `cxc map` has nothing to give an agent-neutral repository.

## Gap

| Measure | Count |
|---|---|
| in codexclaw dev-family, absent anywhere in `pabcd_initiative` | **121** |
| in codexclaw dev-family, absent anywhere in `jaw-dev*` | **91** |
| needed by both targets | 86 |
| needed by `pabcd_initiative` only | 35 |
| needed by `cli-jaw` only | 5 |

"Absent anywhere in the tree" is the right denominator, not "absent from the
matching skill". The three trees place the same rule in different skills —
`PHASE-SPLIT-01` and `LEXICO-SPLIT-01` sit in `dev` in codexclaw but in
`dev-pabcd` in `pabcd_initiative`. A per-skill diff reports those as gaps and
would have the port duplicate a rule the target already has, under a second
owner. Only a tree-wide absence is a real gap.

### Every gap rule already has a dev-family home

The first pass at this census mis-attributed ownership: it reported
`DEV-GIT-COMMIT-01` as living in `loop/SKILL.md:364`, which is a
cross-reference ("Canonical rule ids: `DEV-GIT-COMMIT-01`, ..."), not the rule.
The rule is at `dev/SKILL.md:406`. `gap-census.sh` now searches the dev family
before the whole tree for exactly this reason, and the corrected run resolves
**all 121 and all 91** inside the dev family with zero whole-tree fallbacks.

That result is load-bearing for the roadmap: there is no rule that needs a new
home invented for it in the targets. Every port is "append this rule to the
skill that already owns its family", which is the shape `46bfa38` established
and the shape a reviewer can check. Had even one rule resolved only to `loop/`
or `qa/`, it would have needed a placement decision — a design question, not a
port — and would have belonged in `NEEDS_HUMAN` rather than in a commit.

## Where the gap lives

Gap rules grouped by the codexclaw skill that owns them:

| Owning skill | `pabcd_initiative` needs | `cli-jaw` needs |
|---|---|---|
| `dev-frontend` | **40** | 8 |
| `dev` | 19 | **18** |
| `dev-devops` | 17 | **17** |
| `pabcd` → `dev-pabcd` | 15 | **17** |
| `dev-testing` | 10 | 9 |
| `dev-uiux-design` | 9 | 8 |
| `dev-code-reviewer` | 3 | 4 |
| `dev-security` | 2 | 2 |
| `dev-debugging` | 2 | 2 |
| `dev-backend` | 2 | 2 |
| `dev-scaffolding` | 1 | 3 |
| `dev-data` | 1 | 1 |

Three findings change the plan.

**The premise was half right.** `cli-jaw` is behind codexclaw, but it is not
uniformly behind — and it is *ahead* of `pabcd_initiative` in one large area.
`jaw-dev-frontend` carries 71 of codexclaw's 79 frontend rules; the canonical
repository's `dev-frontend` carries 36 even counting the uncommitted work. So
33 of the 35 rules only `pabcd_initiative` needs are `FE-*` / `UX-*` rules that
`cli-jaw` already shipped. The frontend back-port is a `pabcd_initiative`
problem, not a shared one, and `cli-jaw`'s existing text is a second reference
for the agent-neutral rewrite — cheaper and better-tested than translating
codexclaw's from scratch.

**`cli-jaw` is behind `pabcd_initiative` on five rules.** `ARCH-DECISION-01`,
`ARCH-MAP-01`, `CATALOG-DESIGN-FIRST-01`, `INTERVIEW-CATALOG-01`,
`LOOP-EXPLORE-SELECT-01` exist in the canonical repository and in codexclaw but
not in `jaw-dev*`. Drift here is bidirectional; the ecosystem is not a chain
with one stale end.

**`dev-devops` never got ported at all.** codexclaw has 19 `DEVOPS-*` rules;
both targets have 1. This is not drift, it is an entire skill upgrade that
never travelled. It is also the family most likely to contain
codexclaw-specific content (CI workflow names, branch-protection specifics), so
it needs the closest reading despite being mechanically simple.

## Rules the targets own and codexclaw does not

These exist in a target but have no codexclaw counterpart, so a wholesale sync
deletes them. That is exactly what `7d196d6` did and why `ec6ae5c` reverted it
(000, "The precedent that constrains this unit").

| Tree | Target-only rules |
|---|---|
| `pabcd_initiative` | `FAMILY-FRESH-01`, `FE-MOTION-EXPERIENCE-01`, `INTERVIEW-CLASSIFY-01`, `INTERVIEW-DIVERGE-01`, `PABCD-AUTO-01`, `PROMPT-ROUTING-01` |
| `cli-jaw` | `FAMILY-FRESH-01`, `INTERVIEW-CLASSIFY-01`, `PABCD-AUTO-01`, `PROMPT-ROUTING-01` |

Both lists survive this unit unchanged. `gap-census.sh` prints them under
"NEVER delete these" so the C-phase check is a diff against that line rather
than a memory of this paragraph.

**Two more ids looked target-only and are not.** `DIVERGE-TIER-01` (both
targets) and `INTERVIEW-TEACH-01` (`pabcd_initiative`) are absent from
codexclaw's *dev family* but present in its runtime skills —
`loop/SKILL.md` and `loop/references/divergence-tiers.md` for the first,
`interview/SKILL.md` for the second. The first version of this census read them
as upstream inventions codexclaw had dropped, which is backwards: they are
artifacts of scoping the comparison to the 13 dev-family skills.

The distinction is not cosmetic. "Codexclaw does not have this rule" invites
deleting it from the targets to reduce divergence; "codexclaw has it under a
different owner" means the only question is placement, and the answer is
already settled — `260707_diverge_tier_01_adoption` records `DIVERGE-TIER-01`
as a deliberate adoption into `dev-pabcd`. `gap-census.sh` now diffs
target-only ids against the full codexclaw tree and prints the two classes
under separate headings, so the trap is closed mechanically rather than by this
warning.

## What the census cannot see

The count proves presence, not agreement. A rule id in both trees can carry
materially different text — codexclaw's `LEAN-REVIEW-01` (2026-08-18) rewrote
an `A>B` gate that earlier versions stated as unconditional, and an id-level
census reads that as parity. Three classes of drift are invisible here:

1. **Wording drift** — same id, stronger or narrower requirement.
2. **Severity drift** — same id, moved between `DEFAULT` / `STRICT` /
   `ESCALATE` / `HEURISTIC`.
3. **Reference drift** — the rule is unchanged but the `references/*.md` it
   points at gained sections.

Detecting those is a read, and it is delegated to per-skill review in the
implementation cycles rather than claimed here. The census bounds the work; it
does not complete the audit. Each decade doc's A phase owns the drift read for
its own skills, and a `NOOP` verdict for a skill requires the read, not the
count.

## Reference-file gap

Rule ids undercount the port: 34 of `pabcd_initiative`'s 121 missing rules live
under `dev-frontend/references/core/*`, and a reference file can be missing
entirely without any rule id marking its absence. Checked by path against the
working tree:

| codexclaw file | in `pabcd_initiative` | in `cli-jaw` |
|---|---|---|
| `dev/references/skill-catalog.md` | absent | — |
| `dev/references/static-analysis.md` | absent | — |
| `dev/references/logging.md` | absent | — |
| `dev/references/stacked-prs.md` | absent | — |
| `dev-frontend/references/core/dropdown-layer.md` | absent | — |
| `dev-uiux-design/references/intent-discovery-ladder.md` | absent | — |
| `dev-uiux-design/references/korean-design-vocabulary.md` | absent | — |
| `dev-debugging/references/runtimes/` (9 files + `js/`) | absent | **present** |

The last row repeats the pattern from `dev-frontend`: `cli-jaw` already carries
the per-runtime debugging references that the canonical repository never
received. Where `cli-jaw` has the file, its text is the better source for the
agent-neutral rewrite — it has already been through one adaptation and one
review cycle, so translating it costs less than de-codexclaw-ing the original
and is less likely to leak vocabulary.

The `—` cells are not "present"; they are "not yet checked for `cli-jaw`",
whose reference-file audit belongs to its own devlog unit. Per-skill file
enumeration lives in the decade docs, not here.
