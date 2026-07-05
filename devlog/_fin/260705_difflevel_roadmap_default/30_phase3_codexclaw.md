# 30_phase3 — Codexclaw port: DIFFLEVEL / PHASE-SPLIT / LEXICO / UNIT-RESIDENCE / SOT-SYNC + de-brand

Phase 3 of 4. Target repo: `/Users/jun/Developer/new/700_projects/codexclaw`.
All targets under `plugins/codexclaw/skills/` and one NEW reference file.

Files: 3 MODIFY, 1 NEW.

> **Line-number convention:** `~L` references are approximate guides from the snapshot used during planning; the B executor matches blocks by content, not line number. If a reference is stale, locate the content by its text.

Repo conventions honored:
- **Prefix digits**: codexclaw uses BOTH 2-digit (`00_`) and 3-digit (`000_`) doc
  prefixes historically. 3-digit dominates: 265 files in `_fin/` + `_plan/` vs 30
  two-digit. The latest units (260705) are exclusively 3-digit. This port LEGISLATES
  **3-digit prefixes** as the going-forward standard for codexclaw (the same default
  as the canonical `implementation-log.md`'s "pick ONE per repo" rule). Existing
  2-digit units are NOT renumbered.
- **Language**: English (repo language is English).
- **Deploy relationship**: `plugins/codexclaw/skills/` ships as part of the Codex
  plugin via `.codex-plugin/plugin.json` `"skills": "./skills/"`. No separate
  publish step; changes take effect on next Codex session load.
- **Naming**: skill names prefixed `cxc-` in frontmatter; file paths use the
  unprefixed directory name (`pabcd/`, `dev/`, `dev-scaffolding/`).
- **No external orchestrator**: codexclaw's PABCD is file-state + hook-driven,
  not server-driven. `orchestrate` commands map to `cxc orchestrate`.

| # | File | Blocks |
|---|------|--------|
| 1 | `skills/pabcd/SKILL.md` | 1.1-1.8 |
| 2 | `skills/dev-scaffolding/SKILL.md` | 2.1-2.9 |
| 3 | `skills/dev-scaffolding/references/implementation-log.md` | 3.1 (NEW) |
| 4 | `skills/dev/SKILL.md` | 4.1-4.3 |

---

# File 1 -- `skills/pabcd/SKILL.md`

## 1.1 Interview settles unit residence (~L29)

The current text settles TWO things (work class + loop archetype). The canonical
contract settles THREE (adds unit residence).

**Before:**

```
Plan. **INTERVIEW-CLASSIFY-01 (DEFAULT):** before P, settle both the work class
(`dev` §0.0) and the loop archetype (`cxc-loop` LOOP-ARCHETYPE-01) by asking whether
the verifier defines done or only better; discovering the archetype mid-loop is an
Interview miss, not a Build problem.
```

**After:**

```
Plan. **INTERVIEW-CLASSIFY-01 (DEFAULT):** before P, settle three things: the work
class (`dev` §0.0), the loop archetype (`cxc-loop` LOOP-ARCHETYPE-01) by asking
whether the verifier defines done or only better, and the **unit residence**
(UNIT-RESIDENCE-01, Work-Phase Loop below): which implementation unit
(`devlog/_plan/YYMMDD_slug/`) this work belongs to, an existing unit or a new one.
Discovering the archetype mid-loop is an Interview miss, not a Build problem.
```

## 1.2 PHASE-SPLIT-01 in Phases section (~L75, P bullet)

The P bullet currently says "Write a diff-level plan" but lacks the PHASE-SPLIT-01
dependency-ordering rule that forbids effort-based bucketing. Insert after the
existing P bullet text.

**Before (P bullet, line 75):**

```
1. **P — Plan**: Explore first (read real code, configs, docs). Write a diff-level plan: file change map, scope boundary (IN/OUT), and testable accept criteria. For C2+ plans, begin with a loop-spec header: Loop archetype; Trigger; Goal (user-visible outcome); Non-goals; Verifier (command/gate and what it measures); Stop condition; Memory artifact; Expected terminal outcomes; Escalation condition. HOTL goal plans also state the `cxc-loop` HOTL resource bounds. For open-ended optimization, include the divergence plan, deterministic selection rule, and telemetry schema; if the verifier only reports scalar outcome, instrumentation is B's first work item before candidates. Ground every decision in code you have read. No implementation yet. For broad or unfamiliar repos, include a compact tree, detected conventions, and which existing logs/docs you will reuse.
```

**After:**

```
1. **P — Plan**: Explore first (read real code, configs, docs). **Slice and order phases by dependency/architecture structure (STRICT, PHASE-SPLIT-01)** — the orthodox unlimited-time build order: foundations (schema, contracts, core data flow) → core capabilities → integration → hardening/polish — so each phase consumes the verified output of the previous one. Effort-based bucketing is FORBIDDEN: never split or order phases by estimated effort or payoff speed — no "quick win vs heavy" buckets, no impact/effort matrices, no time-boxed slices. Phase boundaries encode the system's build order, not the schedule. DB/API/UI/test work inside a phase are subtasks, not top-level phases by default, and every phase must still close with something independently verifiable (build, tests, or a demonstrable surface). Write a diff-level plan: file change map, scope boundary (IN/OUT), and testable accept criteria. For C2+ plans, begin with a loop-spec header: Loop archetype; Trigger; Goal (user-visible outcome); Non-goals; Verifier (command/gate and what it measures); Stop condition; Memory artifact; Expected terminal outcomes; Escalation condition. HOTL goal plans also state the `cxc-loop` HOTL resource bounds. For open-ended optimization, include the divergence plan, deterministic selection rule, and telemetry schema; if the verifier only reports scalar outcome, instrumentation is B's first work item before candidates. Ground every decision in code you have read. No implementation yet. For broad or unfamiliar repos, include a compact tree, detected conventions, and which existing logs/docs you will reuse.
```

## 1.3 Work-Phase Loop section: DIFFLEVEL-ROADMAP-01 + LEXICO-SPLIT-01 + UNIT-RESIDENCE-01 (~L101-107)

The existing "Work-Phase Loop" heading and multi-pass paragraph lack the three STRICT
rules. Insert new rule blocks between the "Invariant" paragraph and the loop/multi-pass
paragraph, and rewrite the multi-pass paragraph per the canonical wording.

**Before (lines 101-107):**

```
## Work-Phase Loop (multi-pass tasks)

**Terminology**: a *work-phase* is one outcome slice of the goal (e.g. "Phase 3: Management API"); a *PABCD-phase* is one letter P/A/B/C/D of a single cycle. They are not the same.

**Invariant — one work-phase = one full PABCD cycle.** Run P→A→B→C→D for a work-phase, close D (state → IDLE), then start the next work-phase at P. Do NOT run B for several work-phases back-to-back, and do NOT commit a work-phase straight out of B without passing C and D.

**Loop / multi-pass tasks**: a "loop"/"루프" request (or work too large for one cycle) runs as multiple PABCD passes — one per work-phase. Pre-plan the full slice map and scaffold per-phase decade docs (10_phase1, 20_phase2, ...) up front. The first pass MAY be a design-only PABCD pass (Phase 0): a code-free whole-system design/documentation cycle before the first implementation work-phase.
```

**After:**

```
## Work-Phase Loop (multi-pass tasks)

**Terminology**: a *work-phase* is one outcome slice of the goal (e.g. "Phase 3: Management API"); a *PABCD-phase* is one letter P/A/B/C/D of a single cycle. They are not the same.

**Invariant — one work-phase = one full PABCD cycle.** Run P→A→B→C→D for a work-phase, close D (state → IDLE), then start the next work-phase at P. Do NOT run B for several work-phases back-to-back, and do NOT commit a work-phase straight out of B without passing C and D.

### Implementation-Unit Documents

Full documentation routine (P concretizes the docs, A audits them as a hard gate, D
archives to `_fin/`, plus the mainstream design-doc/RFC translation table):
`dev-scaffolding/references/implementation-log.md`.

**Difflevel roadmap plan (STRICT, DIFFLEVEL-ROADMAP-01):** for any multi-phase unit
(2+ work-phases), the FIRST P — or the dedicated design-only Phase-0 pass — must
deliver the entire roadmap concretized: `000_plan.md` (objective, constraints,
dependency-ordered work-phase map) PLUS every phase's decade doc written to full
diff-level precision (exact paths, NEW/MODIFY/DELETE, before/after diffs) — each one
a copy-paste-executable PRD, not an outline. Scaffolding empty decade files to "fill
per cycle" does NOT satisfy this rule. Each later cycle's P starts from its
pre-written doc: re-verify it against the current codebase (stale check — earlier
phases may have moved lines, signatures, or files), amend the doc, then execute.
LOOP-CONTINUITY-01 applies on top.

**Lexicographic separation (STRICT, LEXICO-SPLIT-01):** every document in a unit
carries a numeric lexicographic prefix — bare semantic filenames (`PLAN.md`,
`DIFF_PLAN.md`, `PHASES.md`, `RCA.md`, an unnumbered `mvpplan/`-style folder) are an
A-phase FAIL, not a style nit. Research/spec material (000-range) and implementation
phase designs (decade ranges) are SEPARATE documents: no diffs inside a research
doc, no survey prose padding a phase doc — a document that mixes both fails the
audit.

**Unit residence (STRICT, UNIT-RESIDENCE-01):** every piece of development work
belongs to an implementation unit (`devlog/_plan/YYMMDD_slug/`). Ceremony scales
with class (PABCD Depth by Work Class below); residence does not. C0-C1 fast-path
work skips the PABCD ceremony but MUST leave a numbered record doc in its owning
unit — next free index in the matching decade, e.g. `040_hotfix_dropdown_crash.md`
— stating what changed, why the fast path applied (class call), and the
verification evidence. No owning unit → create a minimal unit folder holding only
that record. Interview settles residence before P (Interview Trigger above).

Devlog plan artifacts use decade-range numbering to separate concerns:

| Range | Purpose | Examples |
|-------|---------|----------|
| 000-009 | Research, specs, MOC | `000_plan.md`, `001_api_survey.md`, `002_competitor_analysis.md` |
| 010-019 | Phase 1 | `010_phase1_auth_module.md`, `011_phase1_db_schema.md` |
| 020-029 | Phase 2 | `020_phase2_frontend.md` |
| 030-039 | Phase 3 | ... |

Rules:
- 000-range durable research is **mandatory for C4**, and for C3 only when state must persist
  across turns/agents, public contract or architecture decisions need durable audit, or the
  repo already uses devlog planning for that task; optional for C0-C2 and
  low-persistence C3 (a response-level plan is enough — but the work still leaves its
  numbered record in a unit, UNIT-RESIDENCE-01).
- Default: sequential within decade (`000`, `001`, `002`...).
- Overflow (>10 docs in a range): use sub-index (`000_0_name.md`, `000_1_name.md`).
- NEVER use bare filenames like `PLAN.md`, `DIFF_PLAN.md`, `PHASES.md`, `RCA.md`.
- This repo uses 3-digit prefixes (`000_`, `010_`, `020_`). Do not mix with 2-digit.

**Loop / multi-pass tasks**: a "loop"/"루프" request (or work too large for one cycle) runs
as MULTIPLE PABCD passes — one per work-phase. Pre-plan the full slice map and WRITE
all per-phase decade docs (010_phase1, 020_phase2, ...) to diff-level up front
(DIFFLEVEL-ROADMAP-01) — scaffolding empty files is not pre-planning. Each
later cycle's P re-verifies its pre-written doc against the current codebase and
amends it before building. The first pass MAY be a design-only PABCD pass (Phase 0):
a code-free whole-system design/documentation cycle that produces exactly this
difflevel roadmap before the first implementation work-phase.
```

## 1.4 A-gate audit checklist (add items) (~L76, A bullet)

The A bullet currently does not check lexicographic or difflevel compliance. Append
two audit items.

**Before (A bullet, line 76):**

```
2. **A — Audit**: Adversarial, read-only review of the plan against the real codebase. Dispatch an independent reviewer (`spawn_agent`) — even a small/mini-model one — to challenge assumptions, find blockers (rollback gaps, missing callers, phantom constants), and verify references. Fold fixes back into the plan and record the verdict. No code changes. The `A>B` attest structurally requires `auditOutput` (the pasted tail of the reviewer's verdict) — a form-only bar: silently skipping the paste fails the gate, but the gate cannot verify the paste's provenance, so faithful execution (really dispatching the reviewer) remains the agent's obligation.
```

**After:**

```
2. **A — Audit**: Adversarial, read-only review of the plan against the real codebase. Dispatch an independent reviewer (`spawn_agent`) — even a small/mini-model one — to challenge assumptions, find blockers (rollback gaps, missing callers, phantom constants), and verify references. The reviewer also checks: new devlog phase documents use the numbered lexicographic filename convention; bare-named or research/implementation-mixed docs are a FAIL (LEXICO-SPLIT-01). Multi-phase units satisfy DIFFLEVEL-ROADMAP-01: every roadmap phase has a diff-level decade doc (no outline-only or missing phases), and the phase map is dependency-ordered, not effort-bucketed (PHASE-SPLIT-01). Fold fixes back into the plan and record the verdict. No code changes. The `A>B` attest structurally requires `auditOutput` (the pasted tail of the reviewer's verdict) — a form-only bar: silently skipping the paste fails the gate, but the gate cannot verify the paste's provenance, so faithful execution (really dispatching the reviewer) remains the agent's obligation.
```

## 1.5 Depth table C0-C1 Record cell (~L162)

**Before:**

```
| C0-C1 | None/inline | Optional | Direct fix | Smallest proof | One-line summary |
```

**After:**

```
| C0-C1 | None/inline | Optional | Direct fix | Smallest proof | One-line summary as a numbered record doc in the owning unit (UNIT-RESIDENCE-01) |
```

## 1.6 Stub note at end of existing "Jawdev Document Numbering" mention removal

No "Jawdev Document Numbering" heading exists in codexclaw's `pabcd/SKILL.md` (the
L12 port used a different heading scheme). No de-brand action needed in this file.
The Jawdev reference is only in `dev-scaffolding/SKILL.md` (block 2.6 below).

