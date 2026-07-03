# Phase 2 — Interview section update (design/UX-first catalog_discovery mode)

## Part 1 — Plain explanation

We modify the existing Interview section in `skills/dev-pabcd/SKILL.md` to add two
sub-modes: **catalog_discovery** (present the option map, design/UX first) and
**configurator** (compile selections into a spec). The design-first ordering is wired
directly to the dev-uiux-design Product-Personality-Selection methodology.

## Part 2 — Diff-level precision

### MODIFY: `skills/dev-pabcd/SKILL.md` (Interview section, after INTERVIEW-TEACH-01)

Insert a new `### §1.2 Interview Sub-modes` block. Content:

```markdown
### §1.2 Interview Sub-modes

Interview operates in one of three sub-modes, selected by user's knowledge level:

**Clarification** (default, existing): user already knows roughly what they want.
Questions structure goals, constraints, success criteria.

**Catalog Discovery** (`catalog_discovery`): user does not know the option space
(e.g. "사주 앱 만들고 싶어"). The interviewer presents a versioned option catalog
(`references/catalog-discovery.yaml`) in explicit stage order:

1. **Stage 1 — Design/UX** (ALWAYS first, most important): use Product-Personality-Selection
   (dev-uiux-design) as step-1 methodology. Present the 6 design dials (mood, lightness,
   density, shape, typography, motion) with show-then-ask flow: options + trade-offs,
   then question. Map answers to design tokens.
2. **Stage 2 — Domain** (app type): present domain options relevant to the user's stated
   interest. Domain choice seeds stage-3 derived entries via `auto_activate_rules`.
3. **Stage 3 — Derived axes** (feature, data, security, ops, cost): present ONLY entries
   whose `derived_from` or `auto_activate_rules` match the user's stage 1+2 answers.
   Do NOT dump a flat list of all entries.

Entry rules:
- Design/UX questions are asked FIRST in every catalog_discovery session — this is the
  load-bearing invariant (DEFAULT, CATALOG-DESIGN-FIRST-01).
- `implies[]` chains are resolved transitively — if A implies B implies C, all three
  are selected when A is chosen.
- `conflicts[]` are flagged before the user commits — never silently resolved.
- The catalog is a DATA STRUCTURE (`references/catalog-discovery.yaml`), not per-session
  improvisation — do not invent entries not in the catalog.

**Configurator**: after catalog_discovery selections are complete, compile into:
- PRD (functional + non-functional requirements from selected entries)
- MVP cut (sort by cost_class, cut at the user's stated budget/timeline)
- Risk register (all risk_class=high entries)
- PABCD plan seed (work class from INTERVIEW-CLASSIFY-01 + loop archetype)

Sub-mode entry heuristic:
- User states a concrete feature/goal → Clarification (existing)
- User states a vague domain with no tech specifics → Catalog Discovery
- Explicit user request for either mode → honor it
```

### Verifier (Phase 2)
- `grep -c "CATALOG-DESIGN-FIRST-01" skills/dev-pabcd/SKILL.md` → ≥1
- `grep -c "catalog-discovery.yaml" skills/dev-pabcd/SKILL.md` → ≥1
- `grep -cE "cli-jaw|codex|codexclaw" skills/dev-pabcd/SKILL.md` → 0 (agent-neutral)
- Prose check: "ALWAYS first" appears in the design/UX stage description
