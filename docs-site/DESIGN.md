---
name: pabcd-initiative-docs-site
colors:
  primary: "#111111"
  accent: "#e63312"
  background: "#fbfbf9"
typography:
  heading: { fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif", fontSize: "clamp(4rem, 16vw, 15rem)" }
  body: { fontFamily: "Pretendard Variable, Pretendard, -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif", fontSize: "1.0625rem" }
---

# PABCD Initiative docs-site — design lock v2 (element-ledger synthesis)

Reading this as: a methodology documentation hub for engineers running agentic
coding loops, in a Swiss international typographic voice — a printed spec sheet,
type-led, grid-visible, one vermilion accent.

Dials: DESIGN_VARIANCE 6 / MOTION_INTENSITY 3 / density D2 (index) / D3 (doc pages).

**v2 note (user steering, recorded in goalplan ledger):** round-1 HOTL auto-pick
was r1_01 editorial field-manual; the user selected r1_03 Swiss typographic
("이게 젤좋아"). Round 2 was re-run `--ref` r1_03 (r2_09, r2_10). The r1_01-anchored
r2_06..r2_08 renders remain archived as concept provenance only.

## Element ledger (per-token source variant)

Concept renders: `codexclaw/devlog/_plan/260711_dispatch_economy_docs_site/assets/concepts/`
(r1_01..r1_05 round 1; r2_06..r2_08 round 2a ref=r1_01, superseded; r2_09..r2_10
round 2b ref=r1_03, production).

| Token | Value | Source variant | Why |
| --- | --- | --- | --- |
| ism | Swiss international typographic | r1_03 (user-selected winner) | stacked mega-grotesk "PA / BCD" masthead, modular grid, single vermilion square; documentation-hub meta bar built in |
| paper bg | #fbfbf9 + faint modular grid + registration marks | r2_09 (production full-bleed hero bg, -q high) | mostly-empty negative space purpose-built to sit behind live HTML type; satisfies generated-bitmap full-bleed hero without bitmap text |
| ink | #111 (off-black) | r1_03 | pure #000 banned (depth) |
| accent | #e63312 vermilion, square motif + rare emphasis | r1_03 | one solid square + numbered-index accents; max 1 accent discipline |
| masthead | stacked "PA" / "BCD" tight heavy grotesk, "Initiative" small beside | r1_03 | wordmark-as-headline; LIVE HTML TYPE (crisper than bitmap; render text unreliable) |
| right-column figure | five horizontal state bars P/A/B/C/D with axis, gantt-like sequence offsets | r1_03 | rebuilt as honest HTML/CSS sequence figure with CORRECTED semantics: Plan/Audit/Build/Check/Done (render said Analyze/Consolidate/Deploy — bitmap semantic drift corrected) |
| top meta bar | thin mono small-caps strip: brand / description / hub / version / date | r1_03 | doc-hub chrome |
| next-section hint | numbered 01..06 column strip at hero bottom edge | r1_03 footer strip | doubles as primary nav to doc pages; visible in first viewport |
| section divider art | letterpress PA·BCD print-detail photograph | r2_10 | real print texture beats CSS decoration; used once on index |
| reference table | 5-row methodology state table | r1_02 idea (retained from round 2a synthesis) | entry/exit/gate columns fit doc-hub density |
| rejected | r1_01/r1_04 editorial-manual base (superseded by steering), r1_05 (P gear missing, brown one-note risk), r1_02 as base (console vibe) | — | recorded |

Motion: feedback baseline + ONE scroll reveal on index sections (MOTION 3);
`prefers-reduced-motion` honored. No parallax.

Fonts: Archivo (Google Fonts, 500-900) for Latin display, Pretendard variable via
jsDelivr for Korean body, both `font-display: swap`, system CJK fallback for
offline `file://`. Mono = `ui-monospace` system stack.
