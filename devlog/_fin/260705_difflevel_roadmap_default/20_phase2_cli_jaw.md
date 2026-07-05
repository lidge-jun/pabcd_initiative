# 20_phase2 — cli-jaw port: de-brand + DIFFLEVEL / PHASE-SPLIT / LEXICO / UNIT-RESIDENCE / SOT-SYNC

Phase 2 of 4. Target repo: `/Users/jun/Developer/new/700_projects/cli-jaw`.

Files: 12 MODIFY, 1 MODIFY (test rename + rewrite), 0 NEW, 0 DELETE.

**Repo conventions honored:**
- Two-digit decade numbering (cli-jaw uses `00_`, `10_` consistently).
- TypeScript string literals in source (`src/`) require `npm run build` after edit.
- `skills_ref/` is the in-repo skill copy; it deploys to `~/.cli-jaw/skills_ref/` at
  install time. Post-B sync note at the bottom covers this.
- Test file naming: `tests/unit/<name>.test.ts`.
- Build gate: `npx tsc --noEmit` + `npm test` + `npm run gate:all`.

| # | File | Blocks | Type |
|---|------|--------|------|
| 1 | `skills_ref/dev-pabcd/SKILL.md` | 1.1-1.8 | MODIFY |
| 2 | `skills_ref/dev-scaffolding/references/implementation-log.md` | 2.1-2.5 | MODIFY |
| 3 | `skills_ref/dev-scaffolding/SKILL.md` | 3.1-3.11 | MODIFY |
| 4 | `skills_ref/dev/SKILL.md` | 4.1-4.3 | MODIFY |
| 5 | `src/orchestrator/state-machine.ts` | 5.1-5.4 | MODIFY |
| 6 | `src/prompt/builder.ts` | 6.1 | MODIFY |
| 7 | `src/workflows/planaudit.ts` | 7.1 | MODIFY |
| 8 | `src/prompt/templates/a1-system.md` | 8.1 | MODIFY |
| 9 | `src/cli/types.ts` | 9.1-9.2 | MODIFY (de-brand type literals) |
| 10 | `skills_ref/goal/SKILL.md` | 10.1 | MODIFY |
| 11 | `tests/unit/jawdev-skill-contract.test.ts` | 11.1 | MODIFY (rename + de-brand) |
| 12 | `structure/prompt_basic_B.md` | 12.1-12.2 | MODIFY (de-brand architecture doc) |
| 13 | `structure/INDEX.md` | 13.1 | MODIFY (de-brand architecture doc) |

---

# File 1 — `skills_ref/dev-pabcd/SKILL.md`

## 1.1 §1 Interview settles unit residence (~L30-34)

**Before:**

```
**Interview MUST settle two classifications before P** (DEFAULT, INTERVIEW-CLASSIFY-01):
the work class (dev §0.0) and the **loop archetype** (§11.4). Ask: "does a verifier
define done for this work, or only better?" This applies in HITL and goal mode alike.
If the archetype is discovered only after candidates have already been burned, treat
that as an Interview failure, not a Build failure.
```

**After:**

```
**Interview MUST settle three things before P** (DEFAULT, INTERVIEW-CLASSIFY-01):
the work class (dev §0.0), the **loop archetype** (§11.4) — ask "does a verifier
define *done* for this work, or only *better*?" — and the **unit residence**
(UNIT-RESIDENCE-01, §3.1): which implementation unit (`devlog/_plan/YYMMDD_slug/`)
this work belongs to, an existing unit or a new one. This applies in HITL and goal
mode alike. An archetype discovered mid-loop — after candidates have already been
burned — is an Interview failure, not a Build failure.
```

## 1.2 §3 P phase-design paragraph → PHASE-SPLIT-01 (~L122-130)

**Before:**

```
Design phases before mapping them to PABCD. A phase should normally be a user-visible
or consumer-visible outcome unit: "create an item", "edit an item", "share a report",
or "compare three runnable prototypes". DB/API/UI/test work are subtasks inside that
outcome, not top-level phases by default. A simple task can finish in one PABCD with
several small phases; larger work splits into multiple PABCD passes — one full
P→A→B→C→D per work-phase, closed by D and re-entered at P for the next work-phase (see
Terminology / Rule 4). Layer-only phases are allowed only when independently verifiable and
explicitly justified. Do not plan a whole database/API foundation as one PABCD before any
usable outcome exists.
```

**After:**

```
Design phases before mapping them to PABCD. **Slice and order phases by
dependency/architecture structure (STRICT, PHASE-SPLIT-01)** — the orthodox
unlimited-time build order: foundations (schema, contracts, core data flow) → core
capabilities → integration → hardening/polish — so each phase consumes the verified
output of the previous one. DB/API/UI/test work inside a phase are subtasks, not
top-level phases by default, and every phase must still close with something
independently verifiable (build, tests, or a demonstrable surface). Effort-based
bucketing is FORBIDDEN: never split or order phases by estimated effort or payoff
speed — no "quick win vs heavy" buckets, no impact/effort matrices, no time-boxed
slices. Phase boundaries encode the system's build order, not the schedule. A simple
task can finish in one PABCD with several small phases; larger work splits into
multiple PABCD passes — one full P→A→B→C→D per work-phase, closed by D and
re-entered at P for the next work-phase (see Terminology / Rule 4).
```

