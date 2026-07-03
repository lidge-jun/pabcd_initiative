# Catalog Discovery — Spec & Slice Map (design/UX-first)

Date: 2026-07-04
Goal: design/UX-first Catalog Discovery interview mode in the canonical PABCD skills.
Predecessor design: `devlog/260704_catalog_discovery_design.md` (3-employee discussion synthesis).

## Loop-spec header

- **Loop archetype**: spec/repair (a verifier defines *done* — the catalog + interview
  section must satisfy schema + design-first ordering checks; not open-ended optimization).
- **Trigger**: user goal — add catalog_discovery mode, design/UX leading.
- **Goal (user-visible outcome)**: an author/agent running the PABCD Interview on a novice
  ("사주 앱 만들고 싶어") is guided design/UX-FIRST through a versioned option catalog,
  and downstream (security/data/ops/feature) questions are DERIVED from the design+domain
  choices — not asked in a flat undifferentiated list.
- **Non-goals**: no host-CLI code, no runtime engine, no GUI build, no downstream repo edits
  (this pass is canonical-source only; ports tracked separately in backlog).
- **Verifier**: (a) YAML parses (`python3 -c "import yaml,sys; yaml.safe_load(...)"`),
  (b) schema-consistency check — every `implies`/`conflicts`/`derived_from` id resolves to a
  real entry; design axis entries exist for all 6 dials; `axis_order` lists design first,
  (c) prose-consistency — dev-pabcd Interview section references the catalog file and the
  design-first ordering; (d) saju dry-run doc shows design questions asked before
  security/data questions. Measures: referential integrity + ordering correctness, not just
  "file exists".
- **Stop condition**: all 3 work-phases pass their verifier; goal objective's 3 deliverables exist.
- **Memory artifact**: this folder + `devlog/260704_catalog_discovery_design.md`.
- **Expected terminal states**: DONE (all deliverables + verifiers green) | BLOCKED (schema
  can't express design-first derivation cleanly) | NEEDS_HUMAN (business ambiguity in axis semantics).
- **Escalation**: if design-first derivation needs a runtime engine to be meaningful (i.e.
  static YAML can't encode it), stop and surface — that would change scope to code.

## Core architectural decision: design/UX LEADS

The user's hint is the load-bearing constraint: **design/UX is the most important axis; the
backend (security/data/ops) asks its questions BASED ON the design+domain answers.** This is
encoded three ways so it survives prompt drift:

1. **`axis_order` (data)**: catalog declares an explicit stage order —
   `stage 1: design → stage 2: domain(app-type) → stage 3: derived (feature/data/security/ops/cost)`.
   Design is stage 1, always first.
2. **`derived_from` (data)**: stage-3 entries carry `derived_from: [design.*, domain.*]` so the
   configurator can PRIORITIZE/FILTER them from earlier answers instead of dumping a flat list.
3. **Interview prose (skill)**: the catalog_discovery sub-mode explicitly asks design/UX first,
   wired to dev-uiux-design Product-Personality-Selection as the step-1 methodology.

## Work-phase slice map (one full PABCD pass each, design pass already done)

| Phase | Outcome unit | Deliverable | Verifier |
|---|---|---|---|
| **0 (done)** | Design synthesis | `devlog/260704_catalog_discovery_design.md` | committed (82ab348) |
| **1** | Versioned catalog exists, design-first | `skills/dev-pabcd/references/catalog-discovery.yaml` | YAML parse + schema-integrity script |
| **2** | Interview uses catalog design-first | `skills/dev-pabcd/SKILL.md` Interview section: catalog_discovery + configurator sub-modes | prose references catalog + design-first ordering; agent-neutral (no host-CLI) |
| **3** | Design-first flow proven | `devlog/_plan/260704_catalog_discovery/30_saju_dryrun.md` | walkthrough shows design Qs before security/data Qs |

Phase docs: `10_phase1_catalog.md`, `20_phase2_interview.md`, `30_saju_dryrun.md`.

## Terminal-state honesty
Each phase's D records what did NOT get proven and what would falsify the design-first claim.
