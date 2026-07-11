# Design Grammar Port: Hero Composition, Serif Renaissance, KR Serif, OpenAI Grammar

**Date**: 2026-07-09
**Kind**: SoT reinforcement + downstream port (dev-frontend), 4 PABCD work-phases
**Research**: codexclaw `devlog/_plan/260709_design_grammar_research/` (000 + 001),
5 GPT-5.5 explorers, Tier-2 opened sources + live computed-style measurements.

## What changed (identical blocks in SoT, codexclaw, cli-jaw-skills)

| WP | File | Addition |
| --- | --- | --- |
| 1 | layout-discipline.md | `## Hero Composition Grammar (verified 2026-07-09)` — split hero (left bold + right boxed mockup) demoted to paid-conversion-LP-only; replacement menu: centered-stacked-over-media, product-as-stage, editorial opener, evolved split w/ canvas, full-bleed consumer hero. Product visual = stage, never a right-column card. |
| 1 | anti-slop.md | Split-hero template tell (Stripe->Linear exhausted lineage). |
| 2 | aesthetics.md | `### Serif Discipline (verified 2026-07-09)` rewrite — domain-gated three-role system (display serif LIGHT 330-400 + sans UI + mono accent); AI/editorial/trust lane legitimate; dashboard ban + Fraunces/Instrument ban kept; counter-cases (Runway/Attio/Mistral) recorded. |
| 2 | anti-slop.md | "tasteslop" serif-shortcut tell (WIRED 2026-06-05). |
| 3 | korea-2026.md | `### Korean Serif / Myeongjo Display (verified 2026-07-09)` — MaruBuri/Noto Serif KR/Nanum/Chosun ranking, myeongjo display + Pretendard UI pairing, explicit no-KR-AI-wave disclaimer. |
| 4 | aesthetics.md | `### Expressive vs Functional Layers` + `### AI-Brand Grammar Vocabulary` (OpenAI in-house Feb-2025 + ABC Dinamo + Studio Dumbar; Anthropic by Geist; DeepMind by MultiAdaptor/Colophon). |
| 4 | motion.md | `## Soft-Focus Organic Background + Capsule Label (Level 5+)` + `## Product-Led Hero Motion (Level 6+)`. |
| 4 | asset-requirements.md | `## Mockup Production Pipeline` (Rotato-class tools; AI scene + real screenshot compositing; real-UI-pixels rule). |

jawcode: N/A (no dev-frontend skill family).

## Addendum (same day): SKILL.md layer + dev-uiux-design reflection

| WP | File | Addition |
| --- | --- | --- |
| 5 | dev-uiux-design/references/design-isms.md | Two new isms: `AI Serif Editorial` (three-role serif system, tasteslop gate) + `Organic Capsule` (OpenAI announcement grammar, layer split). Numbering adapted: codexclaw 1.14/1.15, SoT/cli-jaw 2.12/2.13. |
| 5 | dev-uiux-design/references/product-personalities.md | `OpenAI (2026 warm-sans organic)` + `Anthropic / Claude (serif bookish)` DNA profiles. |
| 6 | dev-uiux-design/SKILL.md | Ism/profile row counts updated; UX-TYPE-01 typography stance extended with the three-role serif system (added as a new stance bullet in SoT/cli-jaw, which lacked the line); MaruBuri Korean-serif-display bullet in Font Selection. |
| 6 | dev-frontend/SKILL.md | Hero-composition bullet in §5 Anti-Slop; 5 Modular References rows extended (layout-discipline, aesthetics, korea-2026, motion, asset-requirements). |

Noted gap (out of scope, not fixed here): SoT/cli-jaw dev-uiux-design lag
codexclaw — no Liquid Glass ism (1.12), no Liquid Editorial kit (1.13), no
Aside profile, no UX-DEFAULT-ISM-01 section; their design-isms use a 2.x
numbering scheme. A separate backfill port would be needed to converge them.

## Convergence addendum (same day): gap CLOSED

The backfill port ran as a 2-work-phase PABCD loop:

- **References**: design-isms.md, color-system.md, product-personalities.md,
  typography-line-breaks.md, design-read-example.md (newly created in cli-jaw),
  ux-states.md byte-synced codexclaw -> SoT + cli-jaw (all six now
  byte-identical x3; source files carry zero tool-specific mentions).
  Pre-overwrite reverse-drift checks found only numbering/header variants
  (2.x->1.x isms, 7-12->1-6 ux-states, "The Problem" rename) — no substantive
  downstream content lost.
