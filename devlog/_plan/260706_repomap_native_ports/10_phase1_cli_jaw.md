# 10_phase1 — cli-jaw native port: `cli-jaw map <cwd>` + prompt affordance

Phase 1 of 3. Target repo: `/Users/jun/Developer/new/700_projects/cli-jaw`.
Runs in cli-jaw's OWN implementation unit; this doc is the direction + insertion map.
Recon: 2026-07-06 (Banach). Class: C3 (new agent-facing capability).

## Repo shape that constrains the port

- TS/Node/Express, client-server: `bin/` is a CLI client; real logic in `src/`
  (`server.ts:1-2` "business logic lives in src/").
- The Boss agent is a SPAWNED EXTERNAL CLI (claude/codex/opencode) — cli-jaw has NO
  in-process model function-tool registry (`src/agent/args.ts:140-267`,
  `src/agent/spawn.ts:1949-1967`). So the map is surfaced as a CLI command + a system
  prompt affordance, NOT a model tool schema. (code-mode/JWC ACP tool exposure is a
  bigger, separate effort — `src/code-mode/acp-host.ts:233-240` passes `mcpServers: []`;
  out of scope for phase 1.)
- No tree-sitter/ast-grep dep today (`package.json:128-176`); has `fast-glob:151`,
  `@lezer/highlight:137`. A map engine needs a new dep or an external helper.
- Shell-out precedent is abundant (`bin/commands/serve.ts:64-90`,
  `src/agent/spawn.ts:1962-1967`, allowlist runner `src/jaw-ceo/coordinator-utils.ts:70-100`).
- Existing fs-walk to reuse: `src/workflows/context-map/builder.ts:29-56`
  (readdirSync + .git/node_modules skip + depth cap + ext filter).

## Engine decision (OA1 — resolve at cli-jaw's interview)

Three candidates, recommend in order:
1. **web-tree-sitter (pure JS/WASM) + Aider tags.scm** — pure-TS, no native build, runs
   in the same node process. Adds tree-sitter symbol enumeration cli-jaw does not have.
   Recommended: matches "native to the repo's stack" and needs no external runtime.
2. **External helper: call codexclaw's `cxc map`** if present on PATH — cheapest, but
   couples cli-jaw to a codexclaw install. Reject unless codexclaw is a hard dep.
3. **Lezer-based symbol scan** (reuse `@lezer/highlight`) — no new dep, but Lezer
   grammars are highlight-oriented, not tag-query; weaker symbol coverage. Fallback only.

Ranking: start with defs-only ordered by ref-count (cheap, deterministic); add PageRank
later if the map quality needs it. Language tier: TS/JS fixture-verified first.

## Insertion map (diff-level)

| # | File | Change |
|---|------|--------|
| 1 | `bin/commands/map.ts` (NEW) | top-level exec command (pattern: `bin/commands/status.ts:11-39`): parse `<path> [--budget N]`, build the map via the chosen engine, print ranked listing; `--help` without deps prints usage; missing engine dep -> one install hint + nonzero exit |
| 2 | `bin/cli-jaw.ts` (`switch(command)` ~184-281) | add `case 'map': await import('./commands/map.js'); break;` |
| 3 | `bin/cli-jaw.ts` `printHelp()` (135-164) | add a `map <dir>` line to the command list |
| 4 | `src/prompt/templates/a1-system.md` (project-discovery section ~42-51) | ONE affordance line: "Unfamiliar repo: run `cli-jaw map <cwd>` (ranked structure map) before broad/deep Grep. On-demand; keep Grep for text search." |
| 5 | map engine module under `src/` (e.g. `src/workflows/repo-map/`) | reuse `context-map/builder.ts` walk; add tree-sitter tag extraction + ranking + token budget |
| 6 | `package.json` | add the chosen engine dep (if web-tree-sitter) + its grammars |

## Verifier (cli-jaw gate)

- `cli-jaw map src/` prints a ranked, file-grouped symbol map, exit 0; missing dep ->
  one hint line.
- `grep -n "cli-jaw map" src/prompt/templates/a1-system.md` -> affordance present.
- `npx tsc --noEmit` + `npm test` + `npm run gate:all` stay green.
- fixture: a small TS fixture dir, assert known exported symbols appear.

## Non-goals (phase 1)

No code-mode/JWC ACP tool exposure; no model function-tool schema (cli-jaw has none);
no PageRank in v1 (ref-count ranking is acceptable); no all-language claim.