## 1.3 §3.1 rename + three new STRICT rules (~L153-175)

**Before (heading + intro):**

```
### §3.1 Jawdev Document Numbering

Full documentation routine (P concretizes the docs, A audits them as a hard gate, D
archives to `_fin/`, plus the mainstream design-doc/RFC translation table):
`dev-scaffolding/references/implementation-log.md`.

Devlog plan artifacts use decade-range numbering to separate concerns:
```

**After (heading + intro + three inserted rule blocks):**

```
### §3.1 Implementation-Unit Documents

Full documentation routine (P concretizes the docs, A audits them as a hard gate, D
archives to `_fin/`, plus the mainstream design-doc/RFC translation table):
`dev-scaffolding/references/implementation-log.md`.

**Difflevel roadmap plan (STRICT, DIFFLEVEL-ROADMAP-01):** for any multi-phase unit
(2+ work-phases), the FIRST P — or the dedicated design-only Phase-0 pass (§5) —
must deliver the entire roadmap concretized: `00_plan.md` (objective, constraints,
dependency-ordered work-phase map) PLUS every phase's decade doc written to full
diff-level precision (exact paths, NEW/MODIFY/DELETE, before/after diffs) — each one
a copy-paste-executable PRD, not an outline. Scaffolding empty decade files to "fill
per cycle" does NOT satisfy this rule. Each later cycle's P starts from its
pre-written doc: re-verify it against the current codebase (stale check — earlier
phases may have moved lines, signatures, or files), amend the doc, then execute.
LOOP-CONTINUITY-01 (§10) applies on top.

**Lexicographic separation (STRICT, LEXICO-SPLIT-01):** every document in a unit
carries a numeric lexicographic prefix — bare semantic filenames (`PLAN.md`,
`DIFF_PLAN.md`, `PHASES.md`, `RCA.md`, an unnumbered `mvpplan/`-style folder) are an
A-phase FAIL, not a style nit. Research/spec material (00-range) and implementation
phase designs (decade ranges) are SEPARATE documents: no diffs inside a research
doc, no survey prose padding a phase doc — a document that mixes both fails the
audit.

**Unit residence (STRICT, UNIT-RESIDENCE-01):** every piece of development work
belongs to an implementation unit (`devlog/_plan/YYMMDD_slug/`). Ceremony scales
with class (§9); residence does not. C0-C1 fast-path work skips the PABCD ceremony
but MUST leave a numbered record doc in its owning unit — next free index in the
matching decade, e.g. `40_hotfix_dropdown_crash.md` — stating what changed, why the
fast path applied (class call), and the verification evidence. No owning unit →
create a minimal unit folder holding only that record. Interview settles residence
before P (§1).

Devlog plan artifacts use decade-range numbering to separate concerns:
```

**Also in §3.1 Rules list — Before (~L172):**

```
- 00-range durable research is **mandatory for C4**, and for C3 only when state must persist
  across turns/agents, public contract or architecture decisions need durable audit, or the
  user/repo already uses devlog planning for that task; optional for C0-C2 and
  low-persistence C3 (a response-level plan plus verification record is enough).
```

**After:**

```
- 00-range durable research is **mandatory for C4**, and for C3 only when state must persist
  across turns/agents, public contract or architecture decisions need durable audit, or the
  user/repo already uses devlog planning for that task; optional for C0-C2 and
  low-persistence C3 (a response-level plan is enough — but the work still leaves its
  numbered record in a unit, UNIT-RESIDENCE-01).
```

## 1.4 §A audit checklist (~L193)

**Before:**

```
- New devlog phase documents use the numbered Jawdev filename convention.
```

**After:**

```
- New devlog phase documents use the numbered lexicographic filename convention;
  bare-named or research/implementation-mixed docs are a FAIL (LEXICO-SPLIT-01).
- Multi-phase units satisfy DIFFLEVEL-ROADMAP-01: every roadmap phase has a
  diff-level decade doc (no outline-only or missing phases), and the phase map is
  dependency-ordered, not effort-bucketed (PHASE-SPLIT-01).
```

## 1.5 §5 Loop/multi-pass paragraph (~L277-281)

**Before:**

```
**Loop / multi-pass tasks**: a "loop"/"루프" request (or work too large for one cycle) runs
as MULTIPLE PABCD passes — one per work-phase. Pre-plan the full slice map and scaffold
per-phase decade docs (10_phase1, 20_phase2, ...) up front. The first pass MAY be a
design-only PABCD pass (Phase 0): a code-free whole-system design/documentation cycle
before the first implementation work-phase.
```

**After:**

```
**Loop / multi-pass tasks**: a "loop"/"루프" request (or work too large for one cycle) runs
as MULTIPLE PABCD passes — one per work-phase. Pre-plan the full slice map and WRITE
all per-phase decade docs (10_phase1, 20_phase2, ...) to diff-level up front
(DIFFLEVEL-ROADMAP-01, §3.1) — scaffolding empty files is not pre-planning. Each
later cycle's P re-verifies its pre-written doc against the current codebase and
amends it before building. The first pass MAY be a design-only PABCD pass (Phase 0):
a code-free whole-system design/documentation cycle that produces exactly this
difflevel roadmap before the first implementation work-phase.
```

