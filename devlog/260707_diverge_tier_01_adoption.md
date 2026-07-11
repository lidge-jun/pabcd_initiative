# DIVERGE-TIER-01 Adoption — Divergence Cost Tiers (2026-07-07)

## What

New §11.8 "Divergence cost tiers (DEFAULT, DIVERGE-TIER-01)" added to
`skills/dev-pabcd/references/loop-engineering.md` (full text) with a summary
bullet in the `skills/dev-pabcd/SKILL.md` §11 router. Router-resident §11.6/§11.7
got stub headers in the reference file so the "canonical full text" claim stays
honest.

## Why

Owner interview (codexclaw, 2026-07-07): with near-unlimited subagents the old
implicit assumption "subagents are expensive, dispatch sparingly" breaks, but the
binding constraint becomes wall-clock + collapse-owner triage attention. The
owner rejected a 3-round agent-roundtable design as cost-inflated; the adopted
shape is conceptual-first divergence with a rare, criteria-gated implementation
spike. Distilled from the Fable field-guide unknown-discovery practices
(conceptual prototypes, blindspot passes) without importing model-specific
behavior.

## Genealogy / evidence

- Interview + A-gate audit: codexclaw
  `devlog/_plan/260707_harness_divergence_interview/000_interview_record.md`,
  `010_plan.md`, `011_audit_synthesis.md` (5 reviewer findings accepted; the
  Tier-1 gate was tightened to include per-candidate provenance so §11.8 never
  relaxes §11.7).
- Fable research: codexclaw `devlog/_plan/260707_thariq_fable_youtube_plugin_research/`
  and `260707_codex_rs_native_tooling_research/200_fable_loop_adoption.md`.

## Ports

Same rule id, runtime-adapted wording, shipped in the same pass:

- cli-jaw `skills_ref/dev-pabcd/SKILL.md` — inline §11.8 after §11.7 (Boss =
  collapse owner, dispatch employees = explorers).
- jawcode `packages/coding-agent/src/prompts/jaw/orchestrate-p.md` — compact tier
  clause in the loop-spec header divergence bullet.
- codexclaw `plugins/codexclaw/skills/loop/SKILL.md` — tier bullets in the
  Emergence/Divergence layer (explorer subagents author Tier-1 docs; minds stay
  interview-time contradiction lenses; front-matter lives in the candidate doc,
  the divergence CLI records the archive row alongside).
