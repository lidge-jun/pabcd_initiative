---
created: 2026-09-02
status: active
tags: [pabcd-initiative, skills, dev-frontend, dev-uiux-design, award-corpus]
---
# 010 Capture the In-Tree Design-Evidence Port

Work-phase 1. Deliverable: the 22 uncommitted `dev-frontend` /
`dev-uiux-design` files already in the working tree become commits, attributed
as pre-existing hand-written work rather than as this session's back-port.

## Why this is a work-phase and not a cleanup step

The files were written by hand in an earlier session and never committed.
Leaving them uncommitted while the back-port proceeds fails two ways. LOOP-GIT-01
is the first: committed work survives compaction and a failed cycle, uncommitted
work does not, and this unit spans multiple cycles by construction. The second
is attribution — the moment a later phase edits the same files, the diff mixes
hand-authored lines with machine-assisted ones and no reviewer can tell which
audit applies to which line.

It is also the reason the census reads the working tree rather than `HEAD`
(001, header). These files already close part of the gap. Counting `HEAD` would
have sized this repository's `dev-uiux-design` deficit too high and sent a later
phase to re-port rules that are sitting on disk.

## What the change actually is

`+164 / -13` across 16 modified files, plus 6 new reference files totalling 833
lines. The content is one coherent thesis: **award-corpus findings become dated,
bounded design evidence, and evidence never becomes a gate bypass.**

New reference files:

| File | Lines | Content |
|---|---|---|
| `dev-frontend/references/core/reference-capture.md` | 147 | analysis-only capture of third-party references, provenance manifest, legal boundary, never-ship gate |
| `dev-frontend/references/core/section-level-sourcing.md` | 101 | dated gallery paths, section-type retrieval |
| `dev-frontend/references/core/top-bar.md` | 136 | award-calibrated bar geometry, slots, scroll states, mobile collapse |
| `dev-uiux-design/references/compositional-patterns.md` | 196 | composition vocabulary |
| `dev-uiux-design/references/design-award-sources.md` | 115 | the award corpus itself, with crawl dates |
| `dev-uiux-design/references/design-trends.md` | 138 | trend maturity, risk, re-crawl rules |

Measured against the pre-phase `HEAD` (`56ce13a`), the tree goes from 100 rule
ids to 120 — **20 ids added**:

`FE-A11Y-UNUSUAL-NAV-01`, `FE-CAPTURE-01` … `FE-CAPTURE-08`, `FE-HERO-01`,
`FE-HERO-LIGHT-CENTER-01`, `FE-HERO-SPLIT-01`, `FE-LIQUID-STATE-01`,
`FE-MOTION-BUCKET-01`, `FE-MOTION-EXPERIENCE-01`, `FE-PILL-NEST-01`,
`FE-SECTION-SOURCE-01`, `FE-TOPBAR-DOMAIN-01`, `FE-TOPBAR-HOVER-01`,
`FE-TOPBAR-STATE-01`.

**19 of the 20 are real gap closures** — they exist in codexclaw's dev family,
so this phase retires them from the back-port backlog and later phases must not
re-port them.

The twentieth, `FE-MOTION-EXPERIENCE-01`, exists nowhere in codexclaw. It is
this repository's own rule, and it is worth noting because two independent
computations agreed on it: the census's "target-only, genuinely absent from ALL
of codexclaw" list (001) was derived from a tree-wide id diff, and this
per-commit diff arrived at the same single id from the other direction. That
agreement is the reason the "NEVER delete these" line can be trusted as a gate
rather than a note.

The modified files are router-table rows pointing at the new references plus the
carve-outs the new evidence justifies. The load-bearing line is the one added to
`dev-frontend/SKILL.md`:

> Award-derived exceptions in these references are calibrated design evidence,
> not blanket permission to bypass the existing domain, accessibility,
> performance, or anti-slop gates.

`FE-A11Y-UNUSUAL-NAV-01` is that sentence made enforceable: SiteInspire
unusual-layout winners justify a visual system, never the removal of the
accessible route. Every carve-out in the diff is scoped the same way — one
material field per viewport, one bounded hero, a named-variant list with crawl
dates (Vectr, Fin, Michael Pumo, 2026-07-14) rather than an open exemption.

## Provenance

All six new files exist in both `codexclaw/plugins/codexclaw/skills/` and
`cli-jaw/skills_ref/jaw-dev-{frontend,uiux-design}/`, verified by path. So this
is the same back-port this unit continues, resumed by hand and stalled before
commit — not original work invented here, and not something that will conflict
with the upstream text a later phase reads.

## Commit split

Two commits, one per skill, because `dev-frontend` and `dev-uiux-design` are
separately owned surfaces and a reviewer of one should not have to read the
other:

1. `feat(dev-frontend): award-calibrated top bar, reference capture, section sourcing`
2. `feat(dev-uiux-design): design trends, award sources, compositional patterns`

Both land on `feat/skills-core-backport`, below the core back-port commits, as
the bottom of PR 1 (000, "Stack shape").

## Verification

Docs-only phase, so the gates are textual. All three ran before the commits.

- **Gap census is unchanged at 121.** This is the receipt, and its direction is
  counter-intuitive enough to state: the census reads the *working tree*, which
  already contained these files, so committing them must move the number by
  zero. A drop would mean the commit changed content it was only supposed to
  capture; a rise would mean it lost some. The 19 closures are visible against
  `HEAD` (above), not against the census baseline — which is exactly why 001
  reads the tree instead of `HEAD`.
- **Agent-neutrality grep is clean.** No `cxc`, `cxc-`, `.codexclaw`,
  `codexclaw`, `SubagentStop`, `cli-jaw`, or `jaw ` token in
  `skills/dev-frontend` or `skills/dev-uiux-design`. A grep, not a judgment.
- **Every new reference is reachable from a router table.**
  `reference-capture.md`, `section-level-sourcing.md`, `top-bar.md` from
  `dev-frontend/SKILL.md`; `compositional-patterns.md`,
  `design-award-sources.md` from `dev-uiux-design/SKILL.md`;
  `design-trends.md` from both. An unreferenced reference file is dead weight
  the router never loads.
- **"NEVER delete these" line unchanged** — the six repository-original rules
  survive, `FE-MOTION-EXPERIENCE-01` among them.

## Outcome

`DONE`. Two commits on `feat/skills-core-backport`: `9dd844f` (dev-frontend),
`34fff2c` (dev-uiux-design). `NOOP` was not available for this phase — the files
existed and were uncommitted, so there was work by definition.