## 1.6 §9 depth table — C0-C1 Record cell (~L349)

**Before:**

```
| C0-C1 | None/inline | Optional | Direct fix | Smallest proof | One-line summary |
```

**After:**

```
| C0-C1 | None/inline | Optional | Direct fix | Smallest proof | One-line summary as a numbered record doc in the owning unit (UNIT-RESIDENCE-01) |
```

## 1.7 §3 P MUST-include list — SoT sync target (~L118)

**Before:**

```
For broad changes or unfamiliar repositories, P phase MUST include:
- Compact tree of the current repository shape
- Detected repo conventions: docs, plans, architecture notes, source-of-truth logs, naming, tests
- Whether existing `structure/`, `devlog/`, `docs/`, `plans/`, or equivalent logs were read and will be reused
- Whether `structure/` or `devlog/` is proposed
```

**After:**

```
For broad changes or unfamiliar repositories, P phase MUST include:
- Compact tree of the current repository shape
- Detected repo conventions: docs, plans, architecture notes, source-of-truth logs, naming, tests
- Whether existing `structure/`, `devlog/`, `docs/`, `plans/`, or equivalent logs were read and will be reused
- Whether `structure/` or `devlog/` is proposed
- The SoT sync target (SOT-SYNC-01): which general source-of-truth doc
  (`structure/`, architecture/INDEX docs) this unit will patch in C — or, if the
  repo has none, the plan recommends creating one (dev-scaffolding §2.1)
```

## 1.8 §C step 3 — SOT-SYNC-01 replaces generic structure-docs step (~L213-217)

**Before:**

```
### C — Check
Final sanity check:
1. Verify all files saved and consistent
2. Run `npx tsc --noEmit` (if TypeScript project)
3. Update project structure docs if applicable
4. Report completion summary
```

**After:**

```
### C — Check
Final sanity check:
1. Verify all files saved and consistent
2. Run `npx tsc --noEmit` (if TypeScript project)
3. **SoT sync (DEFAULT, SOT-SYNC-01):** locate the repo's general source-of-truth
   docs (`structure/`, architecture/INDEX docs) — found in P, patched HERE so SoT
   and code never diverge silently; if the repo has none, recommend creating one
   (dev-scaffolding §2.1) in the D summary
4. Report completion summary
```

---

# File 2 — `skills_ref/dev-scaffolding/references/implementation-log.md`

## 2.1 Header scope line (L5-6)

**Before:**

```
`dev-scaffolding/SKILL.md` §2.1 (folder proposal rules). Read when a work unit is
C3+, multi-phase, or must survive across sessions/agents.
```

**After:**

```
`dev-scaffolding/SKILL.md` §2.1 (folder proposal rules). Read before any development
work: unit residence is universal (UNIT-RESIDENCE-01) — the full routine below is for
C2+/multi-phase work; C0-C1 leaves a numbered record doc (see the last section).
```

## 2.2 Phase table P row (L31)

**Before:**

```
| P | CONCRETIZE: write `00_plan.md` (objective, measured baseline, work-phase map, risks) + research docs `01+`; phase design docs at **diff-level precision** (exact paths, NEW/MODIFY/DELETE, before/after for MODIFY) | plan exists as files, not chat |
```

**After:**

```
| P | CONCRETIZE: write `00_plan.md` (objective, measured baseline, dependency-ordered work-phase map, risks) + research docs `01+`; decade docs for **EVERY roadmap phase** at **diff-level precision** (exact paths, NEW/MODIFY/DELETE, before/after for MODIFY) — DIFFLEVEL-ROADMAP-01 | plan exists as files, not chat |
```

## 2.3 Multi-cycle paragraph (L37-40)

**Before:**

```
Multi-cycle units: one full PABCD per work-phase; each phase's design doc is written
in P of ITS cycle (pre-scaffold the decade files up front, fill per cycle). The
attestation log in `00_plan.md` is the continuity spine — each new P quotes the
previous D conclusion from it (see `dev-pabcd` §10 LOOP-CONTINUITY-01).
```

**After:**

```
Multi-cycle units: one full PABCD per work-phase; ALL phase design docs are written
to diff-level in the FIRST P (or the design-only Phase-0 pass) —
DIFFLEVEL-ROADMAP-01. P of each later cycle re-verifies its pre-written doc against
the current codebase (stale check) and amends it BEFORE building; it never writes
the doc fresh mid-unit. The attestation log in `00_plan.md` is the continuity spine
— each new P quotes the previous D conclusion from it (see `dev-pabcd` §10
LOOP-CONTINUITY-01).
```

## 2.4 "When NOT to use this" → residence is universal (L67-73)

**Before:**

```
## When NOT to use this

C0-C2 work does not get a unit folder (dev-pabcd §9: response-level plan +
verification record is enough). The routine is mandatory for C4, and for C3 when
state must persist across turns/agents or contracts/architecture need a durable
audit trail. Over-documenting small work is process slop — the classifier decides,
not habit.
```

