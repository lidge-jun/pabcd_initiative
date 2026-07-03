# Catalog Discovery Port Record — 2026-07-04

Ported design/UX-first Catalog Discovery (INTERVIEW-CATALOG-01 / CATALOG-DESIGN-FIRST-01)
from the canonical `skills/dev-pabcd/references/catalog-discovery.yaml` to all 3 downstream
harnesses. Each port adapted to its host idiom (README.md: "Ports are adapted, never blind-copied").

## Port status per copy

| Copy | Status | Integration type | Commit |
|---|---|---|---|
| **pabcd_initiative** (canonical) | DONE (prior goal) | YAML + SKILL.md §1 + dry-run | main, 260704 |
| **cli-jaw** | DONE | FSM prompt hook (STATE_PROMPTS.I) + OrcContext type + catalog YAML in skills_ref submodule + orchestration.md bullet | committed, tsc clean |
| **jawcode** | DONE | jaw-interview Phase 1.5 + 2 `.md` skill-fragments (catalog-discovery-axes, auto-research-catalog) | committed, grep-verified |
| **opencodex** | DONE | Process-doc only (`structure/07_design-methodology.md`) — no runtime, matches infra-plumbing nature | committed |

## Adaptation notes per harness

### cli-jaw
- **Prompt hook**: Catalog Discovery section appended to `STATE_PROMPTS.I` (I-state prompt string in `state-machine.ts`). Follows existing conditional-block-in-prompt pattern (like Loop/Multi-Pass detection).
- **OrcContext**: 3 optional fields added to `interview?` type: `catalogMode`, `catalogStage`, `catalogSelections`. Follows existing perspective rotation pattern in `getPrefix()`.
- **Catalog YAML**: placed in `skills_ref/dev-pabcd/references/` (submodule — committed inside submodule first, then parent). Port header comment added.
- **orchestration.md**: 1 bullet added in IPABCD section referencing the sub-mode.

### jawcode
- **No `.yaml` files** — jawcode convention is `.md` skill-fragments with `kind: "skill-fragment"` metadata. Catalog data encoded as markdown tables with option details.
- **Phase 1.5**: inserted between Phase 1 (init) and Round 0 (topology enumeration gate). Catalog selections feed INTO Round 0 as candidate component list — does not replace the Socratic loop.
- **Ambiguity pre-seeding**: catalog answers pre-seed dimension clarity so the Socratic loop starts below 1.0 ambiguity.
- **auto-research-catalog.md**: follows `auto-research-greenfield.md` pattern — spawned read-only architect that returns structured JSON.

### opencodex
- **No runtime feature** — opencodex is an LLM proxy with no project concept or interview surface.
- **Process-doc**: `structure/07_design-methodology.md` documents the design-first invariant for contributors adding/redesigning GUI surfaces. References canonical source.

## Principle delta worth porting (from prior port record 260703)

Same 3 principles apply:
1. Design/UX decisions come before functional/backend decisions (structural, not stylistic).
2. The catalog is a data structure, not prompt improvisation — prevents option drop-out.
3. Each harness adapts to its own idiom — no blind-copied foreign tokens.
