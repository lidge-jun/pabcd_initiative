# PABCD Freshness Sweep — Cron Prompt

Recurring re-verification of the dev skill family, run as MULTIPLE full PABCD cycles.
Cadence: quarterly (or monthly for fast-moving stacks). Canonical skill source:
`skills/` in this initiative (upgraded 2026-07-02 baseline; all skills carry
`last-verified` frontmatter stamps and reference-level `## Sources` tables).

Copy everything below the line into the scheduled agent's prompt.

---

You are running the scheduled freshness sweep for the dev skill family under
<SKILLS_ROOT> (default: this initiative's `skills/`; substitute a downstream deploy
copy when sweeping a live repo). This prompt is agent-neutral: use whatever runtime
you are on — its built-in web search for discovery, CDP-based (or equivalent)
browser automation only to open/verify primary sources that plain fetch cannot
reach, and its subagent/delegation surface for parallel lanes. Work in goal mode:
PABCD gates are satisfied by evidence-backed checkpoints, one full P→A→B→C→D cycle
per work-phase, never rubber-stamp a phase; if your runtime has no FSM command,
keep the state machine in your notes and record attestations in the devlog (see
the Runtime adapter note in `skills/dev-pabcd/SKILL.md`). Severity classes:
`skills/dev/SKILL.md` §0.2.

## Cycle 0 — Inventory & Research (design-only pass)

P:
1. Build the rot-claim inventory: for every SKILL.md and reference file, collect
   (a) `last-verified` stamps older than the sweep date minus one cadence period,
   (b) every version-pinned or time-sensitive claim (grep for version numbers,
   years, "deprecated", product names, standard names), (c) every `## Sources`
   row. Record the inventory as a devlog research doc (decade numbering: 00_plan,
   01+_research).
2. Dispatch parallel research lanes over the inventory — one lane per domain
   (skill-engineering / testing-debugging / backend-architecture / frontend-uiux /
   devops-data / security-review), ≤5 items per subagent run to avoid context
   exhaustion; re-split and retry a lane once on failure, then run remaining items
   inline via built-in web search. Every lane returns Corrections / Confirmations /
   Additions with per-claim source URL + published date + evidence status
   (sufficient = primary page actually opened/fetched — escalate to CDP browser
   automation when the page is JS-rendered or fetch-blocked; partial =
   snippet-level — snippet consensus alone is never sufficient).
A: dispatch one independent read-only audit of the research-vs-inventory coverage:
   every inventoried claim must be covered by a lane result or an explicit
   out-of-scope declaration. Fix coverage gaps before proceeding.
B/C/D: write the correction backlog (per-skill patch list, grouped into
   implementation cycles of ≤6 substantive files each), gate it (every planned
   correction cites a lane finding), record the cycle summary + attestation.

## Cycles 1..N — Patch (one PABCD per skill group)

Default grouping: (1) meta: dev, dev-pabcd, dev-architecture, dev-code-reviewer;
(2) quality: dev-testing, dev-debugging, dev-security; (3) frontend: dev-frontend,
dev-uiux-design; (4) infra: dev-backend, dev-data, dev-devops, dev-scaffolding.
Skip a group's cycle entirely when the backlog has no corrections for it.

Per cycle:
- P: restate the group's backlog items (quote the lane findings).
- A: self-audit the patch plan against the skill Ownership Map in
  `skills/dev/SKILL.md` (canonical content stays with its owner; stubs never gain
  canonical content).
- B: apply corrections. Rules: version-pinned claims live in references with an
  updated Sources row; routers keep only the frontmatter stamp; every NEW rule
  carries a severity class; router line caps hold (dev ≤410, dev-frontend ≤400,
  all ≤500); no blind rewrites — surgical replacements only.
- C gates (all must pass): `wc -l` caps; every changed pointer/path resolves;
  frontmatter YAML parses with updated `last-verified`; registry descriptions/
  versions synced if the deploy target has a registry; rot-residue grep returns
  only intentional matches (migration notes, deprecation notices).
- D: commit per cycle with research grounding cited; update the devlog attestation
  log.

## Final cycle — Independent verify & propagate

- Dispatch one independent read-only verifier over the full sweep diff:
  cross-refs, research fidelity (no overclaiming beyond lane verdicts —
  `partial` evidence gates wording only, never new version pins), structure,
  registry. FAIL findings are fixed and re-gated before closing.
- Optimization-loop discipline applies to the sweep itself (dev-pabcd §10): if the
  same correction class keeps getting rejected across cycles, target the gate/
  process, not another patch of that class.
- Propagation: report (do not silently edit) the delta relevant to downstream
  forks — codexclaw `plugins/codexclaw/skills/` and jawcode
  `packages/coding-agent/src/defaults/jwc/skills/` — as a port backlog with exact
  old→new wording, unless the run was explicitly scoped to patch them too (then
  each fork is one additional PABCD cycle: adapt to local conventions, never
  blind-copy, run the fork's own tests/gates, commit only sweep-touched files).

## Hard rules

- English for all work products; sources cited for every factual correction.
- Never delete content to "fix" staleness — correct it or mark it explicitly
  unverified.
- If a lane cannot verify a claim, downgrade the skill wording to non-committal
  and record `partial`; do not leave a stale confident claim standing.
- Do not push; commits stay local for human review.
- End-of-run report: corrections applied per skill, claims confirmed unchanged,
  unverifiable items, stamp updates, and the downstream port backlog.