## 1.7 P phase MUST-include list: add SoT sync target (~L75, end of P bullet)

The P bullet's "broad or unfamiliar repos" sentence lists things to include but omits
the SOT-SYNC-01 sync target. Append it.

**Before (end of P bullet sentence):**

```
For broad or unfamiliar repos, include a compact tree, detected conventions, and which existing logs/docs you will reuse.
```

**After:**

```
For broad or unfamiliar repos, include a compact tree, detected conventions, which existing logs/docs you will reuse, and the SoT sync target (SOT-SYNC-01): which general source-of-truth doc (architecture/INDEX docs, or equivalent) this unit will patch in C — or, if the repo has none, the plan recommends creating one (dev-scaffolding §2.1).
```

## 1.8 C phase: add SOT-SYNC-01 step (~L78)

The C bullet lists verification actions but lacks the source-of-truth sync step.
Insert SOT-SYNC-01 between the main C sentence and the C-RENDER-GROUNDING-01 block.

**Before:**

```
4. **C — Check**: Run the real verification — build, typecheck, and targeted tests, plus adversarial review. Capture fresh command output as evidence. Do not claim pass without artifact-level proof.

   **DEFAULT (C-RENDER-GROUNDING-01):**
```

**After:**

```
4. **C — Check**: Run the real verification — build, typecheck, and targeted tests, plus adversarial review. Capture fresh command output as evidence. Do not claim pass without artifact-level proof.

   **SoT sync (DEFAULT, SOT-SYNC-01):** locate the repo's general source-of-truth
   docs (architecture/INDEX docs, or equivalent) — found in P, patched HERE so SoT
   and code never diverge silently; if the repo has none, recommend creating one
   (dev-scaffolding §2.1) in the D summary.

   **DEFAULT (C-RENDER-GROUNDING-01):**
```