**After:**

```
## Ceremony scales; residence does not

Every piece of work lands in an implementation unit (UNIT-RESIDENCE-01). The full
routine above (master plan + all-phase diff-level docs + doc audit) is mandatory for
C4, for any multi-phase unit regardless of class, and for C3 when state must persist
across turns/agents or contracts/architecture need a durable audit trail. C0-C1
fast-path work skips the ceremony but still leaves a numbered record doc in its
owning unit (what changed · why the fast path applied · verification evidence);
create a minimal unit folder if none exists. Over-documenting small work is process
slop — but "small" scales the ceremony down, never the record away.
```

## 2.5 Phase table C row — SOT-SYNC-01 (L34)

**Before:**

```
| C | Gate results (commands + tails) recorded into the unit | evidence lives next to the plan |
```

**After:**

```
| C | Gate results (commands + tails) recorded into the unit; general SoT docs patched to match the change (SOT-SYNC-01 — recommend creating one if absent) | evidence lives next to the plan |
```

---

# File 3 — `skills_ref/dev-scaffolding/SKILL.md`

## 3.1 §2 de-brand (exact line swaps)

| L | Before | After |
|---|--------|-------|
| 45 | `3. Reuse clear conventions instead of imposing the Lidge/Jawdev default.` | `3. Reuse clear conventions instead of imposing the Lidge/source-of-truth default.` |
| 49 | `MUST preserve mature repo conventions over the Lidge/Jawdev default.` | `MUST preserve mature repo conventions over the Lidge/source-of-truth default.` |

## 3.2 §2.1 title + opt-in intro → default routine (L51-56)

**Before:**

```
## 2.1 Lightweight Jawdev Source of Truth

Use this only when:
- The repo is immature, undocumented, or inconsistent; or
- The user asks for Jawdev/Lidge-style structure; or
- A broad change needs a durable plan/current-architecture record.
```

**After:**

```
## 2.1 Lightweight Source of Truth (implementation-unit devlog)

The implementation-unit devlog routine (`devlog/_plan/` units — `dev-pabcd` §3.1,
UNIT-RESIDENCE-01) is the DEFAULT for any repo you do development work in — a
process rule, not a named style to be requested. Propose the `structure/`
architecture docs when:
- The repo is immature, undocumented, or inconsistent; or
- The user asks for a durable source-of-truth structure; or
- A broad change needs a durable plan/current-architecture record.
```

## 3.3 Devlog method bullet list (L76-78)

**Before:**

```
Jawdev devlog method:
- Split large work into phase-level documents instead of one huge plan.
```

**After:**

```
Implementation-unit devlog method:
- Split large work into phase-level documents instead of one huge plan —
  dependency-ordered (PHASE-SPLIT-01), ALL written to diff-level up front
  (DIFFLEVEL-ROADMAP-01; both defined in `dev-pabcd`).
```

## 3.4 Naming paragraph (L82)

**Before:**

```
Jawdev phase document naming uses decade-range prefixes. For the canonical table (00–09 research, 10–19 Phase 1, etc.), see `dev-pabcd/SKILL.md` §3.1 Jawdev Document Numbering — that is the single source of truth.
```

**After:**

```
Phase document naming uses decade-range prefixes (LEXICO-SPLIT-01). For the canonical table (00–09 research, 10–19 Phase 1, etc.), see `dev-pabcd/SKILL.md` §3.1 Implementation-Unit Documents — that is the single source of truth.
```

## 3.5 Folder-approval gate exemption (L87)

**Before:**

```
Before creating any `structure/`/`devlog/` folders, ask concisely: state that no source-of-truth docs were found, show the proposed tree, give a specific recommendation, and confirm you will not create them without approval.
```

**After:**

```
Before creating any `structure/`/`devlog/` folders, ask concisely: state that no source-of-truth docs were found, show the proposed tree, give a specific recommendation, and confirm you will not create them without approval. This gate governs INTRODUCING the convention to a repo (the first `devlog/` or `structure/`); once `devlog/_plan/` exists, creating unit subfolders — including the minimal record unit mandated by UNIT-RESIDENCE-01 — is routine and needs no approval dialogue.
```

## 3.6-3.10 Remaining de-brand line swaps

| # | L | Before | After |
|---|---|--------|-------|
| 3.6 | 92 | `If the user explicitly asks for Lidge/Jawdev standard, create it.` | `If the user explicitly asks for the full source-of-truth standard (§8), create it.` |
| 3.7 | 163 | `\| devlog plan folders \| \`YYMMDD_slug/\` \| \`260510_jawdev_phase_doc_naming/\` \|` | `\| devlog plan folders \| \`YYMMDD_slug/\` \| \`260510_phase_doc_naming/\` \|` |
| 3.8a | 182 | `\`str_func\` is part of the full Lidge/Jawdev standard, not the lightweight default.` | `\`str_func\` is part of the full Lidge standard, not the lightweight default.` |
| 3.8b | 185 | `- The user explicitly asks for full Lidge/Jawdev structure.` | `- The user explicitly asks for the full Lidge structure.` |
| 3.9 | 252 | `3. Follow Jawdev source-of-truth conventions (§2.1) when applicable` | `3. Follow source-of-truth conventions (§2.1) when applicable` |
| 3.10 | 255 | `1. Follow decade numbering (\`dev-pabcd/SKILL.md\` §3.1 Jawdev Document Numbering): 00-09 research, 10-19 phase 1, etc.` | `1. Follow decade numbering (\`dev-pabcd/SKILL.md\` §3.1, LEXICO-SPLIT-01): 00-09 research, 10-19 phase 1, etc.` |

