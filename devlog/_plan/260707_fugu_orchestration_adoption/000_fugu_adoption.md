# 260707 Fugu Orchestration Adoption

Source: Sakana Fugu Technical Report, arXiv:2606.21228v1 (2026-06-19). Learned
orchestrator models (Fugu = hidden-state single-worker router; Fugu-Ultra =
Conductor-style GRPO-trained workflow generator) over a frontier worker pool
(GPT-5.5, Opus 4.8, Gemini 3.1). Analysis method: two parallel gpt-5.5 subagent
reads (technical deep-dive + PABCD transfer mapping, artifacts at
`/tmp/arxiv2606/analysis_technical.md` and
`/tmp/arxiv2606/analysis_pabcd_transfer.md`) cross-checked by a direct main-agent
read of the full paper text.

## Why these mechanisms transfer

Fugu's value is trained routing, which a static skill cannot replicate. What DOES
transfer is what its trained orchestrators converged on behaviorally — the paper
documents the converged policies with concrete incidents:

- **Intra-workflow isolation via access lists** (paper §3.2.2): without isolation,
  the first agent to touch the environment "sets the trajectory for all future
  agents" — they name it orchestration collapse. Access lists make peer-output
  visibility an explicit, per-dispatch decision; cross-workflow shared memory stays
  on so lanes do not re-discover artifacts.
- **Crux-matched aggregation** (paper §4.4): tree topologies picked the aggregator
  by the disputed domain (Gemini for trivia synthesis, GPT for a spectral-number
  derivation) and the paper argues fixed-aggregator systems are capped at the
  aggregator's own ceiling.
- **Cross-model builder/verifier alternation** (paper §4.4): GPT-as-builder with
  Opus dispatched at critical debugging moments; a clean-slate GPT pass broke an
  Opus dead-end on a SWE Bench Pro OTP bug (root cause was client-side concurrency,
  not the server path Opus tunneled into). Different model families decorrelate
  blind spots.
- **Specialist first-principles re-derivation** (paper §4.4 FEAL differential
  cryptanalysis): after Opus built the attack, GPT was tasked as a math specialist
  to re-derive the differential constant bit-by-bit before adoption.
- **Late-stage fan-out gains** (paper §4.3.1 AutoResearch, 123 experiments x 3
  seeds): orchestration was "competitive early... pulls ahead after mid-training,"
  i.e. once coarse configuration search shifted to fine optimizer/schedule tuning;
  it also reduced cross-seed variance.

## Adopted rules

| Rule | Tag | Placement |
|------|-----|-----------|
| DISPATCH-ISOLATION-01 | DEFAULT | dev-pabcd §7.1 (canonical, cli-jaw); codexclaw Delegation Model |
| SPECIALIST-CRUX-01 | HEURISTIC | same |
| REVIEW-DECORRELATE-01 | HEURISTIC | same |
| LOOP-FANOUT-TIMING-01 | HEURISTIC | §10 Optimization-Loop Meta-Rules (all three) |
| COLLAPSE-AGGREGATOR-01 | DEFAULT | §11.9 (canonical bullet, cli-jaw section); codexclaw Meta-Rules |

Single-source induction caveat: all five rules are grounded in one vendor report
whose qualitative examples are curated. Tags were chosen accordingly (three
HEURISTIC, two DEFAULT where the paper gives a mechanism-level failure mode:
orchestration collapse, fixed-aggregator ceiling). Revise when a second domain's
evidence contradicts them.

## Explicitly NOT adopted

- Hidden-state routing head, soft-label SFT routing, sep-CMA-ES, GRPO Conductor:
  require trained models and reward infrastructure; no static analogue.
- Model-brand role bindings ("GPT builds, Opus debugs, Gemini aggregates"): roles
  come from current observed capability evidence, never hard-coded brands.
- Single-interface abstraction hiding orchestration: PABCD's value is visible
  phase discipline and attested evidence; hiding the process would invert it.
- Workflow depth cap (<=5 steps) and quality/latency mode split: already covered
  by DIVERGE-TIER-01 and C0-C5 class scaling.

## Patch map (2026-07-07)

- `pabcd_initiative/skills/dev-pabcd/SKILL.md` — new §7.1, §10 bullet, §11.9
  bullet; README hardening line.
- `cli-jaw/skills_ref/dev-pabcd/SKILL.md` — new §7.1 (generalizes §11.8 star
  topology to all parallel dispatch), §10 bullet, new §11.9 section.
- `codexclaw/plugins/codexclaw/skills/pabcd/SKILL.md` — three Delegation Model
  bullets, two Optimization-Loop Meta-Rules bullets; record at codexclaw devlog
  `260707_fugu_orchestration_adoption/000_record.md`.

## Follow-ups

- jawcode port: no dev-pabcd doc there; fold the five rules into
  `packages/coding-agent/src/defaults/jwc/skills/{team,plan,goal}` phrasing.
- `references/loop-engineering.md` (canonical + codexclaw): sync §11.9 and the
  fan-out timing rule into the full-rules reference on its next touch.
- cxc-loop skill (codexclaw): mirror COLLAPSE-AGGREGATOR-01 into its
  divergence/collapse section on next touch.
