---
created: 2026-09-02
status: active
tags: [pabcd-initiative, skills, codexclaw-backport, research, decisions]
---
# 002 Research Consolidation and Recorded Decisions

Closes the research half of the docs-only cycle. 001 measured the gap; this doc
records what the qualitative reads found, which findings survived verification,
and the four decisions that unblock the implementation cycles.

Investigation was delegated to three parallel read-only `grok-4.6` lanes (gap
inventory for this repository, translation inventory for `cli-jaw`, model-catalog
audit for `cli-jaw`), with every load-bearing claim re-verified in the main
session before it entered this document. Two claims did not survive that check —
recorded below, because a corrected finding is more useful than a clean one.

## The drift is bidirectional, and that reshapes the port

001 counted what this repository is missing. The qualitative read found the
converse: the `4e4db8e` harmonization pass left this repository **newer than
codexclaw** in several skills, so a bulk copy would regress it.

| Skill | Where this repository is ahead |
|---|---|
| `dev-architecture` | **full rule parity already.** Adds a blast-radius row, two monorepo split triggers, dated tool-role attribution, `eslint-plugin-boundaries` / Biome `noBarrelFile` rows |
| `dev-backend` | Node LTS sourcing, OTel maturity, Redis/Valkey licensing, tRPC v11, RFC 9745/8594 deprecation headers |
| `dev-security` | OWASP Top 10:2025 delta mode, ASVS 5.0.0 versioning, Agentic Top 10 2026 naming, slopsquatting checklist |
| `dev-data` | dbt Fusion/SQLMesh licensing nuance, Kafka 4.x KRaft, Airflow 3.x, pandas 3.x, lakehouse neutrality |
| `dev-scaffolding` | the `structure/` + `devlog/` default, which replaced codexclaw's `docs/` + `plans/` |
| `dev-testing` | §5.2/§5.3 pipeline template, §8 security detail, §10 change-type routing |
| `dev-frontend` | `references/stacks/react.md` (303L vs 264L) |

So `dev-architecture` is a `NOOP` for this unit — the first work-phase that can
honestly report one. Everything else is a **merge**, never a replace, and 060's
audit has to read the target side first rather than assuming staleness.

## An internal contradiction to fix while porting

codexclaw *relaxed* `UNIT-RESIDENCE-01` after this repository forked from it:

- codexclaw `dev/SKILL.md:48-50` — C0 patches (typo, config, one-line fix) are
  **exempt** from numbered implementation-unit records; C1 records in the owning
  unit **only when a unit already exists**.
- this repository, `skills/dev/SKILL.md:49-51` — the numbered record doc is
  "**mandatory for ALL work**".

The absolute form contradicts this repository's own `dev-pabcd:256-263`, which
says ceremony scales with work class. That is not codexclaw drift to import or
reject; it is a live inconsistency here, and 020 fixes it while touching the same
lines.

## The reference-file payload is where the volume actually is

Rule ids undercount the work by a wide margin. `dev-debugging` is two rules from
parity but missing **13 reference files, ~1165 lines** — the per-runtime
debugging guides (`node`, `python`, `rust`, `go`, `c-cpp`, `jvm`, `swift`,
`ruby`, `beam`, `js/nextjs-react`, `js/node-backend`, `js/vite-vitest`) plus
`tools/playwright.md`. Confirmed free of codexclaw vocabulary except two lines in
the Playwright file (a lineage note and a tool-name heading).

`dev-frontend/references/core/asset-requirements.md` is the single largest file
gap: **80 lines here against 506 upstream** — effectively a stub.

## Verification corrections

Two subagent findings were wrong in ways that would have caused damage.

### `DIVERGE-TIER-01` is not an upstream invention

Already recorded in 001. The first census read it as absent from codexclaw and
therefore a candidate for removal; it lives in `loop/SKILL.md` and
`loop/references/divergence-tiers.md`, outside the dev-family scope.
`gap-census.sh` now separates the two classes mechanically.

### The `cli-jaw` devlog numbering conflict runs the other way

The translation lane reported a hard contradiction: codexclaw mandates 3-digit
document prefixes (`000_`, `010_`) as STRICT, `cli-jaw`'s
`jaw-dev-pabcd/SKILL.md:163-164` documents 2-digit (`00_plan.md`,
`10_phase1-auth-module.md`), and therefore "a port that carries codexclaw's
numbering would make every existing cli-jaw devlog document a STRICT violation."

Measured instead of assumed: `cli-jaw`'s `devlog/_plan/` holds **492 three-digit
documents against 107 two-digit ones**, and the two-digit files are concentrated
in units from 2026-06 (`260610_*`, `260618_*`, `260621_*`) while every unit from
2026-08 onward is three-digit. The repository migrated; the rule text did not
follow.

The finding inverts. `cli-jaw`'s skill text is stale relative to `cli-jaw`'s own
practice, so porting codexclaw's 3-digit rule repairs the skill instead of
breaking the repository. This is the difference between reading two documents and
reading a document against the tree, and it is why a drift claim needs the tree.