---

# File 2 -- `skills/dev-scaffolding/SKILL.md`

## 2.1 Modular References table: add implementation-log row (~L20-23)

**Before:**

```
## Modular References

| File | When to Read | What It Covers |
|------|-------------|----------------|
| `references/api-docs.md` | API documentation generation | OpenAPI 3.1, developer portal, CI doc drift, SDK generation |
| `references/monorepo-tooling.md` | Setting up or optimizing monorepo builds | Turborepo vs Nx 2026 decision table, task graph for AI agents, CI optimization |
```

**After:**

```
## Modular References

| File | When to Read | What It Covers |
|------|-------------|----------------|
| `references/implementation-log.md` | C2+/multi-phase/cross-session work units | Full devlog routine: decade-numbered plan folders, P-concretize → A-audit → D-archive loop, mainstream design-doc/RFC mapping |
| `references/api-docs.md` | API documentation generation | OpenAPI 3.1, developer portal, CI doc drift, SDK generation |
| `references/monorepo-tooling.md` | Setting up or optimizing monorepo builds | Turborepo vs Nx 2026 decision table, task graph for AI agents, CI optimization |
```

> **Deliberate deviation (WARN 2):** the `When to Read` column triggers at C2+ rather than C3+. C2 work uses compact plans that still follow decade-numbering and unit residence; the reference teaches the convention at every depth, not just the full multi-phase routine. The full ceremony (DIFFLEVEL-ROADMAP-01, all-phase diff-level docs) remains gated at C3+/multi-phase per block 1.3.

