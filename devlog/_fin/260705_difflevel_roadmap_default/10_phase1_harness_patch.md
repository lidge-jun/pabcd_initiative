# 10_phase1 — Harness patch: de-brand + DIFFLEVEL / PHASE-SPLIT / LEXICO / UNIT-RESIDENCE

Phase 1 of 4 (rev 3 — audit round-1 findings incorporated: blocks 1.6, 3.10, fixed
verification grep). All targets under `/Users/jun/Developer/new/700_projects/pabcd_initiative/`.

Files: 4 MODIFY, 0 NEW, 0 DELETE.

| # | File | Blocks |
|---|------|--------|
| 1 | `skills/dev-pabcd/SKILL.md` | 1.1–1.6 |
| 2 | `skills/dev-scaffolding/references/implementation-log.md` | 2.1–2.4 |
| 3 | `skills/dev-scaffolding/SKILL.md` | 3.1–3.10 |
| 4 | `skills/dev/SKILL.md` | 4.1–4.3 |

---

# File 1 — `skills/dev-pabcd/SKILL.md`

## 1.1 §1 Interview settles unit residence (~L39)

**Before:**

```
**Interview MUST settle two classifications before P** (DEFAULT, INTERVIEW-CLASSIFY-01):
the work class (dev §0.0) and the **loop archetype** (§11.4) — ask "does a verifier
define *done* for this work, or only *better*?". This applies in HITL and goal mode
alike. An archetype discovered mid-loop — after candidates have already been burned —
is an Interview failure, not a Build failure.
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

## 1.2 §3 P phase-design paragraph → PHASE-SPLIT-01 (~L182)

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

## 1.3 §3.1 rename + three new STRICT rules (~L215)

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

**Also in §3.1 Rules list — Before:**

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

## 1.4 §A audit checklist (~L255)

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

## 1.5 §5 Loop/multi-pass paragraph (~L341)

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

## 1.6 §9 depth table — C0-C1 Record cell (audit round-1 warn #2)

**Before:**

```
| C0-C1 | None/inline | Optional | Direct fix | Smallest proof | One-line summary |
```

**After:**

```
| C0-C1 | None/inline | Optional | Direct fix | Smallest proof | One-line summary as a numbered record doc in the owning unit (UNIT-RESIDENCE-01) |
```

## 1.7 §3 P MUST-include list — SoT sync target (user directive, rev 4)

**Before:**

```
- Whether `structure/` or `devlog/` is proposed
```

**After:**

```
- Whether `structure/` or `devlog/` is proposed
- The SoT sync target (SOT-SYNC-01): which general source-of-truth doc
  (`structure/`, architecture/INDEX docs) this unit will patch in C — or, if the
  repo has none, the plan recommends creating one (dev-scaffolding §2.1)
```

## 1.8 §C step 3 — SoT sync rule (user directive, rev 4)

**Before:**

```
3. Update project structure docs if applicable
```

**After:**

```
3. **SoT sync (DEFAULT, SOT-SYNC-01):** locate the repo's general source-of-truth
   docs (`structure/`, architecture/INDEX docs) — found in P, patched HERE so SoT
   and code never diverge silently; if the repo has none, recommend creating one
   (dev-scaffolding §2.1) in the D summary
```

---

# File 2 — `skills/dev-scaffolding/references/implementation-log.md`

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

## 2.5 Phase table C row — SoT sync (user directive, rev 4)

**Before:**

```
| C | Gate results (commands + tails) recorded into the unit | evidence lives next to the plan |
```

**After:**

```
| C | Gate results (commands + tails) recorded into the unit; general SoT docs patched to match the change (SOT-SYNC-01 — recommend creating one if absent) | evidence lives next to the plan |
```

---

# File 3 — `skills/dev-scaffolding/SKILL.md`

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

## 3.5–3.9 Remaining de-brand line swaps

| # | L | Before | After |
|---|---|--------|-------|
| 3.5 | 92 | `If the user explicitly asks for Lidge/Jawdev standard, create it.` | `If the user explicitly asks for the full source-of-truth standard (§8), create it.` |
| 3.6 | 163 | `| devlog plan folders | \`YYMMDD_slug/\` | \`260510_jawdev_phase_doc_naming/\` |` | `| devlog plan folders | \`YYMMDD_slug/\` | \`260510_phase_doc_naming/\` |` |
| 3.7a | 182 | `\`str_func\` is part of the full Lidge/Jawdev standard, not the lightweight default.` | `\`str_func\` is part of the full Lidge standard, not the lightweight default.` |
| 3.7b | 185 | `- The user explicitly asks for full Lidge/Jawdev structure.` | `- The user explicitly asks for the full Lidge structure.` |
| 3.8 | 252 | `3. Follow Jawdev source-of-truth conventions (§2.1) when applicable` | `3. Follow source-of-truth conventions (§2.1) when applicable` |
| 3.9 | 255 | `1. Follow decade numbering (\`dev-pabcd/SKILL.md\` §3.1 Jawdev Document Numbering): 00-09 research, 10-19 phase 1, etc.` | `1. Follow decade numbering (\`dev-pabcd/SKILL.md\` §3.1, LEXICO-SPLIT-01): 00-09 research, 10-19 phase 1, etc.` |