## 3.11 §2.1 SoT sync paragraph — insert before devlog method (L74-76, post-3.3)

Runs after block 3.3 has already renamed the line. Before references the post-3.3
state.

**Before:**

```
the repo already uses that convention or the user approves. Create an ADR only for a
decision that is hard to reverse, surprising without context, or has a real tradeoff.

Implementation-unit devlog method:
```

**After:**

```
the repo already uses that convention or the user approves. Create an ADR only for a
decision that is hard to reverse, surprising without context, or has a real tradeoff.

**SoT sync (DEFAULT, SOT-SYNC-01):** before patching a repo, FIND its general
source-of-truth docs first (`structure/`, `architecture.md`, INDEX/context docs)
and read them; any unit that changes architecture, contracts, or structure patches
the SoT doc in the SAME unit (C gate, dev-pabcd §3 C). If the repo has no SoT doc,
recommend creating one — once, via the proposal flow above — rather than silently
working without a source of truth.

Implementation-unit devlog method:
```

---

# File 4 — `skills_ref/dev/SKILL.md`

## 4.1 §0.1 Patch Fast-Path Keep bullet (L42)

**Before:**

```
- Keep: §3 verification gate, §4 change documentation when a worklog/changelog file is provided, §5 safety rules (imports/exports), §7.2 static analysis
```

**After:**

```
- Keep: §3 verification gate, §4 change documentation — including the numbered
  record doc in the owning implementation unit, mandatory for ALL work
  (UNIT-RESIDENCE-01, `dev-pabcd` §3.1), §5 safety rules (imports/exports), §7.2 static analysis
```

## 4.2-4.3 De-brand line swaps

| # | L | Before | After |
|---|---|--------|-------|
| 4.2 | 208 | `phase-document patterns (Jawdev decade numbering — see \`dev-pabcd\`).` | `phase-document patterns (decade numbering — see \`dev-pabcd\`).` |
| 4.3 | 254 | `- Jawdev/devlog phase documents use decade-range numbering (00-09 research, 10-19 phase 1, …); never bare \`PLAN.md\`/\`PHASES.md\`/\`RCA.md\`. Full convention: \`dev-pabcd\`.` | `- Devlog phase documents use decade-range numbering (00-09 research, 10-19 phase 1, …); never bare \`PLAN.md\`/\`PHASES.md\`/\`RCA.md\` (LEXICO-SPLIT-01). Full convention: \`dev-pabcd\`.` |

---

# File 5 — `src/orchestrator/state-machine.ts`

These are TypeScript template-literal strings injected as system prompts at runtime.
All edits are inside string literals, so they affect prompt content only — no signature
or type changes.

## 5.1 Interview INTERVIEW-CLASSIFY-01 prompt (~L409-412)

**Before:**

```
- **INTERVIEW-CLASSIFY-01**: before suggesting P, settle the loop archetype — does a
  verifier define *done* (spec-satisfaction), or only *better* (open-ended optimization:
  scores, win rates, benchmarks)? Record it as a known fact. Optimization work must plan
  instrumentation + an explore-and-select scheme in P — never a bare repair loop.
```

**After:**

```
- **INTERVIEW-CLASSIFY-01**: before suggesting P, settle the loop archetype — does a
  verifier define *done* (spec-satisfaction), or only *better* (open-ended optimization:
  scores, win rates, benchmarks)? Record it as a known fact. Also settle the **unit
  residence** (UNIT-RESIDENCE-01): which implementation unit (\`devlog/_plan/YYMMDD_slug/\`)
  this work belongs to, existing or new. Optimization work must plan instrumentation +
  an explore-and-select scheme in P — never a bare repair loop.
```

## 5.2 Interview Loop/Multi-Pass section (~L437-440)

**Before:**

```
If the user's request contains "loop" / "루프" (or clearly describes work too large for one PABCD cycle), treat it as a MULTI-PASS task:
- Assume PABCD will run several full cycles — one per work-phase.
- An Interview output may be a devlog scaffold: the work-phase decomposition (slice map) and per-phase stub docs using decade numbering (10_phase1, 20_phase2, ...), so the structure is agreed before P.
- A loop may open with a design-only PABCD pass (Phase 0): a code-free whole-system design/documentation cycle that runs before the first implementation work-phase. Note this possibility to the user when the task warrants it.`,
```

**After:**

```
If the user's request contains "loop" / "루프" (or clearly describes work too large for one PABCD cycle), treat it as a MULTI-PASS task:
- Assume PABCD will run several full cycles — one per work-phase.
- An Interview output settles the unit residence (UNIT-RESIDENCE-01) and produces the work-phase decomposition (slice map). P then WRITES all per-phase decade docs to diff-level (DIFFLEVEL-ROADMAP-01) — scaffolding empty stubs is not pre-planning.
- A loop may open with a design-only PABCD pass (Phase 0): a code-free whole-system design/documentation cycle that produces the difflevel roadmap before the first implementation work-phase. Note this possibility to the user when the task warrants it.`,
```