## 2.2 SCAF-SOT-01 section: remove codexclaw-specific branding (~L54-62)

The `SCAF-SOT-01` block names "codexclaw" specifically, which is appropriate for a
codexclaw-internal skill. However the de-brand target is "Jawdev" -- and this section
does not contain Jawdev. No change needed for this block. (It is already
codexclaw-native.)

## 2.3 Section 2.1 title + intro: convert from opt-in to default (~L64-69)

**Before:**

```
## 2.1 Lightweight Source of Truth

Use this only when:
- The repo is immature, undocumented, or inconsistent; or
- The user explicitly asks for a project source-of-truth layout; or
- A broad change needs a durable plan/current-architecture record.
```

**After:**

```
## 2.1 Lightweight Source of Truth (implementation-unit devlog)

The implementation-unit devlog routine (`devlog/_plan/` units — `pabcd` §Work-Phase
Loop, UNIT-RESIDENCE-01) is the DEFAULT for any repo you do development work in — a
process rule, not a named style to be requested. Propose the `docs/`/`plans/`
architecture docs when:
- The repo is immature, undocumented, or inconsistent; or
- The user asks for a durable source-of-truth structure; or
- A broad change needs a durable plan/current-architecture record.
```

## 2.4 Source-of-truth method bullets: add dependency-ordering and difflevel (~L89-93)

