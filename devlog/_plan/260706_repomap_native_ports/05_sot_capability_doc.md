# 05_sot_capability_doc — SoT capability note + deployment line

Phase 0 of the unit (write first — it is the contract the ports satisfy).

## What ships in the SoT (this repo, pabcd_initiative)

NEW: `skills/dev-pabcd/references/repo-map-capability.md` — the agent-neutral contract
(invocation, output, engine, no-preload rule, graceful degradation, affordance surfaces)
+ the port-sites/status table + verification tiering. Written in Runtime-adapter style so
each harness reads it and maps to its own stack.

MODIFY (at C, SOT-SYNC-01): `skills/dev-pabcd/SKILL.md` — add one line under the
references list pointing to `references/repo-map-capability.md`, so an agent loading the
dev-pabcd skill discovers the capability contract. Keep it a pointer, not a duplicate.

MODIFY: `README.md` — add repo-map to the "Downstream adaptations" paragraph (the doc
already enumerates the cxc-*/jwc port targets; repo-map is a new shared capability).

## Deployment line (the sync mechanism the user asked for)

The SoT `repo-map-capability.md` port-sites table is the single place that lists all
three implementations + status. The recurring freshness sweep
(`prompts/freshness-sweep.md`) re-reads that table and re-verifies each port against the
contract, emitting a downstream port backlog when one drifts. This is exactly how the
dev-skill family already stays in sync across the three harnesses; repo-map joins that
line as a capability row instead of a one-off feature.

## Why SoT-here, engine-there (not one shared binary)

Recon 2026-07-06 proved the three stacks cannot share an engine binary:
- codexclaw runs Python skill scripts -> vendored RepoMapper works.
- cli-jaw is TS/Node with NO tree-sitter dep and NO model tool registry -> needs a TS
  engine + a CLI/prompt affordance, not a Python vendor.
- jawcode already has tree-sitter native in `crates/pi-ast` -> vendoring Python would
  duplicate a capability it already owns; the native path is a tags-query addition.

So the SoT syncs the CONTRACT (what map does + how it's surfaced), and each repo owns its
engine. Drift is caught by re-verifying the contract, not by diffing source.

## Verifier for THIS phase

- `test -f skills/dev-pabcd/references/repo-map-capability.md` -> present.
- the port-sites table lists all three harnesses with a status column.
- `grep -n repo-map skills/dev-pabcd/SKILL.md` -> the pointer line exists (added at C).
