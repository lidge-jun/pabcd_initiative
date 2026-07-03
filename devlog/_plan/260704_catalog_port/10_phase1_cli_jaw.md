# Phase 1 — cli-jaw port

## Part 1 — Plain explanation
cli-jaw's Interview mode (I-state in the FSM) gets a "Catalog Discovery" sub-mode.
When a user says "사주 앱 만들고 싶어", the interview presents design choices FIRST
(using the catalog YAML), then domain, then derives backend questions — instead of
jumping into generic Socratic questioning. The catalog YAML goes into skills_ref,
the I-state prompt gets a new section, and the OrcContext type gets catalog fields.

## Part 2 — Diff-level precision

### 1. NEW: `skills_ref/dev-pabcd/references/catalog-discovery.yaml`
Create `references/` dir under `skills_ref/dev-pabcd/`, copy the canonical
`catalog-discovery.yaml` with ONE adaptation: add a cli-jaw header comment noting
"Adapted port from pabcd_initiative canonical — see README.md port rule."

### 2. MODIFY: `src/orchestrator/state-machine.ts`

**a. OrcContext.interview type (line ~83)**
Add 3 optional fields inside the existing `interview?` block:
```typescript
  catalogMode?: 'active' | 'completed' | 'skipped';
  catalogStage?: 1 | 2 | 3;
  catalogSelections?: Record<string, unknown>;
```

**b. STATE_PROMPTS.I (after line ~418, before closing backtick)**
Append a new section inside the existing I-state prompt string:
```markdown
## Catalog Discovery Sub-Mode (INTERVIEW-CATALOG-01)

When the user names a vague domain but no features ("사주 앱 만들고 싶어", "앱 만들고 싶어"),
enter catalog_discovery. Load the option ontology from `skills_ref/dev-pabcd/references/catalog-discovery.yaml`.

**Hard barrier — design/UX LEADS.** Iterate `axis_order` ascending by `stage`. Do NOT present
a stage until every `required` entry of all earlier stages is answered:
- Stage 1 (design): all 6 dials (mood/lightness/density/shape/typography/motion) via
  Product-Personality-Selection. Present `question_options` with trade-offs, then ask.
- Stage 2 (domain): app type selection.
- Stage 3 (derived): surface via `derived_from` + `auto_activate_rules` keyword scan on
  the user's initial request. Never dump a flat list.

Configurator: compile selections + resolved `implies[]` into PRD sections / MVP cut by
`cost_class` / risk register (every `risk_class: high`) / PABCD plan seed.

Entry heuristic: concrete feature/goal → standard Clarification; vague domain → Catalog Discovery.
```

**c. getPrefix() / buildPrefixForState() (line ~267)**
Add conditional catalog-stage perspective after the existing perspective rotation:
```typescript
if (ctx?.interview?.catalogMode === 'active') {
  const stage = ctx.interview.catalogStage || 1;
  const stageLabels = { 1: 'DESIGN/UX', 2: 'DOMAIN', 3: 'DERIVED' };
  prefix += `\n[Catalog Discovery Stage ${stage}: ${stageLabels[stage] || 'UNKNOWN'} — design-first barrier active]`;
}
```

### 3. MODIFY: `src/prompt/templates/orchestration.md`

Around line 49 (after "Interview operating detail arrives in the I-state prompt on entry"),
add one bullet:
```markdown
- Interview has a **Catalog Discovery** sub-mode (`INTERVIEW-CATALOG-01`) for product/feature
  work where the user doesn't know the option space. It uses a staged design-first ontology
  (`skills_ref/dev-pabcd/references/catalog-discovery.yaml`): design/UX choices → domain → derived
  backend questions. See I-state prompt for full rules.
```

## Files touched
- NEW  `skills_ref/dev-pabcd/references/catalog-discovery.yaml`
- MOD  `src/orchestrator/state-machine.ts` (3 insertion points)
- MOD  `src/prompt/templates/orchestration.md` (1 bullet)

## Verifier
- `npx tsc --noEmit` passes (TypeScript compiles)
- `grep -c 'INTERVIEW-CATALOG-01' src/orchestrator/state-machine.ts` → ≥1
- `grep -c 'catalog-discovery.yaml' src/orchestrator/state-machine.ts` → ≥1
- `grep -c 'Catalog Discovery' src/prompt/templates/orchestration.md` → ≥1
- `grep -cE 'jawcode|codexclaw|opencodex' src/orchestrator/state-machine.ts` → 0
- catalog YAML exists and parses