**Correction, recorded rather than quietly fixed.** The first version of this
section said "all 18 unit directories use 3-digit prefixes, and not one file uses
2-digit", and that claim reached a commit message and two pull-request bodies
before it was rechecked. It came from a loop that listed unit directories and then
sampled only the most recent fifteen — every one of which is three-digit — and
generalized. The 107 two-digit files are real and sit in the units that loop never
looked at.

The conclusion survives and is better supported by the true numbers than by the
false ones: 492-to-107 with a clean date boundary is a migration, which is a
stronger argument for adopting three digits than "nothing uses two" would have
been. What does not survive is the absolute form, and the reason it slipped is
worth keeping: a per-directory loop that samples is not a census, and this is the
second time in this unit that shape produced a wrong claim (the first was the
`DIVERGE-TIER-01` scoping error in 001). Both times the fix was to widen the
measurement rather than to trust the pattern.

## Recorded decisions

Four questions were escalated rather than guessed. Answers, with what each one
changes:

**1. Attestation shape — do both.** `cli-jaw`'s attest parser accepts exactly
`from`, `to`, `did`, `checkOutput`, `exitCode` and silently drops
`planUnit`, `workPhaseId`, `auditOutput`, `auditVerdict`, `auditResidual`,
`testReceiptPath` (verified directly in `src/orchestrator/attestation.ts:21-32,
46-57`). So codexclaw's per-edge required-key table is false in `cli-jaw` today.
Decision: port `ATTEST-SHAPE-01` and `AUDIT-LOOP-01` as **discipline** carried in
the `did` narrative, with the skill stating plainly that the gate is form-only —
**and** open a separate change extending the parser to gate the audit fields, so
the rule becomes true rather than staying aspirational. The two are not
alternatives, and neither ecosystem has to be the only one that improves.

**2. Document numbering — 3-digit.** Port codexclaw's convention. Per the
correction above this fixes a stale rule rather than invalidating history.

**3. Commit discipline — port `DEV-GIT-COMMIT-01` as written.** Full authority
granted for this work, so the conflict with the parent-repository
"no proactive git actions" rule is resolved in favour of the rule as codexclaw
states it. `DEV-GIT-PUSH-01` never conflicted and ports unchanged.

**4. Scope — all of it, in roadmap order.** 010 through 070 here, then the
`cli-jaw` side. No triage pass; `NOOP` is reported per work-phase where parity
already exists (`dev-architecture` being the first).

## Not portable

Consolidated so each implementation cycle can check against one list rather than
re-deriving it. None of these crosses into `skills/`:

- **`cxc` CLI invocations** — `cxc orchestrate|loop|goalplan|map|receipt|
  review-round|chat|memory|doctor|serve|skill`. This repository's runtime-adapter
  block (`dev-pabcd/SKILL.md:10-17`) is where every command reference routes.
- **`.codexclaw/` paths** — `sessions/<id>.json`, `ledger.jsonl`,
  `interviews/<id>.jsonl`, `evidence/<session>/test-receipt.json`, `divergence/`.
- **Hook and loader internals** — `pabcd-state`, `SessionStart`,
  `UserPromptSubmit`, `PostToolUse`, `SubagentStop`, `handleStop`,
  `LOOP_ARM_DIRECTIVE`, `MAX_STOP_BLOCKS`, `PLUGIN_ROOT`, `coerceAttest`.
- **Host subagent API** — `spawn_agent`, `wait_agent`, `send_input`,
  `followup_task`, `close_agent`, `resume_agent`, `interrupt_agent`,
  `tool_search`, `request_user_input`, `update_plan`, `agent_type:"explorer"`,
  V1/V2 versioning. The explorer/worker **role** distinction is portable; the
  names are not.
- **Native tool ids in the browse/QA ladders** — `agbrowse`,
  `browser:control-in-app-browser`, `chrome:control-chrome`,
  `computer-use:computer-use`. The ladder *shape* is the rule; convert to
  capability tiers.
- **codexclaw `structure/` cross-references** — `00_philosophy.md`,
  `20_pabcd_dispatch_doctrine.md`, `60_native_capabilities.md`. Inline the
  substance or drop the pointer; a link the reader cannot open is worse than no
  link.
- **`DEV-SKILL-DISCOVERY-01`** and **`dev/references/skill-catalog.md`** — a
  specific external skill registry, clawhub/hermes resolution, "built-in
  codexclaw skills win name conflicts". Entirely registry mechanics.
- **`REVIEW-REMOVED-BACKEND-01`** — checks a codexclaw file for a codexclaw-
  specific list of retired search backends. The generic form ("review a policy
  doc for retired capabilities reappearing") is portable; the name list is not.
- **`TEST-PROMPT-SEAM-01`'s incident writeup** — names four codexclaw test files
  and an internal provenance dispute. Port the rule, the forbidden/allowed
  bullets, and the closing lesson; drop the incident.
- **`SCAF-SOT-01`'s branding** — retitle "Codexclaw-First Durable Docs" to
  "Existing-Convention-First Durable Docs"; the body is already generic.
- **`E1-E8` enforcement tiers** in `PLAN-BYPASS-NAMED-01` — an internal taxonomy
  defined in neither tree. Port the other four fields, or define the scale.
