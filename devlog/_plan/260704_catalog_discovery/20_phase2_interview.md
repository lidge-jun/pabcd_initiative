# Phase 2 — Interview wiring (design-first) [STUB — filled in Phase 2 P]

## MODIFY: skills/dev-pabcd/SKILL.md — Interview section (§1 / §3 P)

Add a `### Catalog Discovery sub-mode (INTERVIEW-CATALOG-01)` block after INTERVIEW-TEACH-01:
- When the user names a vague domain but not features ("사주 앱 만들고 싶어"),
  enter catalog_discovery: present the option map from
  `references/catalog-discovery.yaml`, DESIGN/UX axis FIRST.
- Design-first ordering is mandatory: ask design (Product-Personality-Selection, then
  mood/adjective, reference-first, Design Read) BEFORE domain, and derive
  security/data/ops/feature questions from the design+domain answers via `derived_from`.
- Configurator sub-mode: compile selections (+ resolved implies[] chains) into
  PRD / MVP cut (cost_class) / risk register (risk_class=high) / PABCD plan seed.
- Agent-neutral: reference the catalog by repo-relative path; no host-CLI commands.

Verifier (Phase 2): grep the Interview section for the catalog path + "design" ordering
+ "Product-Personality"; confirm zero host-CLI command strings added.