**Before:**

```
Source-of-truth method:
- Split large work into phase-level documents instead of one huge plan when the repo already uses plan files.
```

**After:**

```
Implementation-unit devlog method:
- Split large work into phase-level documents instead of one huge plan —
  dependency-ordered (PHASE-SPLIT-01), ALL written to diff-level up front
  (DIFFLEVEL-ROADMAP-01; both defined in `pabcd`).
```

## 2.5 Numbering convention paragraphs: harden + remove optional framing (~L95-98)

**Before:**

```
When a repo already numbers planning documents by phase/decade, follow that local convention.
When no such convention exists, treat numbering as optional — never invent a heavy numbering system silently.
For codexclaw repos with decade numbering, point readers to the local `pabcd/SKILL.md`
Jawdev Document Numbering section.
```

**After:**

```
Phase document naming uses decade-range prefixes (LEXICO-SPLIT-01). For the canonical
table (000-009 research, 010-019 Phase 1, etc.), see `pabcd/SKILL.md`
Implementation-Unit Documents — that is the single source of truth. This repo uses
3-digit prefixes; do not mix with 2-digit.
```

## 2.6 Folder-approval gate: add unit-subfolder exemption (~L100-101)

**Before:**

```
Before creating any new source-of-truth folders, ask concisely: state that no durable docs were found,
show the proposed tree, give a specific recommendation, and confirm you will not create them without approval.
```

**After:**

```
Before creating any new source-of-truth folders, ask concisely: state that no durable docs were found,
show the proposed tree, give a specific recommendation, and confirm you will not create them without approval.
This gate governs INTRODUCING the convention to a repo (the first `devlog/` or source-of-truth structure);
once `devlog/_plan/` exists, creating unit subfolders — including the minimal record unit mandated by
UNIT-RESIDENCE-01 — is routine and needs no approval dialogue.
```

## 2.7 Phase docs naming table row (~L185-186)

**Before:**

```
| Phase docs          | optional numbered docs when the repo already uses them | `00_plan.md`, `10_phase1_build.md` |
```

**After:**

