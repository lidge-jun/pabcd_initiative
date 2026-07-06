# 20_phase2 — jawcode NATIVE port: `jwc map <cwd>` on pi-ast tree-sitter

Phase 2 of 3. Target repo: `/Users/jun/Developer/new/700_projects/jawcode`.
Runs in jawcode's OWN implementation unit; this doc is the direction + insertion map.
Recon: 2026-07-06 (Ptolemy). Class: C3 (native crate + napi + agent tool + prompt).

## Repo shape that constrains the port — this is the TRUE native path

jawcode already OWNS tree-sitter natively, so vendoring Python (the codexclaw path)
would duplicate a capability it has. The native path reuses `crates/pi-ast`.

- `crates/pi-ast` has tree-sitter + ast-grep-core with 20+ language parsers
  (`Cargo.toml`), `resolve_language`, `collect_matches`, `supported_lang_list`
  (`crates/pi-ast/src/ops.rs`). BUT it exposes pattern search/rewrite only — NO
  tags-query API (no `tags.scm` / QueryCursor / @definition/@reference). Public surface
  is `language/ops/summary/SupportLang` (`crates/pi-ast/src/lib.rs:1-5`).
- TS<-Rust bridge is napi via `crates/pi-natives` (`ast_grep`/`ast_edit` are `#[napi]`
  at `crates/pi-natives/src/ast.rs:532-533,688-689`), surfaced to TS as
  `@jawcode-dev/natives` generated `native/index.js:30-42` / `index.d.ts:225-229`.
- Agent tool registry: `packages/coding-agent/src/tools/index.ts` (AstGrepTool pattern
  at `:34-35, :71-73, :339-345`; essentials at `:300-316`).
- CLI: `packages/coding-agent/src/cli.ts` subcommand array (`:36-59, :68-75`).
- System prompt: `packages/coding-agent/src/prompts/system/system-prompt.md`,
  `<ast-tools>` section (`:230-239`) and search-guidance (`:332-336`).
- NO reusable PageRank/graph util (`state-graph.ts:59` is unrelated). PageRank is net-new.

## Native build path (the real cost)

`crates/pi-ast` (add tags-query fn + per-language tags.scm) -> `crates/pi-natives/src/ast.rs`
(napi export, e.g. `repo_map` / `extract_tags`) -> `bun --cwd=packages/natives run build`
regenerates napi binding + `index.d.ts` + enum exports
(`packages/natives/scripts/build-native.ts:155-209`). So this port requires a cargo
rebuild + napi regen, unlike cli-jaw/codexclaw.

## Decisions (OA2/OA3)

- **Ranking (OA2)**: recommend PageRank in RUST inside pi-ast (petgraph or a ~60-line
  power-iteration over the ref graph) so the whole map builds in one native call and TS
  just renders. Alternative: defs-only ref-count ranking in TS first, PageRank later.
  Recommend native PageRank because pi-ast already holds the parsed refs — doing it in
  Rust avoids shipping the ref graph across the napi boundary.
- **Language tier (OA3)**: TS/JS + Rust fixture-verified first (jawcode's own stack),
  inherit others from the vendored tags.scm best-effort.
- **tags.scm source**: reuse Aider's `tags.scm` set (Apache-2.0) that codexclaw already
  vendored — copy the query files into `crates/pi-ast` resources; attribute in NOTICE.

## Insertion map (diff-level)

| # | File | Change |
|---|------|--------|
| 1 | `crates/pi-ast/src/tags.rs` (NEW) + `resources/tags/*.scm` | tree-sitter tags-query: parse a file, run the language's tags.scm via QueryCursor, return defs+refs; add `pub fn extract_tags(...)` and a `repo_map(paths, budget)` that walks, tags, ranks |
| 2 | `crates/pi-ast/src/lib.rs` | export the new `tags` module |
| 3 | `crates/pi-ast` PageRank (in `tags.rs` or a `rank.rs`) | power-iteration over referencer->definer edges; budget-cut by rank |
| 4 | `crates/pi-natives/src/ast.rs` | `#[napi] pub fn repo_map(...)` wrapping pi-ast; mirror the AstGrep napi pattern |
| 5 | `packages/natives/native/index.d.ts` (generated) | via `bun run build` — do not hand-edit |
| 6 | `packages/coding-agent/src/tools/map.ts` (NEW) | agent tool calling the native `repoMap`; schema `{ path, budget? }`; description says "ranked structure map; run before deep grep in unfamiliar code" |
| 7 | `packages/coding-agent/src/tools/index.ts` | import/export MapTool; add to `BUILTIN_TOOLS`; consider `DEFAULT_ESSENTIAL_TOOL_NAMES` |
| 8 | `packages/coding-agent/src/cli.ts` (36-59, 68-75) | add `jwc map <cwd>` subcommand |
| 9 | `packages/coding-agent/src/prompts/system/system-prompt.md` (`<ast-tools>` 230-239) | affordance line: the map tool exists; run before deep grep in unfamiliar code |

## Verifier (jawcode gate)

- `jwc map <a real crate/package dir>` prints a ranked symbol map, exit 0.
- the `map` tool appears in the tool registry; the model can call it.
- `grep -n "map" packages/coding-agent/src/prompts/system/system-prompt.md` -> affordance.
- cargo test (pi-ast tags), `bun run build` for natives succeeds, jawcode TS gate green.
- fixtures: TS + Rust mini-files with known symbols, assert they appear.

## Effort note

Recon judgment: TS+Rust-first is a "few hundred line" add; full multi-language tags +
refined ref graph is medium+. Ship TS+Rust tier first, expand later. This is the only
port needing a native (cargo + napi) build.