## 5.3 P prompt — save line + loop line (~L453-454)

**Before:**

```
   - Save to a devlog plan file using Jawdev decade numbering (see dev-pabcd skill).
   - For a loop / multi-pass task: pre-plan the FULL work-phase slice map up front and scaffold per-phase stub docs (10_phase1, 20_phase2, ...). The first pass MAY be a design-only PABCD pass (Phase 0) whose build output is documentation/architecture, not code.
```

**After:**

```
   - Save to a devlog plan file using decade numbering (see dev-pabcd skill, LEXICO-SPLIT-01).
   - For a loop / multi-pass task: pre-plan the FULL work-phase slice map and WRITE all per-phase decade docs (10_phase1, 20_phase2, ...) to diff-level up front (DIFFLEVEL-ROADMAP-01) — scaffolding empty stubs is not pre-planning. The first pass MAY be a design-only PABCD pass (Phase 0) whose build output is documentation/architecture, not code.
```

## 5.4 C prompt — SoT sync stage (~L598-600)

**Before:**

```
C4: also persist the screenshot to the devlog.

**Stage 2: Scrutiny (based on change scope)**
```

**After:**

```
C4: also persist the screenshot to the devlog.

**Stage 1.75: SoT Sync (DEFAULT, SOT-SYNC-01)**
If \`structure/\`, \`architecture.md\`, or INDEX/context docs exist in the repo, patch
them to reflect the changes made in B — SoT and code must never diverge silently.
If the repo has no SoT doc, note the recommendation to create one in the D summary.

**Stage 2: Scrutiny (based on change scope)**
```

---

# File 6 — `src/prompt/builder.ts`

## 6.1 PABCD guide devlog line (~L569)

**Before:**

```
- Devlog plan docs use decade numbering (00-09 research, 10-19 phase 1, ...). A loop/multi-pass task pre-plans the full slice map and scaffolds per-phase docs up front, and may open with a design-only PABCD pass.
```

**After (as applied — B repair, PSC-004 1600-char window):**

```
- Devlog plan docs use decade numbering (LEXICO-SPLIT-01). Loop/multi-pass tasks WRITE all per-phase docs to diff-level up front (DIFFLEVEL-ROADMAP-01) and may open with a design-only PABCD pass.
```

> B-repair note: the originally planned After text (+74 chars, with the decade
> examples and the "scaffolding empty stubs" clause) pushed the `design-only PABCD
> pass` phrase past the 1600-char window asserted by test PSC-004. The applied text
> keeps both rule IDs and the design-only-pass phrasing; the dropped clauses remain
> in the full dev-pabcd skill body and the state-machine P prompt. Doc synced to
> match the applied code (doc-code convergence per the B routine).

---

# File 7 — `src/workflows/planaudit.ts`

## 7.1 Audit checks array — Jawdev line (~L40)

**Before:**

```
        'Devlog phase documents use the numbered Jawdev filename convention.',
```

**After:**

```
        'Devlog phase documents use the numbered lexicographic filename convention (LEXICO-SPLIT-01); bare-named or research/implementation-mixed docs are a FAIL.',
        'Multi-phase units satisfy DIFFLEVEL-ROADMAP-01: every roadmap phase has a diff-level decade doc, and the phase map is dependency-ordered (PHASE-SPLIT-01).',
```

Note: this adds one element to the `checks` array. The `.join('\n- ')` call handles
the extra entry without any other code change.

---

# File 8 — `src/prompt/templates/a1-system.md`

## 8.1 Project context discovery — jawdev mention (~L48)

**Before:**

```
3. For orchestration work: read `devlog/` and `_plan/` for prior decisions and jawdev conventions
```

**After:**

```
3. For orchestration work: read `devlog/` and `_plan/` for prior decisions and devlog conventions
```

---

# File 9 — `src/cli/types.ts`

These are TypeScript union-literal types. The values are internal enum-like strings,
not user-facing labels. Renaming them requires checking all import sites for the old
literals — the grep in File 9 context (above) confirmed the two values appear ONLY
in `types.ts` itself and nowhere else in `src/`.

## 9.1 WorkflowArtifactAction kind (~L97)

**Before:**

```
        | 'save-jawdev'
```

**After:**

```
        | 'save-devlog'
```

## 9.2 WorkflowArtifactStorage mode (~L104)

**Before:**

```
    mode: 'chat' | 'jaw-home-cache' | 'pabcd-worklog' | 'jawdev-devlog' | 'memory' | 'project-file';
```

**After:**

```
    mode: 'chat' | 'jaw-home-cache' | 'pabcd-worklog' | 'devlog' | 'memory' | 'project-file';
```

