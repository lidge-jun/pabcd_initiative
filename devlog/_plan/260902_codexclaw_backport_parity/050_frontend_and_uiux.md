---
created: 2026-09-02
status: done
tags: [pabcd-initiative, backport, dev-frontend, dev-uiux-design]
---
# 050 Frontend and UI/UX

The largest phase by rule count, and the only one where the upstream files had diverged
enough that a merge was needed rather than an append.

Branch `feat/skills-frontend-backport`, PR #6, based on #5's head. This branch also carries
060 and 070 (see 060 for why they were not split further).

## Rule count, measured

`186 → 241` across this branch, **+55** — of which 060's remainder commit accounts for 13,
leaving **+42** for the frontend/UI-UX work proper.

## Commits

| Commit | Concern |
|---|---|
| `8d7d62c` | merge the fuller upstream references, losslessly |
| `aca6ca2` | name the unnamed rules; add concept and icon strategy |

Rules include `FE-AI-TELL-01`, `FE-A11Y-POLISH-01`, `FE-AESTHETIC-HONESTY-01`,
`FE-ICON-01`, `FE-ASSET-*` (concept, prompt, select, parallel, provider, bg),
`FE-IMAGE-SET-CONTINUITY-01`, `FE-IMAGE-ANCHOR-ROTATION-01`, `FE-MOTION-HONESTY-01`,
`FE-MOTION-VIDEO-01`, `FE-MEDIA-BUDGET-01`, and on the UX side `UX-AUDIENCE-01`,
`UX-DIAL-PRESET-01`, `UX-IMAGE-FIRST-01`, `UX-ASSET-GEN-01`, `UX-ICON-01`,
`UX-CONVERSATION-*`.

New reference files: `content-surface-pipeline.md`, `dropdown-layer.md`,
`token-source-divergence.md`, `conversational-ai.md`, `intent-discovery-ladder.md`,
`korean-design-vocabulary.md`.

## The lossless merge, and what "lossless" required

`8d7d62c` is the one place where upstream and local had both grown, so neither side could
simply win.

**`anti-slop.md`** — upstream was fuller, but the local copy carried three things upstream
did not: the Material-Field Exemption, the Bounded Authored Field Exemption, and the
split-hero template. Taking upstream wholesale would have deleted them silently, which is
exactly the failure mode that got the earlier wholesale sync (`ec6ae5c`) reverted.

All three survived, but the third survived **twice**, and writing this record is what caught
it. The merge kept the local unnamed split-hero line *and* took upstream's
`FE-HERO-SPLIT-01`, leaving two rules on one subject at different thresholds:

| | Threshold |
|---|---|
| upstream, named | never choose it unprompted; build only on explicit request, propose only for paid-conversion LPs |
| local, unnamed | reserve it for conversion-focused paid landing pages only |

The named version subsumes the other clause for clause and is stricter — its `Default:`
applies everywhere, where the local line scoped itself to brand/product homepages. Two
thresholds for one decision is worse than one, because a reader who wants the split hero can
satisfy the laxer sentence and stop reading.

So the duplicate was removed, and upstream's clarifying exemption — which had been sitting at
the left margin, rendering as a paragraph detached from the rule it narrows — became a
sub-bullet. That is a **deletion**, the second exception to this unit's additive constraint
after 030's flake-policy replacement, and it is recorded for the same reason: the constraint
is only meaningful if departures from it are named.

A scan of the other seven files that merge touched found no further duplicates.

The near-miss worth keeping: the first verification of this claim searched for `split-hero`
case-sensitively, found zero, and appeared to show the line had been lost outright. The
text says `Split-hero`. A case-sensitive grep is how you conclude that content is missing
when it is actually duplicated — the opposite error, from the same one-character cause.

**`asset-requirements.md`** — 80 lines locally, 585 after. The upstream version was written
against one specific image-generation tool; generalizing it into capability terms is most of
the growth. A reader without that tool now gets the concept, the prompt discipline, the
selection criteria, and the parallelism guidance, rather than a command they cannot run.

## The neutrality failure this phase caused, and the gate that now catches it

The `ima2` tool name leaked into six places through this merge and the 010 capture. It is a
legitimate name in cli-jaw's ecosystem, which is why it did not look wrong while porting —
but this repository is the agent-neutral publication, so it does not belong here.

Neutralized, and `gap-census.sh`'s token list was extended to include it so the same leak
fails the gate next time. That is the useful outcome: the leak was found by reading, and
the fix was to make reading unnecessary.

## Verification

- Census gap 0 for both skills.
- Neutrality scan clean, with `ima2` now in the token list.
- The three `anti-slop.md` locals confirmed present by name after the merge, not inferred
  from the diff being small.
