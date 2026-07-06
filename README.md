# PABCD Initiative

Canonical home for the PABCD development methodology: the FSM-driven workflow
(PABCD state machine + attestation), the dev skill family that catches LLM
detail-misses, and the modular router+references architecture.

- `skills/` — the 13-skill dev family, snapshotted from `cli-jaw/skills_ref` at the
  2026-07-02 75-grade upgrade (router diets, sourced 2026 currency, freshness
  stamps, AI-era gates), then made **agent-neutral**: no host-CLI commands —
  Hardened 2026-07-05 (`devlog/_plan/260705_difflevel_roadmap_default/`, ported to
  cli-jaw/codexclaw/jawcode): de-branded ("Jawdev" removed; the routine is anonymous
  rules, not an opt-in style) and five rules added — DIFFLEVEL-ROADMAP-01 (multi-phase
  ⇒ first P writes every phase doc to diff-level), PHASE-SPLIT-01 (dependency-order
  phases; effort bucketing forbidden), LEXICO-SPLIT-01 (numbered docs; research ≠
  implementation design), UNIT-RESIDENCE-01 (all work lives in a unit; C0-C1 leaves a
  numbered record doc), SOT-SYNC-01 (find general SoT docs first; patch them in the
  same unit at C; recommend creating one if absent).
  Hardened 2026-07-06 (activation-evidence pack, from the NEXT NATION dead-branch
  incident + 4-lane external research; see codexclaw devlog
  `260706_loop_mechanism_research`): C-ACTIVATION-GROUNDING-01 (conditional paths
  need trigger+observe evidence at C; P names activation scenarios; A checks trigger
  reachability), LOOP-MECHANISM-PROOF-01 / LOOP-RESIDUAL-TRACE-01 /
  LOOP-PEER-CONTRAST-01 (optimization-loop specializations), and dev-testing
  GATE-HOLDOUT-LEAKAGE-01 / GATE-AGREEMENT-STATS-01.
  `orchestrate <phase>` maps to whatever FSM/delegation surface the runtime has
  (or heuristic worklog attestations when none exists; see the Runtime adapter
  note in `skills/dev-pabcd/SKILL.md`). This is a COPY — cli-jaw's `skills_ref`
  submodule remains its own live deploy source.
- `prompts/freshness-sweep.md` — cron prompt for the recurring multi-cycle PABCD
  freshness sweep (re-verify time-sensitive claims, patch, independently verify,
  emit downstream port backlog).
- `backlog/` — adoption/backlog records; `260702_loop_engineering_backlog.md` holds the
  loop-engineering alignment (dev-pabcd §11), the plateau finding, and the future-work
  table (server-side doom-loop gate, evidence-bound attestation, explore-and-select
  tooling, downstream ports).

Downstream adaptations of the same principles: `codexclaw/plugins/codexclaw/skills`
(cxc-* family) and `jawcode/packages/coding-agent/src/defaults/jwc/skills` (+ role
agent prompts). Ports are adapted, never blind-copied.

Shared capabilities carry the same SoT-then-port line. `repo-map` (a ranked structure
map: tree-sitter tags + PageRank, on-demand, run before deep grep) has its contract in
`skills/dev-pabcd/references/repo-map-capability.md`, shipped in codexclaw (`cxc map`,
reference impl) and planned for cli-jaw (`cli-jaw map`) and jawcode (`jwc map`, native on
pi-ast). See `devlog/_plan/260706_repomap_native_ports/`.

Method background: cli-jaw `devlog/_plan/260702_dev_skills_75_upgrade/` (research
lanes, audit trail, attestations).
