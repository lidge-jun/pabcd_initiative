# 00_spec — repo-map (structure map) tool: SoT + native ports to 3 harnesses

Date: 2026-07-06
Unit: `devlog/_plan/260706_repomap_native_ports/`
Class: C3 (cross-harness capability port; each target adapts natively, durable audit trail)

## Loop-spec

- **Loop archetype**: spec-satisfaction (each port has a concrete verifier: the
  `map` command emits a ranked symbol map on a real dir, and the agent is told it exists).
- **Trigger**: user directive 2026-07-06. codexclaw shipped `cxc map` (vendored
  RepoMapper: tree-sitter tags + PageRank) plus a SessionStart affordance. The same
  capability should exist in cli-jaw and jawcode, but as NATIVE implementations that
  fit each repo's stack — not a blind copy of the Python vendoring. pabcd_initiative is
  the SoT that holds the tool concept + deployment line so the three stay in sync.
- **Goal**: an agent working in ANY of the three harnesses can, without being told,
  learn a structure-map tool exists and run it on demand (`<runtime> map <cwd>`) before
  deep grep dives in unfamiliar code. Each harness implements the engine in its own
  idiom; the SoT names the contract + affordance, not one shared binary.
- **Non-goals**:
  - No whole-repo map preload into the system prompt (the map BODY is on-demand only;
    only a one-line POINTER affordance is injected). This is the deliberately-rejected
    session-start-index pattern — evidence in codexclaw `devlog/_plan/lazygap/005` and
    `260706_repo_map`.
  - No single shared binary the three call (they diverge by stack: Python vendor vs
    native pi-ast vs new TS dep). SoT syncs the CONTRACT, not the code.
  - No daemon/server/watcher/persistent index in any port (stateless one-shot; a
    rebuildable derived cache is allowed).
- **Verifier (per port)**:
  - `<runtime> map <a real source dir>` prints a ranked, file-grouped symbol list and
    exits 0; on missing deps it prints one install/again hint, never a stack trace.
  - the agent's system prompt (or SessionStart affordance) names the tool at a real
    insertion point (evidence: grep the inserted line).
  - existing test/build gate of that repo stays green.
- **Stop condition**: all three port docs (10/20/30) written to diff-level; SoT tool
  doc committed; no code changed in this unit (this unit is PLAN + SoT text only —
  implementation happens in each downstream repo's own unit).
- **Memory artifact**: this unit folder.
- **Expected terminal states**: DONE (all docs + SoT written, verified present) or
  NEEDS_HUMAN if a per-repo effort/scope decision is rejected.

## The three harnesses are structurally different (recon 2026-07-06)

This is the load-bearing finding. A blind copy is impossible; each needs a different
native shape.

| Harness | Stack | Map engine path | Tool surface | Prompt surface |
|---|---|---|---|---|
| codexclaw | Codex plugin (TS components + Python skill scripts) | DONE — vendored RepoMapper Python (`skills/repo-map/scripts`) | `cxc map` dispatcher + repo-map skill | SessionStart affordance hook (cxc-ops) |
| cli-jaw | TS/Node/Express client-server; agent = spawned external CLI | NEW TS engine or external helper (no tree-sitter dep today; has `fast-glob`, `@lezer/highlight`) | `cli-jaw map` CLI command (`bin/commands/map.ts`); NO model function-tool registry exists | `src/prompt/templates/a1-system.md` "Project context discovery" section |
| jawcode | TS+Rust monorepo; native pi-ast crate has tree-sitter + ast-grep-core | NATIVE — add tags-query to `crates/pi-ast`, expose via `pi-natives` napi | `jwc map` CLI (`packages/coding-agent/src/cli.ts`) + agent tool (`src/tools/index.ts` registry) | `packages/coding-agent/src/prompts/system/system-prompt.md` `<ast-tools>` section |

## SoT deployment line (how sync works)

`skills/dev-scaffolding` already owns SOT-SYNC-01: find the general SoT doc, patch it in
the same unit at C. This unit ADDS a repo-map capability doc to the SoT
(`skills/dev-pabcd/references/repo-map-capability.md`, or a new SoT note — see 05) that:

1. Names the tool contract (input `<cwd>`, output ranked symbol map, on-demand, no
   preload, one-line affordance) in agent-neutral terms (Runtime adapter style).
2. Lists the three port sites + their status, so a future freshness sweep re-checks all
   three against the SoT contract.

Downstream repos each get their OWN implementation unit (this unit only writes the plan
+ SoT text; it does not edit downstream code).

## Phase docs (dependency-ordered, PHASE-SPLIT-01)

- `05_sot_capability_doc.md` — the SoT capability note + deployment-line table (write first;
  it is the contract the ports satisfy).
- `10_phase1_cli_jaw.md` — cli-jaw native port direction (TS engine choice + CLI + prompt).
- `20_phase2_jawcode.md` — jawcode native port direction (pi-ast tags-query + napi + tool + prompt).
- `30_phase3_codexclaw_backport.md` — reconcile codexclaw (already shipped) against the
  SoT contract; record it as the reference implementation + any drift to fix.

## Open assumptions (carried to A)

- OA1: cli-jaw map engine — pure-TS tree-sitter (`web-tree-sitter` / `tree-sitter` napi)
  vs shelling to an external helper vs a lightweight lezer-based symbol scan. 10 proposes;
  user picks at that repo's own interview.
- OA2: jawcode ranking — PageRank is net-new (no graph util exists). Options: port a
  small PageRank in Rust (pi-ast) or in TS (coding-agent), or ship defs-only ranking
  (by ref-count) first and add PageRank later. 20 proposes.
- OA3: language scope per port — start with each repo's primary languages (cli-jaw: TS;
  jawcode: TS+Rust) rather than all 25, matching codexclaw's fixture-verified tiering.
