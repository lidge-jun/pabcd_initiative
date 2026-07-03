# Phase 2 — Interview section update (design/UX-first catalog_discovery mode)

## Part 1 — Plain explanation

We modify the existing Interview section in `skills/dev-pabcd/SKILL.md` to add two
sub-modes: **catalog_discovery** (present the option map, design/UX first) and
**configurator** (compile selections into a spec). The design-first ordering is wired
directly to the dev-uiux-design Product-Personality-Selection methodology.

## Part 2 — Diff-level precision

### MODIFY: `skills/dev-pabcd/SKILL.md` (§1, bold-lead paragraph AFTER INTERVIEW-DIVERGE-01, ~line 53)

Insert a bold-lead paragraph matching §1's existing style (NOT a `### §1.2` heading — audit
fix #4). Content (revised per Phase-2 audit cxr-mr5d3n7i-wsw402, GATE was REJECT):

```markdown
**Catalog Discovery sub-mode** (DEFAULT, INTERVIEW-CATALOG-01 / CATALOG-DESIGN-FIRST-01):
when the user names a vague domain but not features ("사주 앱 만들고 싶어", "뭘 만들지 모르겠어"),
they cannot choose from options they have never seen (the strong form of INTERVIEW-TEACH-01).
Enter `catalog_discovery` and present the option ontology in `references/catalog-discovery.yaml`.

*Design/UX LEADS — hard barrier.* Iterate `axis_order` by ascending `stage`; do NOT present a
stage until every `required` entry of all earlier stages is answered. Stage 1 is design, so all
six design dials (mood, lightness, density, shape, typography, motion), each `required: true`,
MUST be answered before any Stage 2 (domain) or Stage 3 (feature/data/security/ops/cost) question
appears. This is the load-bearing invariant — backend is asked on top of design, never before it.

*Design methodology — Product-Personality Selection first* (`design_methodology.primary`, from
dev-uiux-design): for each design dial show its `question_options` (labels + trade-offs) anchored
on familiar products, then ask (present-then-ask, not confirm-what-they-said); refine via the
declared `followups` (Korean-adjective→token, reference discovery, Design Read).

*Deriving the backend questions* — two matching paths populate Stage 3 from earlier answers, never a
flat list: (a) **structural** — a chosen Stage-2 domain entry's `implies[]` plus each Stage-3 entry's
`derived_from` (resolve `implies[]` transitively); (b) **keyword** — scan the user's INITIAL free-text
request against Stage-3 `auto_activate_rules` (e.g. "사주"/"생년월일" pre-activates
`security.pii_protection`). Confirm high-impact activations; the catalog is a DATA STRUCTURE — do not
invent entries not in it.

*Configurator step.* Once selections are complete, compile them (with resolved `implies[]` chains)
into a spec: PRD sections, an MVP cut ordered by `cost_class`, a risk register of every
`risk_class: high` entry, and a PABCD plan seed carrying the work class + loop archetype from
INTERVIEW-CLASSIFY-01.

*Scope.* The YAML encodes derivation INPUTS + dependency metadata; this prose is the agent
procedure that reads it. Automated runtime filtering is out of scope (it would escalate to code).
```

Audit fixes folded: #1 hard `axis_order` barrier wording; #2 dropped `conflicts[]` (not in YAML);
#4 bold-lead paragraph not `§1.2` heading; #5 correct semantics — Stage-2 seeds via
`implies`/`derived_from` (structural), `auto_activate_rules` = keyword match on the INITIAL query.

### Verifier (Phase 2)
- `grep -c "CATALOG-DESIGN-FIRST-01" skills/dev-pabcd/SKILL.md` → ≥1
- `grep -c "catalog-discovery.yaml" skills/dev-pabcd/SKILL.md` → ≥1
- `grep -cE "cli-jaw|codexclaw" skills/dev-pabcd/SKILL.md` → 0 (agent-neutral; baseline 0)
- Prose check: "hard barrier" + "MUST be answered before" present (design-first barrier)
- Field fidelity: every backticked field name in the block exists in catalog-discovery.yaml
  (no `conflicts`)