```
| Phase docs          | decade-prefixed `NNN_slug.md`, `000_*` is the index (LEXICO-SPLIT-01) | `000_plan.md`, `010_phase1_build.md` |
```

## 2.8 Planning Documentation section: harden with LEXICO-SPLIT-01 (~L276-278)

**Before:**

```
### Planning Documentation
1. Reuse the repo's existing planning/doc archive pattern when one exists
2. Each plan entry should capture: title, date, what changed, why, evidence paths
3. Cross-reference related plan entries within the same work folder when helpful
```

**After:**

```
### Planning Documentation
1. Follow decade numbering (`pabcd/SKILL.md` Implementation-Unit Documents, LEXICO-SPLIT-01): 000-009 research, 010-019 phase 1, etc.
2. Each plan entry should capture: title, date, what changed, why, evidence paths
3. Cross-reference related plan entries within the same work folder when helpful
```

## 2.9 Section 2.1: add SOT-SYNC-01 paragraph (~L88, after ADR paragraph)

The canonical §2.1 contains a SOT-SYNC-01 paragraph between the ADR/reuse paragraph
and the method bullets. codexclaw's §2.1 lacks it. Insert between the ADR line and
the method header (which block 2.4 has already renamed to "Implementation-unit devlog
method:").

**Before (after block 2.4 is applied):**

```
decision that is hard to reverse, surprising without context, or has a real tradeoff.

Implementation-unit devlog method:
```

**After:**

```
decision that is hard to reverse, surprising without context, or has a real tradeoff.

**SoT sync (DEFAULT, SOT-SYNC-01):** before patching a repo, FIND its general
source-of-truth docs first (architecture/INDEX docs, or equivalent)
and read them; any unit that changes architecture, contracts, or structure patches
the SoT doc in the SAME unit (C gate, `pabcd` C phase). If the repo has no SoT doc,
recommend creating one — once, via the proposal flow above — rather than silently
working without a source of truth.

Implementation-unit devlog method:
```

---

# File 3 -- `skills/dev-scaffolding/references/implementation-log.md` (NEW)

## 3.1 Complete new file

**Insertion point:** New file at
`plugins/codexclaw/skills/dev-scaffolding/references/implementation-log.md`.

**Content:**

```markdown
# Implementation Log (devlog) Routine — the documentation loop inside PABCD

Canonical spec for the per-implementation-unit documentation routine that rides the
PABCD cycle. Companion to `pabcd/SKILL.md` (numbering) and
`dev-scaffolding/SKILL.md` §2.1 (folder proposal rules). Read before any development
work: unit residence is universal (UNIT-RESIDENCE-01) — the full routine below is for
C2+/multi-phase work; C0-C1 leaves a numbered record doc (see the last section).

## The unit: one implementation unit = one plan folder

```
devlog/
  _plan/
    YYMMDD_slug/          <- one implementation unit (not one issue, not one commit)
      000_plan.md         <- master plan: objective, constraints, work-phase map
      001_research_*.md   <- research/spec docs (000-009 range)
      010_phase1_*.md     <- phase 1 design at diff-level precision
      020_phase2_*.md     <- phase 2 ...
  _fin/                   <- completed units move here (closure record kept, not deleted)
```

Numbering: decade ranges separate concerns — `000-009` research/specs/MOC, `010-019`
phase 1, `020-029` phase 2, and so on. This repo standardizes on three-digit prefixes
(`000_`, `010_`, `020_`). Never bare semantic filenames (`PLAN.md`, `RCA.md`) — the
numeric prefix is the ordering and the audit trail.

## How the routine rides PABCD (the loop)

| Phase | Documentation action | Gate |
|-------|---------------------|------|
| P | CONCRETIZE: write `000_plan.md` (objective, measured baseline, dependency-ordered work-phase map, risks) + research docs `001+`; decade docs for **EVERY roadmap phase** at **diff-level precision** (exact paths, NEW/MODIFY/DELETE, before/after for MODIFY) — DIFFLEVEL-ROADMAP-01 | plan exists as files, not chat |
| A | AUDIT THE DOCS: an independent reviewer checks the plan docs — paths/signatures real, research coverage complete, phases sized, no ownership violations, no contradictions vs research | FAIL → fix docs → re-audit |
| B | Implementation cites the doc it executes; deviations are edited back into the doc BEFORE coding past them | doc and code never diverge silently |
| C | Gate results (commands + tails) recorded into the unit; general SoT docs patched to match the change (SOT-SYNC-01 — recommend creating one if absent) | evidence lives next to the plan |
| D | Attestation/summary appended to `000_plan.md`; on unit completion the folder moves `_plan/` → `_fin/` | durable closure record |

Multi-cycle units: one full PABCD per work-phase; ALL phase design docs are written
to diff-level in the FIRST P (or the design-only Phase-0 pass) —
DIFFLEVEL-ROADMAP-01. P of each later cycle re-verifies its pre-written doc against
the current codebase (stale check) and amends it BEFORE building; it never writes
the doc fresh mid-unit. The attestation log in `000_plan.md` is the continuity spine
— each new P quotes the previous D conclusion from it (see `pabcd` LOOP-CONTINUITY-01).

## Mapping to mainstream developer practice (translation table)

This routine is NOT an issue tracker. Issues are the industry's unit of *tracking*
(small, cheap, closable); this is the industry's unit of *thinking* — the design-doc
lineage. Mature orgs run BOTH and link them. If a collaborator says "devlog isn't
standard", translate:

| This routine | Mainstream equivalent |
|--------------|----------------------|
| `_plan/YYMMDD_slug/` unit folder | Design doc / RFC per feature (Google design docs, Rust RFCs, PEPs) |
| `000-009` research docs | RFC "Motivation / Prior art" sections |
| Diff-level phase docs | Detailed design; kernel patch-series cover letter |
| A-phase doc audit | Design review / RFC final-comment-period — review BEFORE code |
| Evidence in C, attestation in D | CI gate records + review sign-off |
| `_fin/` closure record | Shipped postmortem + changelog entry |
| Hard-to-reverse decisions | ADR (see `dev-scaffolding` §2.1 — separate, immutable) |
| Issue/ticket | Still useful: one issue per unit LINKING to the folder; sub-issues for tracking granularity |

Two deliberate differences from common practice, kept on purpose:
1. **Diff-level precision in the plan** — most design docs stop at architecture;
   agents execute better from exact-path plans, and the A audit becomes mechanical.
2. **Docs gate execution** (A before B) — in many teams design review is advisory;
   here it is a hard gate because the executor (an agent) will otherwise
   confidently build from a flawed plan.

## Ceremony scales; residence does not

Every piece of work lands in an implementation unit (UNIT-RESIDENCE-01). The full
routine above (master plan + all-phase diff-level docs + doc audit) is mandatory for
C4, for any multi-phase unit regardless of class, and for C3 when state must persist
across turns/agents or contracts/architecture need a durable audit trail. C0-C1
fast-path work skips the ceremony but still leaves a numbered record doc in its
owning unit (what changed, why the fast path applied, verification evidence);
create a minimal unit folder if none exists. Over-documenting small work is process
slop — but "small" scales the ceremony down, never the record away.
```

---

# File 4 -- `skills/dev/SKILL.md`

## 4.1 Fast-path keep bullet: add UNIT-RESIDENCE-01 (~L44)

**Before:**

```
- Keep: §3 verification gate, §4 change documentation when a worklog/changelog file is provided, §5 safety rules (imports/exports), §7.2 static analysis
```

**After:**

```
- Keep: §3 verification gate, §4 change documentation — including the numbered
  record doc in the owning implementation unit, mandatory for ALL work
  (UNIT-RESIDENCE-01, `pabcd` Implementation-Unit Documents), §5 safety rules (imports/exports), §7.2 static analysis
```

## 4.2 Convention discovery: decade numbering note (~L287)

**Before:**

```
- If the repo already uses numbered phase documents, preserve that numbering scheme; decade-range numbering is an optional convention, not a universal rule
```

**After:**

```
- Devlog phase documents use decade-range numbering (000-009 research, 010-019 phase 1, ...); never bare `PLAN.md`/`PHASES.md`/`RCA.md` (LEXICO-SPLIT-01). Full convention: `pabcd`.
```

## 4.3 Modular Development phase doc rule (~L345)

**Before:**

```
- If the repo already uses numbered phase or planning documents, preserve the existing numbering/naming convention. Do not invent generic filenames like `PLAN.md`, `PHASES.md`, or `RCA.md` when the repo already has a clear pattern.
```

**After:**

```
- Devlog phase documents use decade-range numbering (LEXICO-SPLIT-01, `pabcd` Implementation-Unit Documents). Never use bare filenames like `PLAN.md`, `PHASES.md`, or `RCA.md`.
```

---

## De-branding verification

After the port, the only "Jawdev" reference in `plugins/codexclaw/skills/` was on
line 98 of `dev-scaffolding/SKILL.md` (block 2.5 above). The After text removes it
entirely. No other skills files contain "Jawdev".

Residual "Jawdev" in codexclaw outside the skill files:
- `.codexclaw/ledger.jsonl` (historical transition evidence) -- append-only, not edited.
- `.omo/evidence/` (historical review) -- archival, not edited.
These are data artifacts, not prompt/rule surfaces, and are out of scope.

---

## Verification (C gate for this phase)

Run from repo root `/Users/jun/Developer/new/700_projects/codexclaw`:

```bash
# De-brand check
grep -ric "jawdev" plugins/codexclaw/skills/             # expect 0

# Rule tag presence in pabcd
grep -c "DIFFLEVEL-ROADMAP-01" plugins/codexclaw/skills/pabcd/SKILL.md    # expect >=2
grep -c "LEXICO-SPLIT-01"      plugins/codexclaw/skills/pabcd/SKILL.md    # expect >=2
grep -c "UNIT-RESIDENCE-01"    plugins/codexclaw/skills/pabcd/SKILL.md    # expect >=3
grep -c "PHASE-SPLIT-01"       plugins/codexclaw/skills/pabcd/SKILL.md    # expect >=1
grep -c "SOT-SYNC-01"         plugins/codexclaw/skills/pabcd/SKILL.md    # expect 2

# Scaffold rule tags
grep -c "UNIT-RESIDENCE-01" plugins/codexclaw/skills/dev-scaffolding/references/implementation-log.md  # expect >=2
grep -c "UNIT-RESIDENCE-01" plugins/codexclaw/skills/dev-scaffolding/SKILL.md   # expect >=2
grep -c "UNIT-RESIDENCE-01" plugins/codexclaw/skills/dev/SKILL.md               # expect 1
grep -c "LEXICO-SPLIT-01"  plugins/codexclaw/skills/dev-scaffolding/SKILL.md    # expect >=2
grep -c "SOT-SYNC-01"     plugins/codexclaw/skills/dev-scaffolding/SKILL.md    # expect 1
grep -c "SOT-SYNC-01"     plugins/codexclaw/skills/dev-scaffolding/references/implementation-log.md  # expect 1

# Anti-regression: old phrasing removed
grep -rn "fill per cycle"       plugins/codexclaw/skills/   # expect 1 (the prohibition sentence in pabcd/SKILL.md only)
grep -rn "scaffold per-phase"   plugins/codexclaw/skills/   # expect 0 hits
grep -rn "optional.*numbering"  plugins/codexclaw/skills/dev-scaffolding/SKILL.md  # expect 0 hits

# New file exists
test -f plugins/codexclaw/skills/dev-scaffolding/references/implementation-log.md && echo OK || echo MISSING

# Build/test gate (B executor MUST run these)
npm run build        # expect exit 0
npm test             # expect exit 0 (all component + hook + gui tests pass)
```

**Note on "fill per cycle" self-hit:** the single expected hit IS the prohibition
sentence (`Scaffolding empty decade files to "fill per cycle" does NOT satisfy this
rule.`) in `pabcd/SKILL.md`. To verify no OTHER usage exists, pipe through
`grep -v "does NOT satisfy"` and confirm 0 residual hits.

Plus read-back: every After block matches the file verbatim; no other lines changed.

---

## Deploy/sync note

The patched files under `plugins/codexclaw/skills/` are the ONLY copies. They ship
directly via the Codex plugin loader (`plugin.json` -> `"skills": "./skills/"`).
There is no separate publish, build, or distribution step for skill markdown files.
The `references/implementation-log.md` NEW file is automatically discoverable by the
skill loader because it sits under the skill's directory tree.

After applying, run `npm run build && npm test` to confirm no hook/component regression.
No `npm publish` or remote push is part of this phase.
