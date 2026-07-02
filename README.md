# PABCD Initiative

Canonical home for the PABCD development methodology: the FSM-driven workflow
(PABCD state machine + attestation), the dev skill family that catches LLM
detail-misses, and the modular router+references architecture.

- `skills/` — the 13-skill dev family, snapshotted from `cli-jaw/skills_ref` at the
  2026-07-02 75-grade upgrade (router diets, sourced 2026 currency, freshness
  stamps, AI-era gates), then made **agent-neutral**: no host-CLI commands —
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

Method background: cli-jaw `devlog/_plan/260702_dev_skills_75_upgrade/` (research
lanes, audit trail, attestations).
