# Phase 2 — jawcode port

## Part 1 — Plain explanation
jawcode's jaw-interview skill gets a pre-Round-0 "Catalog Discovery" path. When a
greenfield user says something vague about building a product, catalog discovery runs
design/UX questions FIRST (using a .md skill-fragment, not .yaml — following jawcode's
convention), then domain, then derives components — which feed INTO the existing Round 0
topology enumeration rather than replacing it.

## Part 2 — Diff-level precision

### 1. NEW: `packages/.../jwc/skills/jaw-interview/catalog-discovery-axes.md`
jawcode uses sibling `.md` skill-fragments, not `.yaml` reference files. The catalog data
is encoded as a markdown document with fenced YAML blocks (the axis ontology), prefixed
with `kind: "skill-fragment"` metadata. Content = adapted version of the canonical catalog
focusing on the axis_order, design_methodology, and entry definitions.

### 2. NEW: `packages/.../jwc/skills/jaw-interview/auto-research-catalog.md`
A `kind: "skill-fragment"` prompt (following the auto-research-greenfield.md pattern) that
spawns a read-only architect to present catalog axis options for the current stage. Returns:
```json
{
  "status": "catalog_stage_complete",
  "stage": 1,
  "selections": { "mood": "mystical", "lightness": "dark", ... },
  "next_stage": 2,
  "derived_candidates": ["security.pii_protection"]
}
```

### 3. MODIFY: `packages/.../jwc/skills/jaw-interview/SKILL.md`
Insert between Phase 1 (init) and Round 0 (topology enumeration gate):

```markdown
### Phase 1.5 — Catalog Discovery (conditional)

When the initial idea is a vague product/domain request ("사주 앱 만들고 싶어") with no
prior codebase context (greenfield, no brownfield signals), activate catalog discovery
before the topology enumeration gate.

**Trigger**: `state.type === "greenfield"` AND initial idea matches product-creation pattern
(no file paths, no function names, no error descriptions — just a domain/product concept).

**Stages (design/UX LEADS — hard barrier, CATALOG-DESIGN-FIRST-01)**:
1. Design/UX — Product-Personality-Selection methodology (6 dials: mood/lightness/density/
   shape/typography/motion). Present options with trade-offs, then ask. ALL 6 required before
   advancing. Load options from `catalog-discovery-axes.md`.
2. Domain — app type selection. Seeds stage-3 derivation via `implies[]`.
3. Derived — surface backend entries whose `derived_from` matches chosen stage 1+2 entries,
   or whose `auto_activate_rules` keywords match the initial idea text.

**Output**: catalog selections stored in `state.catalog_discovery`. The derived component list
from stage 3 becomes the candidate list for Round 0 topology enumeration — the user confirms/
edits before the Socratic ambiguity loop begins.

**Ambiguity pre-seeding**: personality selection → pre-seed goal clarity; domain → constraint
clarity; derived architecture → context clarity. This gives the Socratic loop a non-1.0
starting ambiguity.

**Skip**: if the user wants standard Socratic flow or already specifies components, skip catalog
discovery and go straight to Round 0.
```

## Files touched
- NEW  `packages/.../jwc/skills/jaw-interview/catalog-discovery-axes.md`
- NEW  `packages/.../jwc/skills/jaw-interview/auto-research-catalog.md`
- MOD  `packages/.../jwc/skills/jaw-interview/SKILL.md`

## Verifier
- `grep -c 'CATALOG-DESIGN-FIRST-01' */jaw-interview/SKILL.md` → ≥1
- `grep -c 'catalog-discovery-axes' */jaw-interview/SKILL.md` → ≥1
- No `.yaml` files added (jawcode convention = `.md` fragments)
- `grep -cE 'cli-jaw|opencodex' */jaw-interview/SKILL.md` → 0