- **SKILL.md (section-additive, wholesale copy avoided)**: SoT gained
  UX-DEFAULT-ISM-01 (No-Brief Default Direction) + the step-3 expressive-surface
  pointer; cli-jaw gained Lazy-User Gate (UX-LAZY-01), UX State Contract
  (UX-STATE-01), IA Chooser (UX-IA-01), UX-DEFAULT-ISM-01, and the UX-INTENT-01
  compact ambiguity flow (its old 6-question Socratic intro was replaced; the
  old Rules bullets survive inside "Optional deepening" except the "max 6
  questions" cap, superseded by the ONE-fork rule). Ism/profile rows updated to
  true counts (15 / 10). codexclaw's Native-tool-support paragraph and
  frontmatter were deliberately NOT ported (agent-neutral).

Remaining known drift: minor wording differences in shared SKILL.md prose
(SoT keeps its richer Lazy-User phrasing; codexclaw keeps tool-specific
paragraphs). Capability level is now equal across the three repos.

## dev-frontend convergence addendum (same day)

3-work-phase PABCD loop, criterion = capability parity (not byte parity where
structure deliberately differs):

- **WP1 backfill/syncs**: color-system.md + liquid-glass.md added to SoT+cli-jaw;
  preflight-full.md added to cli-jaw; theme-switching, examples/README,
  layout-discipline, mobile-native synced to the newest variant (reviewer caught
  two same-line-count SoT drifts: stale RN 0.84 content, old Bento phrasing);
  scripts/README direction REVERSED after diff proof — SoT's §12-aligned version
  was newest and now lives in all three.
- **WP2 forward ports**: typography-wrapping + anti-slop byte-synced x3 (SoT's 16
  unique anti-slop lines verified as phrasing variants whose substance exists in
  the codexclaw version); motion.md full-synced (892L) with downstream-only
  neutralizations — generic image-gen/image-to-video wording replaces the ima2
  example, and codexclaw-local devlog paths became descriptive attributions.
- **WP3 reverse ports + SKILL.md parity**: SoT's korea-2026 "Verified 2026
  Additions" block ported to codexclaw+cli-jaw (korea-2026 now byte-identical
  x3); react/perf moved-content ports to cli-jaw judged N/A (equivalent inline
  sections exist); discoverability rows for color-system/liquid-glass added to
  SoT+cli-jaw SKILL.md and preflight-full row to cli-jaw.

Accepted structural residuals: SoT SKILL.md keeps its 2026-07-02 refactor
(§8-10 consolidated into "React Behavior Rules", §6 connection budgets moved to
performance-budget.md) while codexclaw/cli-jaw keep the inline layout; motion.md
downstream copies differ from codexclaw only by the two neutralized spots.

## Review trail

- WP1: reviewer Curie (gpt-5.4) FAIL->fix->PASS (contradiction between paid-LP
  exception and absolute rule — rule rescoped "Outside the paid-LP exception
  above"; scope-creep suspicion rebutted with git evidence: Hangul bullet was a
  pre-existing uncommitted 260708 port line).
- WP2, WP3: Curie PASS, no blockers.
- WP4 final gate: FRESH reviewer Hypatia (gpt-5.4) FAIL->fix->PASS (cross-ref
  renamed to the exact heading `Frame Sequence Format Guide`); brand
  attributions fact-checked against opened sources.
- All WPs: blocks byte-identical across the 3 repos, insertions-only diffs
  (rewrites accounted), code-fence parity.

## Key sources

Wallpaper/Fast Company/Creative Review (OpenAI Feb-2025 rebrand), studiodumbar.com,
geist.co/work/anthropic, multiadaptor.com + colophon-foundry.org (DeepMind),
WIRED "AI Has Come for Serif Fonts" (2026-06-05), live computed styles claude.ai /
medium.com / manus.im / runwayml.com / attio.com / mistral.ai (2026-07-09),
LogRocket "Linear Design" (2026-02-03), Nordcraft, Rectangle "Linear effect",
live hero inspections of 11 sites (2026-07-09), hangeul.naver.com MaruBuri,
notofonts/noto-cjk, Apple Newsroom Liquid Glass (2025-06-09), WWDC25 session 356.
