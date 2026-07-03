# Phase 3 — opencodex port

## Part 1 — Plain explanation
opencodex is infrastructure plumbing (LLM proxy), not a product-creation tool — it has no
interview surface and no project concept. The investigation concluded a full GUI wizard or API
endpoint would be artificial. The honest port is a process-doc: document that new GUI surfaces
in opencodex must follow catalog-discovery stage ordering (design/UX first) so the invariant is
visible to contributors without bolting on runtime code with no consumer.

## Part 2 — Diff-level precision

### NEW: `structure/07_design-methodology.md`
```markdown
# 07 — Design Methodology for New Surfaces

When adding or redesigning a GUI page, CLI wizard, or user-facing flow in opencodex,
follow the PABCD Catalog Discovery stage ordering:

1. **Design/UX decisions first** (Product-Personality-Selection): mood, density, lightness,
   shape, typography, motion. Decide visual direction before functional layout.
2. **Domain-specific config semantics** second: what entities does this surface manage
   (providers, models, accounts, sidecars)?
3. **Backend wiring derived last**: API endpoints, data structures, and state management
   are consequences of the above, not independent decisions.

This is the design-first invariant (CATALOG-DESIGN-FIRST-01) from the PABCD Initiative
(pabcd_initiative/skills/dev-pabcd/references/catalog-discovery.yaml). It ensures design
coherence across surfaces without requiring a runtime interview engine.

## Existing surfaces and their design direction

| Surface | Current design | Notes |
|---|---|---|
| Dashboard | Data-dense, light, rounded, sans | Default Bun/React template |
| ocx init | CLI numbered menu, no personality | Flat — could benefit from staged approach |
| Add Provider modal | Functional form | Minimal styling |

When next touching these surfaces, apply the stage-1 design dials before restructuring layout.
```

## Files touched
- NEW `structure/07_design-methodology.md`

## Verifier
- File exists and is non-empty
- `grep -c 'CATALOG-DESIGN-FIRST-01' structure/07_design-methodology.md` → ≥1
- `grep -cE 'cli-jaw|jawcode|codexclaw' structure/07_design-methodology.md` → 0
