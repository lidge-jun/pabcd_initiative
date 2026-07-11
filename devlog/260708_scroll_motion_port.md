# Scroll-Driven Motion Knowledge Port

**Date**: 2026-07-08
**Kind**: SoT expansion + downstream port (dev-frontend/motion.md)

## What

`dev-frontend/references/core/motion.md` gained a scroll-driven effects
expansion, validated by building and auditing a real cinematic studio landing
(GYEOL) plus two research passes (5-lane + 2-lane GPT-5.5 explorer surveys,
source-proofed). New content:

- Scroll-Driven subsections: CSS scroll-driven animations, horizontal
  scroll-in-vertical, sticky card stacking, frame sequence scrolltelling,
  video `currentTime` scrub, slide/page transitions, text mask & reveal,
  SVG path drawing, Lottie scroll scrub.
- Cinematic Section Transitions (zoom-through/portal, 3D fly-through,
  crossfade/scale-depth, card-to-fullscreen, wipe, pinned timeline).
- Scroll Pattern Decision Tree.
- Frame Sequence Format Guide (WebP/AVIF/JPEG).
- `prefers-reduced-motion`: added the JS SHORT-CIRCUIT rule — CSS overrides
  alone are insufficient; the script must skip building frame arrays, binding
  listeners, and running the update loop, and render a static end state. This
  rule came from an independent audit (reviewer on a different model family)
  of the GYEOL build, where reduced-motion CSS existed but the JS still built
  160 offscreen frames and bound scroll handlers (REVIEW-DECORRELATE-01 catch).

## Port status (SoT-then-port; ports adapted, never blind-copied)

| Target | Path | Status |
| --- | --- | --- |
| SoT | `pabcd_initiative/skills/dev-frontend/references/core/motion.md` | Done, agent-neutral (no host-CLI; generic "image-generation tool" / "text-to-video model"; ffmpeg kept as standard) |
| cli-jaw | `cli-jaw-skills/dev-frontend/references/core/motion.md` (deployed via `cli-jaw/skills_ref` submodule) | Done, kept in sync with SoT |
| codexclaw | `codexclaw/plugins/codexclaw/skills/dev-frontend/references/core/motion.md` | Done (cxc-flavored: scroll+cinematic already present from prior turns; added the reduced-motion JS rule) |
| jawcode | `jawcode/packages/coding-agent/src/defaults/jwc/skills` | N/A — no dev-frontend skill exists (role skills only: browse/goal/jaw-interview/plan/search/team). Frontend-motion port not applicable; nothing created. |

## Agent-neutrality

SoT + cli-jaw carry zero host-CLI commands (`grep -c 'ima2\|cxc ' == 0`). The
codexclaw copy keeps its cxc-flavored research pointers. `ffmpeg` remains in all
copies as a standard, non-host tool.

## Verification

- SoT: 164 -> 415 lines; code fences even (48); diff shows additions only.
- cli-jaw: byte-identical to SoT after port.
- codexclaw: reduced-motion JS rule added; existing scroll/cinematic sections
  untouched.
- Source research: codexclaw `devlog/_plan/260708_scroll_driven_effects/`
  (`000_research.md`, `001_cinematic_transitions.md`).
