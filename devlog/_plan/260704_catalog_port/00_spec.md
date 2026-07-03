# Catalog Discovery Port — Spec & Slice Map

Date: 2026-07-04
Goal: Port design/UX-first Catalog Discovery to all 3 downstream harnesses.
Predecessor: `devlog/_plan/260704_catalog_discovery/` (canonical implementation complete, verified).
Port rule: README.md — "Ports are adapted, never blind-copied."

## Loop-spec header

- **Loop archetype**: spec/repair (verifier defines done — each port must reference the
  catalog, enforce design-first ordering in its host idiom, and pass no-cross-contamination check).
- **Trigger**: user goal — port catalog_discovery to cli-jaw, jawcode, opencodex.
- **Goal**: each harness can run a catalog_discovery interview with design/UX leading.
- **Non-goals**: no new GUI components; no runtime catalog filtering engine; no changes to
  the canonical pabcd_initiative source (already done).
- **Verifier**: per-repo: (a) catalog file exists at correct path, (b) interview/skill prose
  references catalog and declares design-first, (c) no foreign host-CLI tokens
  (each repo only uses its own idiom), (d) TypeScript compiles where applicable.
- **Stop condition**: all 3 ports pass their verifiers.
- **Memory artifact**: this folder.
- **Expected terminal states**: DONE | BLOCKED (repo structure changed upstream).

## Work-phase slice map

| Phase | Repo | Outcome | Verifier |
|---|---|---|---|
| 1 | cli-jaw | FSM I-state prompt hook + catalog YAML + orchestration.md update | tsc + grep checks |
| 2 | jawcode | jaw-interview SKILL.md catalog mode + auto-research variant + catalog YAML | grep + no tsc (prompt-only) |
| 3 | opencodex | structure/ doc referencing catalog for downstream consumers | file exists + content check |

Phase docs: `10_phase1_cli_jaw.md`, `20_phase2_jawcode.md`, `30_phase3_opencodex.md`.