## 3.10 Folder-approval gate exemption for unit subfolders (audit round-1 warn #3, L87)

**Before:**

```
Before creating any `structure/`/`devlog/` folders, ask concisely: state that no source-of-truth docs were found, show the proposed tree, give a specific recommendation, and confirm you will not create them without approval.
```

**After:**

```
Before creating any `structure/`/`devlog/` folders, ask concisely: state that no source-of-truth docs were found, show the proposed tree, give a specific recommendation, and confirm you will not create them without approval. This gate governs INTRODUCING the convention to a repo (the first `devlog/` or `structure/`); once `devlog/_plan/` exists, creating unit subfolders — including the minimal record unit mandated by UNIT-RESIDENCE-01 — is routine and needs no approval dialogue.
```

## 3.11 §2.1 — SoT sync paragraph (user directive, rev 4)

**Insert after the "Folder names are advisory. …" / optional-files paragraph (before "Implementation-unit devlog method:"):**

```
**SoT sync (DEFAULT, SOT-SYNC-01):** before patching a repo, FIND its general
source-of-truth docs first (`structure/`, `architecture.md`, INDEX/context docs)
and read them; any unit that changes architecture, contracts, or structure patches
the SoT doc in the SAME unit (C gate, dev-pabcd §3 C). If the repo has no SoT doc,
recommend creating one — once, via the proposal flow above — rather than silently
working without a source of truth.
```

---

# File 4 — `skills/dev/SKILL.md`

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

## 4.2–4.3 De-brand line swaps

| # | L | Before | After |
|---|---|--------|-------|
| 4.2 | 208 | `phase-document patterns (Jawdev decade numbering — see \`dev-pabcd\`).` | `phase-document patterns (decade numbering — see \`dev-pabcd\`).` |
| 4.3 | 254 | `- Jawdev/devlog phase documents use decade-range numbering (00-09 research, 10-19 phase 1, …); never bare \`PLAN.md\`/\`PHASES.md\`/\`RCA.md\`. Full convention: \`dev-pabcd\`.` | `- Devlog phase documents use decade-range numbering (00-09 research, 10-19 phase 1, …); never bare \`PLAN.md\`/\`PHASES.md\`/\`RCA.md\` (LEXICO-SPLIT-01). Full convention: \`dev-pabcd\`.` |

---

## Verification (C gate for this phase)

Run from repo root `/Users/jun/Developer/new/700_projects/pabcd_initiative`:

```
grep -ric "jawdev" skills/                                         # expect 0
grep -c "DIFFLEVEL-ROADMAP-01" skills/dev-pabcd/SKILL.md            # expect ≥3
grep -c "LEXICO-SPLIT-01"      skills/dev-pabcd/SKILL.md            # expect ≥2
grep -c "UNIT-RESIDENCE-01"    skills/dev-pabcd/SKILL.md            # expect ≥3
grep -c "PHASE-SPLIT-01"       skills/dev-pabcd/SKILL.md            # expect ≥2
grep -rn "fill per cycle" skills/                                   # expect 0 hits
grep -n  "pre-scaffold the decade" skills/                           # expect 0 hits
grep -rn "scaffold$" skills/dev-pabcd/SKILL.md                       # expect 0 hits (audit fix: old phrase spans a line break)
grep -c "UNIT-RESIDENCE-01" skills/dev-scaffolding/references/implementation-log.md  # expect ≥2
grep -c "UNIT-RESIDENCE-01" skills/dev-scaffolding/SKILL.md          # expect 1
grep -c "UNIT-RESIDENCE-01" skills/dev/SKILL.md                      # expect 1
grep -c "SOT-SYNC-01" skills/dev-pabcd/SKILL.md                      # expect 2
grep -c "SOT-SYNC-01" skills/dev-scaffolding/SKILL.md                # expect 1
grep -c "SOT-SYNC-01" skills/dev-scaffolding/references/implementation-log.md  # expect 1
```

Plus read-back: every After block matches the file verbatim; no other lines changed.
