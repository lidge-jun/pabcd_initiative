# 30_phase3 — codexclaw reconcile: reference impl vs the SoT contract

Phase 3 of 3. Target repo: `/Users/jun/Developer/new/700_projects/codexclaw`.
codexclaw already SHIPPED repo-map (2026-07-06); this phase confirms it satisfies the
new SoT contract and records it as the reference implementation, noting any drift.

## What codexclaw already has (shipped)

- Engine: vendored RepoMapper (MIT, Aider-lineage tree-sitter tags + PageRank),
  `plugins/codexclaw/skills/repo-map/scripts/` (Python, lazy imports, install-hint
  degradation, `--budget`, cache under `.codexclaw/cache/repomap`).
- Command: `cxc map <dir>` via `bin/codexclaw.mjs` (python3 -B, dist/build/target skip).
- Affordance: SessionStart hook `session-start-announcing-map-affordance.json`
  (cxc-ops `map-affordance.ts`): size-gated one-line POINTER, silent on small repos.
- Docs: `devlog/_plan/260706_repo_map/00_plan.md`, `lazygap/005` amendment,
  dev SKILL §1.5 DEV-MAP-FIRST-01, ast-grep overview boundary, skill-hub catalog.

## Contract conformance check (against 05 / repo-map-capability.md)

| Contract clause | codexclaw | Verdict |
|---|---|---|
| `<runtime> map <path> [--budget N]` one-shot | `cxc map <dir> --budget N` | PASS |
| ranked def listing, ~4096 default | RepoMapper PageRank, default 4096 | PASS |
| tree-sitter tags engine | vendored RepoMapper tags.scm | PASS |
| no preload / no server; rebuildable cache | on-demand; diskcache; wiped by `cxc reset --all` | PASS |
| graceful degradation + `--help` w/o deps | lazy imports; install hint; -B | PASS |
| affordance via a real surface, POINTER only, size-gated | SessionStart additionalContext, 40-file gate | PASS |
| primary-language fixture tiering | TS/JS + Python + Rust fixture-verified | PASS |

Verdict: codexclaw is the REFERENCE implementation of the SoT contract. No drift.

## Backport action (small)

Only one SoT-alignment edit in codexclaw's own future unit (NOT this unit):
- Add a one-line pointer in codexclaw docs (e.g. repo-map SKILL "Notes" or INDEX) to the
  SoT contract `pabcd_initiative/skills/dev-pabcd/references/repo-map-capability.md`, so
  the reference impl links back to the SoT for the freshness sweep. Optional, C0.

## Cross-harness divergences to keep (intentional, not drift)

- Engine differs by stack (Python vendor / pi-ast native / TS engine) — the SoT syncs
  the contract, not the engine (see 05). These are NOT drift; the freshness sweep checks
  contract conformance, not source identity.
- Affordance surface differs by runtime capability (SessionStart hook vs system-prompt
  line vs tool description) — all three are contract-acceptable surfaces.

## Verifier

- the conformance table above maps every contract clause to a shipped codexclaw
  artifact (re-run `cxc map` + grep the affordance hook to confirm live).
- `repo-map-capability.md` port-sites table lists codexclaw status = SHIPPED (reference).
