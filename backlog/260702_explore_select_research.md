# Explore-and-Select Loop — Research Results (2026-07-02)

Appendix to `260702_loop_engineering_backlog.md` §2 (the plateau finding). Five research
lanes returned; this doc records the proposed rule, the design skeleton, and the source
map. Lanes: ChatGPT 5.5 Pro (session continuation), 3× gpt-5.3-codex-spark literature
sweeps, LazyCodex/OmO-harnessed gpt-5.5 (team-topology question).

## 1. Proposed rule (ChatGPT Pro) — LOOP-EXPLORE-SELECT-01

Candidate rule text for a future dev-pabcd revision (currently referenced from §11.4 as
a pointer; full adoption pending a normal PABCD pass):

```text
DEFAULT (LOOP-EXPLORE-SELECT-01):
When LOOP-ARCHETYPE-01 classifies a work-phase as Open-ended optimization
and PLATEAU fires, do not run another same-class C→B repair. Start a new
Explore-and-Select PABCD work-phase.

P defines: strategic descriptors, telemetry, candidate budget, archive,
opponent portfolio, evaluator cascade, selection rule, and terminal states.
A audits the loop design and verifier, not only the code plan.
B generates a bounded population of StrategyCard+patch candidates, evaluates
them on paired instances, admits them to a strategic-diversity archive, and
promotes only robust finalists.
C revalidates the selected best-so-far against the fixed verifier, regression
sentinels, timing, and allowed-surface constraints.
D reports DONE only if the objective threshold is met; otherwise report
BUDGET_EXHAUSTED with best-so-far, archive evidence, loss signatures, and the
next exploration direction.
```

Key design elements (full pseudocode in the ChatGPT session,
https://chatgpt.com/c/6a466d08-a268-83ee-a628-428205a8bd36):

- **Unit of evolution = StrategyCard + bounded patch**, never "threshold ±5". The
  candidate carries archetype, opponent model, strategic hypothesis, expected replay
  signature, predicted vs measured behavior descriptors, and a death log entry.
- **Two-layer diversity**: idea diversity (StrategyCards, EoH-style thoughts) ×
  behavior diversity (replay-measured descriptors). A candidate whose measured behavior
  contradicts its claimed strategy is re-archived by measurement or killed.
- **MAP-Elites-style archive** keyed by strategic descriptors (pressure_timing,
  economy_posture, map_control, primary_win_plan, opponent_model, map_size_plan) — not
  one leaderboard.
- **PSRO-lite opponent portfolio**: fixed opponents + incumbent + 2-4 frozen elites +
  1-3 hand-written exploiters/probes stressing one weakness each.
- **Hyperband-style evaluation cascade**: stage0 validity → stage1 cheap target slice
  (+ rush-regression sentinels) → stage2 archive admission → stage3 full tournament for
  top-K only. Novelty is an exploration criterion, never a deployment criterion.
- **Plateau = 2+ of**: score_plateau, archive_plateau, loss_signature_plateau,
  death_class_plateau (native §10), anchor_plateau (native §10), budget_plateau.
- **Restart ladder**: soft (sample from underfilled cells) → strategic (regenerate from
  replay telemetry) → island (reset worst island) → PSRO (change opponent mix / add
  exploiter) → evaluator (add telemetry — mandatory first step for NEXT NATION, whose
  verifier only says "losing") → PABCD (back to P/Interview).

## 2. Team-topology verdict (LazyCodex lane, gpt-5.5)

Committee (co-writing, consensus) does NOT attack the plateau — it accelerates
convergence around the incumbent concept; population/league DOES. Division of labor:
committee for review/postmortem/invariants, population for strategy generation, **solo
builder for final integration** (the author's B-phase distrust survives). Diversity must
be mechanical: archetype-pinned prompts with *different objectives per archetype*,
isolated contexts/worktrees, behavior-descriptor novelty gates, deterministic promotion
("do not let agents vote"). Supporting evidence: multi-agent debate does not reliably
beat single agents while model heterogeneity helps (https://arxiv.org/abs/2502.08788);
LLM conformity to majority answers (https://arxiv.org/abs/2410.12428).

## 3. Literature map (spark lanes, condensed)

### LLM-guided evolutionary/program search
- FunSearch — program evolution + external evaluator, island diversity:
  https://www.nature.com/articles/s41586-023-06924-6
- AlphaEvolve — evolvable code blocks, elite archive:
  https://arxiv.org/abs/2506.13131
- EoH — evolve NL "thoughts" + code together: https://arxiv.org/abs/2401.02051
- EoH-S — complementary heuristic *set* (portfolio vs one generic policy):
  https://arxiv.org/abs/2508.03082
- MAP-Elites — quality-diversity archive: https://arxiv.org/abs/1504.04909
- Novelty search (abandoning objectives): https://doi.org/10.1162/EVCO_a_00025

### Self-play / population / opponent modeling
- PSRO original (unified game-theoretic MARL): https://arxiv.org/abs/1711.00832
- PSRO survey (strategy exploration as core difficulty):
  https://arxiv.org/abs/2403.02227
- AlphaStar league + exploiters: https://www.nature.com/articles/s41586-019-1724-z
- TStarBot-X — league training at low compute: https://arxiv.org/abs/2011.13729
- PBT (population-based training): https://arxiv.org/abs/1711.09846
- Meta-game evaluation (seed/map cross-play + bootstrap — directly addresses the
  5-seed × 3-map selection bias): https://arxiv.org/abs/2405.00243

### Plateau detection / restart & exploration scheduling
- Hyperband (successive-halving budgets): https://arxiv.org/abs/1603.06560
- Stagnation detection in EAs (raise step size on non-improvement):
  https://arxiv.org/abs/2004.03266
- Bandit multi-start control for local search: https://arxiv.org/abs/1401.3894
- GP-Hedge portfolio allocation: https://arxiv.org/abs/1009.5419
- MAB restart/reset in CDCL SAT: https://arxiv.org/abs/2404.03753 (+ cold restarts:
  https://arxiv.org/abs/2404.16387)
- ME-MAP-Elites (bandit over emitters — widen vs deepen decision):
  https://arxiv.org/abs/2007.05352
- Dominated Novelty Search: https://arxiv.org/abs/2502.00593
- Reflexion (+ known limits): https://arxiv.org/abs/2303.11366 · Self-Refine:
  https://arxiv.org/abs/2303.17651 · Agent-R (loop-break recovery):
  https://arxiv.org/abs/2501.11425

### Verification caveats
- Two spark-sourced future-dated arXiv IDs are UNVERIFIED — spot-check before citing:
  https://arxiv.org/abs/2605.28273 (Global PSRO / population exploitability),
  https://arxiv.org/abs/2602.16928 (LLM-discovered MARL algorithms).
- Spark lane 1 occasionally framed the case as the game of Go rather than a Go-language
  bot; method mappings remain valid, wording does not.

## 4. Operational counters (lane-3 synthesis)

Keep two counters per candidate lineage: `no_progress_at_gate` and
`same_reason_repeats`. Reward depth-first continuation while improving; enforce
controlled diversification when failure signatures converge. This is the quantitative
backing for §10 LOOP-PHASE-DEATH-01's N=3 starting value.
