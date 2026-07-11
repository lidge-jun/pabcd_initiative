# Korean Hero / Large-Display Typography Port

**Date**: 2026-07-08
**Kind**: SoT reinforcement + downstream port (dev-frontend korea-2026.md + anti-slop.md)

## Trigger

User flagged that oversized bold Korean heroes read as slop specifically in
Hangul (shown on the GYEOL studio mockup: `clamp(..., 10rem)` / weight 700 /
`line-height: 0.9`). Two GPT-5.5 explorers researched how Toss and other premium
Korean services handle hero typography, with Tier-2 proof (one lane measured
live pages via Playwright computed style).

## Finding (Tier-2, measured 2026-07-08)

Premium Korean services size Korean heroes ~`56-72px` desktop / ~`26-40px`
mobile, weight `700` (not `900`), line-height `1.25-1.4` (not `0.9`), with
`word-break: keep-all` and manual phrase breaks. `900` shows up on English
display / short brand phrases, not long Hangul. Huge bold Hangul reads as a
heavy graphic mass because each syllable is a dense square block with little
ascender/descender rhythm (Typotheque, Morisawa). Measured: Toss home
66px/700/lh1.4, Toss team 72px/700/lh1.3, Daangn 64px/700/lh1.31, Kakao
70px/700/lh1.27, Woowa Korean 40px/700 (its 900 is English), Naver 32px/600,
Musinsa 20px/600.

## Port status

| Target | Files | Status |
| --- | --- | --- |
| SoT | `pabcd_initiative/.../korea-2026.md`, `anti-slop.md` | Done — added "Korean Hero / Large Display Type" subsection + slop signal |
| cli-jaw | `cli-jaw-skills/.../korea-2026.md`, `anti-slop.md` | Done — same block (Korean-hero block diff-matches SoT) |
| codexclaw | `codexclaw/plugins/codexclaw/skills/dev-frontend/.../korea-2026.md`, `anti-slop.md` | Done — same block |
| jawcode | — | N/A (no dev-frontend skill) |

Note: korea-2026.md and anti-slop.md were already divergent between SoT and
cli-jaw before this change, so the port adds the SAME new block to each rather
than byte-syncing whole files. The new Korean-hero block is diff-identical
across SoT and cli-jaw.

## Demonstration

The GYEOL studio hero was refixed to the restrained pattern (verified via
Playwright computed style): desktop `74.9px / 700 / line-height 1.16 / keep-all`,
mobile `33.6px / 700 / lh 1.16`, down from `~160px / 700 / lh 0.9`. The hero now
leans on whitespace + imagery + supporting copy instead of a giant Hangul wall.

## Sources

Live pages: toss.im, toss.im/team, toss.im/tossface, about.daangn.com,
kakaocorp.com, woowahan.com, navercorp.com, musinsa.com, dive.hyundaicard.com.
Type: Typotheque CJK typesetting, Morisawa Hangeul guide, W3C KLREQ, MDN
word-break/line-break, Pretendard / Wanted Sans / Spoqa / Sandoll (Toss Product
Sans) docs.
