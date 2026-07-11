# Opaque-Surface Gradient Discipline Port

**Date**: 2026-07-09
**Kind**: SoT reinforcement + downstream port (dev-frontend anti-slop.md + color-system.md)

## Trigger

User flagged the opencodex GUI "Account login" panel (`.panel-accent`,
`opencodex/gui/src/styles.css:175`) as tacky: a purple-tinted
`linear-gradient(accent-soft -> transparent)` wash over an opaque functional
panel. Three parallel GPT-5.5 explorer lanes researched why this reads dated and
what premium systems do instead (one lane died on a proxy stream disconnect and
was respawned as a slim Korean-services lane with live Playwright DOM
measurements).

## Finding (Tier-2)

Gradients survive on ambient/expressive/translucent/media surfaces; on opaque
functional surfaces (cards, panels, sidebars, badges, task UI) the premium
2025-2026 direction is flat: semantic tint tokens (Primer
`--bgColor-accent-muted`, Radix accent steps 3-5, shadcn flat `--accent`),
border/ring emphasis (Geist, Tailwind), left/top accent bar (Stripe Apps),
elevation tokens (Primer), or semantic status roles (Atlassian). Korean premium
services (Toss/Kakao/Naver/Channel Talk/Daangn, live-measured) match: flat
tint/border on functional panels, gradients only in heroes/illustrations.

## Port status

| Target | Files | Status |
| --- | --- | --- |
| codexclaw | dev-frontend anti-slop.md (FE-GRADIENT-02 + rescoped "empty flat sections" line), color-system.md (FE-COLOR-ACCENT-SURFACE-01) | Done |
| SoT (pabcd_initiative) | same two files | Done — byte-identical to codexclaw |
| cli-jaw (cli-jaw-skills) | same two files | Done — byte-identical |
| jawcode | — | N/A (no dev-frontend skill family) |
| dev-uiux-design (all repos) | — | N/A this round: the finding is CSS surface-treatment level (token/fill discipline), owned by dev-frontend; no ism/profile change warranted |

All three copies remain agent-neutral (`rg 'ima2|imagegen|view_image|browser:control|cxc-'` = 0
on SoT/cli-jaw). Both files were byte-identical across repos before the edit, so
the port is a whole-file byte-sync, no divergence handling needed.

## Conflict resolved

anti-slop.md previously said "Empty flat sections with no depth -> add
background imagery, patterns, or gradients", which contradicted the new rule on
opaque functional panels. The line is now scoped to marketing/ambient surfaces
with a pointer to FE-GRADIENT-02.

## Demonstration

opencodex GUI `.panel-accent` refit to flat tint + existing border (gradient
wash removed) — recorded in codexclaw devlog
`devlog/_plan/260709_opaque_gradient_discipline/` (000 research, 001 Korean
field measurements).
