# Repo-Map Capability (SoT, agent-neutral)

> Source-of-truth contract for the "structure map" capability shared across the
> pabcd_initiative harnesses (codexclaw, cli-jaw, jawcode). This file names WHAT the
> tool must do and HOW it is surfaced; each harness implements the engine in its own
> stack (Runtime adapter style — see `../SKILL.md` Runtime adapter note). When a port
> drifts from this contract, fix the port or amend this file in the same unit
> (SOT-SYNC-01). Ports are adapted, never blind-copied.

## Why this capability exists

The pre-edit exploration phase is the real cost of agentic coding: `rg`/grep answers
"where is this string" but the agent reconstructs the repo's SHAPE by opening files
every session. A ranked structure map (which files own which symbols, ranked by
reference gravity) collapses that. External research (2026-07-06, four lanes; see
codexclaw `devlog/_plan/260706_repo_map/00_plan.md` Sources) is consistent:

- On-demand, tool-invoked structure maps are the most TOKEN-EFFICIENT exploration aid.
- Whole-repo indexing PRELOADED at session start is the weakest-evidence pattern
  (stale-index problem; abandoned by Claude Code; Aider disables the map for weak
  models). So the map BODY is on-demand only.
- The affordance (telling the agent the tool exists) is the missing link: a map tool
  no model knows about is never used.

## Contract (all ports MUST satisfy)

1. **Invocation**: `<runtime> map <path> [--budget N]` — a stateless one-shot command.
   `<runtime>` = `cxc` (codexclaw), `cli-jaw` (cli-jaw), `jwc` (jawcode).
2. **Output**: a token-budgeted, file-grouped listing of DEFINITIONS (functions,
   types, classes, exports) with line numbers, ordered by importance (reference
   gravity — PageRank over the symbol-reference graph, or a defensible proxy such as
   ref-count when PageRank is not yet available). Default budget ~4096 tokens.
3. **Engine**: tree-sitter tag queries (definition/reference capture, Aider-lineage
   `tags.scm`) are the honest engine. ast-grep pattern search is NOT sufficient for
   full symbol enumeration (silent misses). Reuse the repo's existing tree-sitter if
   it has one.
4. **No preload, no server**: never inject the map body into the system prompt; never
   run a daemon/watcher/persistent index. A rebuildable derived cache (e.g. a tags
   cache under the repo's scratch dir) is allowed and must be gitignored + wiped by the
   repo's reset command.
5. **Graceful degradation**: missing engine deps print ONE install/enable hint and a
   nonzero exit, never a stack trace. `--help` works without heavy deps.
6. **Affordance (the discoverability half)**: the agent MUST be told the tool exists
   through a real enforcement/prompt surface — NOT only a skill the model might not
   read. Acceptable surfaces, in order of the runtime's capability:
   - a session-start context injection (Codex SessionStart additionalContext), or
   - a one-line entry in the coding agent's MAIN system prompt near its search/discovery
     guidance, or
   - a registered model tool whose description says "run before deep grep in unfamiliar
     code."
   The affordance is a POINTER (the tool exists, use it on demand), never the map body.
   Gate it on repo size where cheap (skip tiny repos).

## Port sites + status (freshness-sweep re-checks this table)

| Harness | Engine | Command site | Affordance site | Status |
|---|---|---|---|---|
| codexclaw | vendored RepoMapper (Python, tree-sitter tags + PageRank) | `bin/codexclaw.mjs` `map` -> `skills/repo-map/scripts/repomap.py` | SessionStart hook `session-start-announcing-map-affordance.json` (cxc-ops) | SHIPPED 2026-07-06 (reference impl) |
| cli-jaw | NEW native TS engine (no tree-sitter dep today) | `bin/commands/map.ts` + `bin/cli-jaw.ts` case | `src/prompt/templates/a1-system.md` project-discovery section | PLANNED (this unit 10) |
| jawcode | NATIVE pi-ast (tree-sitter + ast-grep-core already present) + napi | `packages/coding-agent/src/cli.ts` `map` + `src/tools/index.ts` tool | `packages/coding-agent/src/prompts/system/system-prompt.md` `<ast-tools>` | PLANNED (this unit 20) |

## Verification tiering (per port)

Match the fixture-verified tier discipline codexclaw used: verify the tag queries
against real fixtures for that repo's PRIMARY languages first (cli-jaw: TS/JS;
jawcode: TS/JS + Rust), inherit other languages best-effort from the upstream
`tags.scm` set. Do not claim "all languages" without per-language fixture evidence.