**IMPORTANT runtime note:** these two literal values are currently type-only — grep
confirms they are referenced nowhere else in `src/`. However, if any workflow or
handler code is added between the time this doc is written and the time B executes,
a stale check grep MUST be re-run:

```bash
grep -rn "save-jawdev\|jawdev-devlog" src/
```

If new hits appear, update those sites in the same commit.

---

# File 10 — `skills_ref/goal/SKILL.md`

## 10.1 Multi-phase / loop goals paragraph (~L48)

**Before:**

```
**Multi-phase / loop goals**: each sub-goal / work-phase = one FULL PABCD cycle (P→A→B→C→D). After D (state → IDLE), run `cli-jaw orchestrate P` to start the next work-phase; repeat until the objective is met. Never run B for several work-phases back-to-back. A "loop"/"루프" goal is multi-pass: pre-plan the full slice map and scaffold per-phase decade docs, and it may open with a design-only PABCD pass (Phase 0) before the first implementation work-phase. Faithfully execute each PABCD-phase — never rubber-stamp a phase to advance.
```

**After:**

```
**Multi-phase / loop goals**: each sub-goal / work-phase = one FULL PABCD cycle (P→A→B→C→D). After D (state → IDLE), run `cli-jaw orchestrate P` to start the next work-phase; repeat until the objective is met. Never run B for several work-phases back-to-back. A "loop"/"루프" goal is multi-pass: pre-plan the full slice map and WRITE all per-phase decade docs to diff-level up front (DIFFLEVEL-ROADMAP-01) — scaffolding empty stubs is not pre-planning. It may open with a design-only PABCD pass (Phase 0) before the first implementation work-phase. Faithfully execute each PABCD-phase — never rubber-stamp a phase to advance.
```

---

# File 11 — `tests/unit/jawdev-skill-contract.test.ts`

Rename to `tests/unit/devlog-skill-contract.test.ts` and de-brand test names.

## 11.1 Full file rewrite

The test assertions check for patterns (`decade-range`, `00_.*plan`, `bare semantic
filenames`, `PLAN.md`, etc.) that remain valid post-port. Only the test names and
file name change. The Jawdev-specific assertions (`Jawdev` appearing in skill text)
are NOT checked by these tests — they check structural patterns only. No assertion
changes needed.

**Before (file: `tests/unit/jawdev-skill-contract.test.ts`):**

```typescript
test('JDS-001: dev-scaffolding documents decade-range Jawdev phase filenames', { skip: !hasRequiredDocs && 'skills_ref/devlog submodules not checked out' }, () => {
```

**After (file: `tests/unit/devlog-skill-contract.test.ts`):**

```typescript
test('DLC-001: dev-scaffolding documents decade-range lexicographic phase filenames', { skip: !hasRequiredDocs && 'skills_ref/devlog submodules not checked out' }, () => {
```

**Before:**

```typescript
test('JDS-002: common dev and PABCD skills propagate the Jawdev naming contract', { skip: !hasRequiredDocs && 'skills_ref/devlog submodules not checked out' }, () => {
```

**After:**

```typescript
test('DLC-002: common dev and PABCD skills propagate the devlog naming contract', { skip: !hasRequiredDocs && 'skills_ref/devlog submodules not checked out' }, () => {
```

**Before:**

```typescript
test('JDS-003: devlog local AGENTS file enforces decade-range phase document naming', { skip: !hasRequiredDocs && 'skills_ref/devlog submodules not checked out' }, () => {
```

**After:**

```typescript
test('DLC-003: devlog local AGENTS file enforces decade-range phase document naming', { skip: !hasRequiredDocs && 'skills_ref/devlog submodules not checked out' }, () => {
```

File rename: `git mv tests/unit/jawdev-skill-contract.test.ts tests/unit/devlog-skill-contract.test.ts`

---

# File 12 — `structure/prompt_basic_B.md`

Current-architecture doc. Contains two Jawdev references in the skills injection
summary that must be de-branded for consistency.

## 12.1 dev skill summary (L79)

**Before:**

```
- dev skill은 TS-first strict-compatible 기본값과 Jawdev convention discovery/source-of-truth proposal 규칙을 포함한다.
```

**After:**

```
- dev skill은 TS-first strict-compatible 기본값과 devlog convention discovery/source-of-truth proposal 규칙을 포함한다.
```

## 12.2 dev-scaffolding summary (L81)

**Before:**

```
- dev-scaffolding은 기존 repo convention 우선, `structure/`/`devlog/` 생성은 승인 기반으로 다룬다. Jawdev 방식은 phase별 문서 분리와 diff-level plan 파일 저장을 기본으로 설명한다.
```

**After:**

```
- dev-scaffolding은 기존 repo convention 우선, `structure/`/`devlog/` 생성은 승인 기반으로 다룬다. Implementation-unit devlog 방식은 phase별 문서 분리와 diff-level plan 파일 저장을 기본으로 설명한다.
```

---

# File 13 — `structure/INDEX.md`

Current-architecture doc. The topic-gap tracker table references "Jawdev skill
guidance" in a row label.

## 13.1 PABCD topic-gap row (L136)

**Before:**

```
| PABCD Project root guard + Jawdev skill guidance | `src/orchestrator/pipeline.ts`, `src/orchestrator/state-machine.ts`, `skills_ref/dev*/SKILL.md`, `structure/prompt_basic_B.md` | PABCD docs should require `Project root: <absolute path>` in injected/dispatch examples and skill docs should prefer strict TypeScript plus existing `structure/`/`devlog`/SOT discovery. |
```

**After:**

```
| PABCD Project root guard + devlog skill guidance | `src/orchestrator/pipeline.ts`, `src/orchestrator/state-machine.ts`, `skills_ref/dev*/SKILL.md`, `structure/prompt_basic_B.md` | PABCD docs should require `Project root: <absolute path>` in injected/dispatch examples and skill docs should prefer strict TypeScript plus existing `structure/`/`devlog`/SOT discovery. |
```

---

## Verification (C gate for this phase)

Run from repo root `/Users/jun/Developer/new/700_projects/cli-jaw`:

```bash
# De-brand assertions
grep -ric "jawdev" skills_ref/dev-pabcd/ skills_ref/dev-scaffolding/ skills_ref/dev/ skills_ref/goal/   # expect 0
grep -ric "jawdev" src/orchestrator/ src/prompt/ src/workflows/ src/cli/types.ts                         # expect 0
grep -ric "jawdev" structure/prompt_basic_B.md structure/INDEX.md                                        # expect 0
grep -ric "jawdev" tests/unit/                                                                           # expect 0

# Contract rule counts
grep -c "DIFFLEVEL-ROADMAP-01" skills_ref/dev-pabcd/SKILL.md           # expect >= 3
grep -c "LEXICO-SPLIT-01"      skills_ref/dev-pabcd/SKILL.md           # expect >= 2
grep -c "UNIT-RESIDENCE-01"    skills_ref/dev-pabcd/SKILL.md           # expect >= 3
grep -c "PHASE-SPLIT-01"       skills_ref/dev-pabcd/SKILL.md           # expect >= 2
grep -rn "fill per cycle" skills_ref/                                  # expect 0 hits
grep -n  "pre-scaffold the decade" skills_ref/                          # expect 0 hits
grep -c "UNIT-RESIDENCE-01" skills_ref/dev-scaffolding/references/implementation-log.md  # expect >= 2
grep -c "UNIT-RESIDENCE-01" skills_ref/dev-scaffolding/SKILL.md         # expect 2
grep -c "UNIT-RESIDENCE-01" skills_ref/dev/SKILL.md                     # expect 1
grep -c "SOT-SYNC-01"      skills_ref/dev-pabcd/SKILL.md               # expect 2
grep -c "SOT-SYNC-01"      skills_ref/dev-scaffolding/references/implementation-log.md  # expect 1
grep -c "SOT-SYNC-01"      skills_ref/dev-scaffolding/SKILL.md         # expect 1

# Source-code prompt strings
grep -c "DIFFLEVEL-ROADMAP-01" src/orchestrator/state-machine.ts        # expect >= 1
grep -c "LEXICO-SPLIT-01"      src/orchestrator/state-machine.ts        # expect >= 1
grep -c "UNIT-RESIDENCE-01"    src/orchestrator/state-machine.ts        # expect >= 1
grep -c "DIFFLEVEL-ROADMAP-01" src/workflows/planaudit.ts               # expect 1
grep -c "LEXICO-SPLIT-01"      src/workflows/planaudit.ts               # expect 1
grep -c "LEXICO-SPLIT-01"      src/prompt/builder.ts                    # expect 1
grep -c "DIFFLEVEL-ROADMAP-01" src/prompt/builder.ts                    # expect 1
grep -c "SOT-SYNC-01"         src/orchestrator/state-machine.ts        # expect 1

# Stale-check for type literals
grep -rn "save-jawdev\|jawdev-devlog" src/                              # expect 0

# Build + test gates
npx tsc --noEmit                                                        # expect exit 0
npm test                                                                 # expect exit 0
npm run gate:all                                                        # expect exit 0
```

Plus read-back: every After block matches the file verbatim; no other lines changed.

---

## Deploy / sync note

`skills_ref/` in the cli-jaw repo is the source copy. At install/update time, it
deploys to `~/.cli-jaw/skills_ref/` (the user-home installed copy that agents
read at runtime). After B merges:

1. Run `npm run build` to compile the TypeScript source changes to `dist/`.
2. Run `jaw skill sync` (or the install script) to push `skills_ref/` to
   `~/.cli-jaw/skills_ref/`. Until this runs, any live agent session will still
   read the OLD skill text from the installed copy.
3. Restart any running `jaw serve` instance to pick up the new `dist/` and the
   prompt-template changes.

4. **Doc regeneration required**: `docs/dev/skills/detail/dev-pabcd.html`,
   `docs/dev/ko/skills/detail/dev-pabcd.html`, and
   `docs/dev/zh/skills/detail/dev-pabcd.html` contain stale Jawdev references
   (L177, L203 in each locale). These are hand-crafted HTML files with no
   discoverable generation command — TODO for B executor: manually de-brand the
   three HTML files, or build a generation script and regenerate.

This deploy step is OUT OF SCOPE for the B executor's commit — it is a post-merge
operational step.
