# 40_phase4 — Jawcode port: implementation-unit discipline into the jwc skill family

Phase 4 of 4. Target repo: `/Users/jun/Developer/new/700_projects/jawcode` (TS/Rust
monorepo, bun workspace). All targets under `packages/coding-agent/src/`.

Files: 4 MODIFY, 0 NEW, 0 DELETE.

| # | File (relative to repo root) | Blocks |
|---|-------------------------------|--------|
| 1 | `packages/coding-agent/src/defaults/jwc/skills/jaw-interview/SKILL.md` | 1.1 |
| 2 | `packages/coding-agent/src/prompts/jaw/orchestrate-i.md` | 2.1 |
| 3 | `packages/coding-agent/src/prompts/jaw/orchestrate-p.md` | 3.1–3.3 |
| 4 | `packages/coding-agent/src/prompts/jaw/orchestrate-c.md` | 4.1–4.3 |

Repo conventions honored:

- **Numbering**: jawcode does not use `NNN_` doc prefixes in its skill family;
  its convention is a flat `SKILL.md` per folder. The port adds contract rules
  as inline sections, not numbered files.
- **Language**: jawcode skills are English. All additions are English.
- **Skill format**: jawcode skills use XML-like tags (`<Purpose>`, `<Steps>`,
  `<Execution_Policy>`) and YAML frontmatter. Insertions match the surrounding
  style exactly.
- **Bundled skill pipeline**: skills are imported as text in
  `packages/coding-agent/src/defaults/jwc-defaults.ts` and rendered into the
  system prompt at runtime. No separate install step; the source file IS the
  deployed artifact.
- **Build gate**: `bun run check` (includes `bun run check:ts` which runs biome
  + tsc). `bun run test` runs the full suite. The modified files are `.md` only,
  so `check:ts` passes trivially; `test` may snapshot-compare prompt output
  (check snapshot tests under `packages/coding-agent/test/`).
- **De-branding scope**: one "Jawdev" occurrence exists across the target
  surfaces (orchestrate-p.md L13). The port replaces it.

---

## Why 4 MODIFY, 0 NEW

Jawcode has NO implementation-unit concept today. The six bundled jwc skills
(browse, goal, jaw-interview, plan, search, team) have no devlog numbering
rules, no unit-residence requirement, and no difflevel roadmap mandate. The
contract enters through four injection points:

1. **jaw-interview SKILL.md** — INTERVIEW-CLASSIFY-01 currently settles TWO
   things (task shape + loop archetype). The contract adds a third: unit
   residence. This is the canonical location because the jawcode interview
   engine is the requirements-gathering surface that feeds planning.

2. **orchestrate-i.md** — the thin routing prompt for the I stage. It
   references INTERVIEW-CLASSIFY-01 and must be updated to mention the
   third settlement (unit residence), keeping it aligned with the
   jaw-interview skill.

3. **orchestrate-p.md** — the P stage prompt where plans are written to
   devlog. It contains the single "Jawdev" occurrence and the naming
   instruction. The port: (a) de-brands "Jawdev" to neutral, (b) adds
   DIFFLEVEL-ROADMAP-01 enforcement for multi-phase units, (c) adds
   PHASE-SPLIT-01 (dependency ordering, effort-bucketing ban), (d) adds
   LEXICO-SPLIT-01 (no bare filenames), (e) adds UNIT-RESIDENCE-01
   (C0-C1 record-doc requirement), (f) adds SOT-SYNC-01 (SoT sync
   target in plan requirements).

4. **orchestrate-c.md** — the C stage prompt where checks are run and
   the verdict is issued. The port adds SOT-SYNC-01 as a new stage
   between adversarial review and render grounding, requiring the agent
   to locate and patch the repo's general source-of-truth docs before
   issuing the verdict. Existing stages are renumbered to accommodate
   the insertion.

No NEW files are needed because jawcode's convention is inline skill
content, not separate reference documents. The plan skill is SUPERSEDED
and read-only (see its frontmatter); we do NOT touch it.

---

# File 1 — `packages/coding-agent/src/defaults/jwc/skills/jaw-interview/SKILL.md`

## 1.1 INTERVIEW-CLASSIFY-01: two classifications -> three (~L49)

**Before:**

```
- **INTERVIEW-CLASSIFY-01:** before the interview can hand off to planning or execution, settle two classifications: the task shape and the loop archetype. Ask, explicitly or implicitly from evidence, whether a verifier defines done for this work or only better. Record the answer as `spec-satisfaction` or `open-ended-optimization`; discovering this only after candidates have been burned is an interview failure, not a build failure.
```

**After:**

```
- **INTERVIEW-CLASSIFY-01:** before the interview can hand off to planning or execution, settle three things: the task shape, the loop archetype, and the **unit residence** — which implementation unit (`devlog/_plan/YYMMDD_slug/`) this work belongs to, an existing unit or a new one (UNIT-RESIDENCE-01). Ask, explicitly or implicitly from evidence, whether a verifier defines done for this work or only better. Record the archetype as `spec-satisfaction` or `open-ended-optimization`; record the unit path in the spec metadata. Discovering the archetype only after candidates have been burned, or orphaning work outside a unit, is an interview failure, not a build failure.
```

---

# File 2 — `packages/coding-agent/src/prompts/jaw/orchestrate-i.md`

## 2.1 INTERVIEW-CLASSIFY-01 reference: add unit residence (~L7)

**Before:**

```
2. Settle the loop archetype before suggesting P (INTERVIEW-CLASSIFY-01): does a verifier define *done* for this work (spec-satisfaction), or only *better* (open-ended optimization — scores, win rates, benchmarks)? Record it in the spec; optimization work must plan instrumentation and an explore-and-select scheme in P, not a repair loop.
```

**After:**

```
2. Settle the loop archetype and the unit residence before suggesting P (INTERVIEW-CLASSIFY-01): does a verifier define *done* for this work (spec-satisfaction), or only *better* (open-ended optimization — scores, win rates, benchmarks)? Record the archetype in the spec; optimization work must plan instrumentation and an explore-and-select scheme in P, not a repair loop. Also settle which implementation unit (`devlog/_plan/YYMMDD_slug/`) this work belongs to — an existing unit or a new one (UNIT-RESIDENCE-01). Record the unit path in the spec.
```

---

# File 3 — `packages/coding-agent/src/prompts/jaw/orchestrate-p.md`

## 3.1 De-brand + add four contract rules to the naming instruction (~L13)

**Before:**

```
   - Save to a devlog plan file and record it as `plan_ref`. Use Jawdev lexicographic execution-order naming, not append-only chronology: `00_*` for MOC/index, phase bands such as `10/20/30` for small plans or `100/200/300` for larger plans, and PABCD artifacts placed inside the relevant phase sequence as plan/audit/synthesis/build/check records rather than top-level P/A/B/C/D bands. Example for Phase 2: `20_plan.md`, `20.1_p_critic_round1.md`, `20.2_p_synthesis_round1.md`, `20.3_a_planner_round1.md`, `20.4_a_architect_round1.md`, `21_impl.md`; use sortable point slots when inserting between existing phase files.
```

**After:**

```
   - Save to a devlog plan file and record it as `plan_ref`. Use lexicographic execution-order naming (LEXICO-SPLIT-01), not append-only chronology: `00_*` for MOC/index, phase bands such as `10/20/30` for small plans or `100/200/300` for larger plans, and PABCD artifacts placed inside the relevant phase sequence as plan/audit/synthesis/build/check records rather than top-level P/A/B/C/D bands. Never use bare semantic filenames (`PLAN.md`, `PHASES.md`, `RCA.md`); research/spec material (00-range) and implementation phase designs (decade ranges) are separate documents — a doc that mixes both fails audit. Example for Phase 2: `20_plan.md`, `20.1_p_critic_round1.md`, `20.2_p_synthesis_round1.md`, `20.3_a_planner_round1.md`, `20.4_a_architect_round1.md`, `21_impl.md`; use sortable point slots when inserting between existing phase files.
```

## 3.2 NEW passage: difflevel + phase-split + unit-residence rules (insert after L13, before step 3)

**Insertion point:** immediately after the save-to-devlog bullet (block 3.1 above) and
before step 3 ("Quality review loop").

**NEW block:**

```
   - **Difflevel roadmap plan (STRICT, DIFFLEVEL-ROADMAP-01):** for any multi-phase unit (2+ work-phases), the FIRST P — or the dedicated design-only Phase-0 pass — must deliver the entire roadmap concretized: `00_moc.md` (objective, constraints, dependency-ordered work-phase map) PLUS every phase's decade doc written to full diff-level precision (exact paths, NEW/MODIFY/DELETE, before/after diffs) — each one a copy-paste-executable PRD, not an outline. Scaffolding empty decade files to "fill per cycle" does NOT satisfy this rule. Each later cycle's P starts from its pre-written doc: re-verify it against the current codebase (stale check — earlier phases may have moved lines, signatures, or files), amend the doc, then execute.
   - **Phase ordering (STRICT, PHASE-SPLIT-01):** slice and order phases by dependency/architecture structure — foundations → core capabilities → integration → hardening/polish — so each phase consumes the verified output of the previous one. Effort-based bucketing is FORBIDDEN: never split or order phases by estimated effort or payoff speed — no "quick win vs heavy" buckets, no impact/effort matrices, no time-boxed slices. Phase boundaries encode the build order, not the schedule. DB/API/UI/test work inside a phase are subtasks, not top-level phases by default, and every phase must still close with something independently verifiable (build passes, tests green, or a demonstrable surface).
   - **Unit residence (STRICT, UNIT-RESIDENCE-01):** every piece of development work belongs to an implementation unit (`devlog/_plan/YYMMDD_slug/`). Ceremony scales with class; residence does not. C0-C1 fast-path work (trivial patches, single-file local fixes) skips the PABCD ceremony but MUST leave a numbered record doc in its owning unit — next free index in the matching decade, e.g. `40_hotfix_dropdown_crash.md` — stating what changed, why the fast path applied, and the verification evidence. No owning unit → create a minimal unit folder holding only that record. Interview settles residence before P (INTERVIEW-CLASSIFY-01).
```

## 3.3 SOT-SYNC-01: SoT sync target in plan requirements (insert after block 3.2, before step 3)

**Insertion point:** immediately after block 3.2's content (the three
contract-rule bullets) and before step 3 ("Quality review loop").

**NEW block:**

```
   - **SoT sync target (DEFAULT, SOT-SYNC-01):** identify which general source-of-truth doc in this repo (`structure/`, architecture/INDEX docs, or equivalent) this unit will patch at C — or, if the repo has no SoT doc, recommend creating one in the plan. Do not create new project-level source-of-truth folders during B unless approved here or explicitly requested by the user.
```

---

# File 4 — `packages/coding-agent/src/prompts/jaw/orchestrate-c.md`

## 4.1 Header: three-stage -> five-stage, add SoT sync + render grounding to stage chain (~L3)

**Before:**

```
You are now in Check mode — a three-stage verification gate (D050-9/17): mechanical verification → adversarial review → verdict.
```

**After (as applied — post-B polish):**

```
You are now in Check mode — a five-stage verification gate (D050-9/17): mechanical verification → adversarial review → SoT sync → render grounding (conditional) → verdict.
```

> Polish note: the original After said "four-stage … SoT sync → verdict", omitting
> render grounding from the chain while the body numbers stages 1-5. Header now
> matches the body's stage count and chain.

## 4.2 SOT-SYNC-01: insert SoT sync as new Stage 3, renumber render grounding to Stage 4 (~L13-14)

**Before:**

```
- Runtime actor note: compatible C-stage reviewer lanes (`c:mechanical-check-reviewer`, `c:adversarial-reviewer`) may resume within the same C-stage namespace on reruns. C→B/P/I routing retires C-stage lookup before the target stage starts; never carry C reviewer actors across stages.
Stage 3 — Render grounding (conditional — skip when not applicable):
When the work-phase produced an artifact whose correctness only shows when run or rendered (HTML page, SVG, game, UI, chart, animation, script with observable visual/interactive output), first mark it in-scope — `jwc orchestrate verdict --render-pending` (this arms the c→d soft warning until you resolve it) — then run the render-grounding loop before proceeding to verdict:
```

**After:**

```
- Runtime actor note: compatible C-stage reviewer lanes (`c:mechanical-check-reviewer`, `c:adversarial-reviewer`) may resume within the same C-stage namespace on reruns. C→B/P/I routing retires C-stage lookup before the target stage starts; never carry C reviewer actors across stages.

Stage 3 — SoT sync (DEFAULT, SOT-SYNC-01):
- Locate the repo's general source-of-truth docs (`structure/`, architecture/INDEX docs, or equivalent) — identified in P; patch them HERE so documentation and code never diverge silently. If the repo has no SoT doc, recommend creating one in the D summary.

Stage 4 — Render grounding (conditional — skip when not applicable):
When the work-phase produced an artifact whose correctness only shows when run or rendered (HTML page, SVG, game, UI, chart, animation, script with observable visual/interactive output), first mark it in-scope — `jwc orchestrate verdict --render-pending` (this arms the c→d soft warning until you resolve it) — then run the render-grounding loop before proceeding to verdict:
```

## 4.3 Renumber Stage 4 -> Stage 5 (~L21)

**Before:**

```
Stage 4 — Verdict:
```

**After:**

```
Stage 5 — Verdict:
```

---

## Verification (C gate for this phase)

Run from repo root `/Users/jun/Developer/new/700_projects/jawcode`:

```bash
# De-brand: zero Jawdev occurrences across the four touched files
grep -c "Jawdev" packages/coding-agent/src/prompts/jaw/orchestrate-p.md     # expect 0
grep -ric "Jawdev" packages/coding-agent/src/defaults/jwc/skills/jaw-interview/SKILL.md  # expect 0
grep -ric "Jawdev" packages/coding-agent/src/prompts/jaw/orchestrate-i.md   # expect 0
grep -ric "Jawdev" packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 0

# Contract rule presence
grep -c "DIFFLEVEL-ROADMAP-01" packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1
grep -c "PHASE-SPLIT-01"       packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1
grep -c "LEXICO-SPLIT-01"      packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1
grep -c "UNIT-RESIDENCE-01"    packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1
grep -c "UNIT-RESIDENCE-01"    packages/coding-agent/src/defaults/jwc/skills/jaw-interview/SKILL.md  # expect 1
grep -c "UNIT-RESIDENCE-01"    packages/coding-agent/src/prompts/jaw/orchestrate-i.md   # expect 1

# SOT-SYNC-01 presence
grep -c "SOT-SYNC-01"         packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1
grep -c "SOT-SYNC-01"         packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 1

# Stage renumbering in orchestrate-c.md
grep -c "five-stage"          packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 1
grep -c "three-stage\|four-stage" packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 0
grep -c "Stage 3 — SoT sync"  packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 1
grep -c "Stage 4 — Render"    packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 1
grep -c "Stage 5 — Verdict"   packages/coding-agent/src/prompts/jaw/orchestrate-c.md   # expect 1

# Removed phrases
grep -c "fill per cycle"       packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1 — the hit IS the DIFFLEVEL-ROADMAP-01 prohibition sentence (self-hit, not a regression)
grep -c "quick win"            packages/coding-agent/src/prompts/jaw/orchestrate-p.md   # expect 1 — the hit IS the PHASE-SPLIT-01 ban's negative example (self-hit, not a regression)

# INTERVIEW-CLASSIFY-01 says "three things" not "two classifications"
grep -c "settle three things"  packages/coding-agent/src/defaults/jwc/skills/jaw-interview/SKILL.md  # expect 1
grep -c "settle two"           packages/coding-agent/src/defaults/jwc/skills/jaw-interview/SKILL.md  # expect 0

# Build gate (modified files are .md only — tsc is unaffected, but run anyway)
bun run check:ts               # expect exit 0
# Prompt snapshot tests: the only snapshot files are under
# packages/coding-agent/test/core/__snapshots__/ (edit-hotspots-golden.test.ts.snap,
# diff-oracle.test.ts.snap) — these test diff/edit logic, NOT prompt text content.
# Tests that exercise the four target files (default-jwc-definitions.test.ts,
# jaw-interview-skill-policy.test.ts, workflow-surface-orchestrate.test.ts) use
# structural assertions (toContain, toMatchObject), not snapshot comparisons.
# If any prompt snapshot tests ARE added in the future, update them first:
#   bun run test:ts --update   # update snapshots only if failures are snapshot mismatches
# Then verify the full suite passes:
bun run test:ts                 # expect exit 0
```

Plus read-back: every After block matches the file verbatim; no other lines changed.

---

## Deploy/sync note

The four modified files are source-of-truth artifacts inside the jawcode
monorepo. They are imported as text at build time by
`packages/coding-agent/src/defaults/jwc-defaults.ts` (for skills) and by the
orchestrate prompt loader (for `orchestrate-*.md` files). Changes take effect
in the next `bun run build` or development server restart. No separate
copy/sync step is required — the source file IS the deployed artifact.

The `packages/jwc/defaults/cli-jaw/` directory contains a CLI-shipped copy
of cli-jaw defaults, but it does NOT mirror the `jwc/skills/` or
`prompts/jaw/` directories. No secondary sync is needed for this port.

---

## Adaptation notes (jawcode-specific decisions)

1. **No separate reference documents.** The contract source
   (`dev-pabcd/SKILL.md §3.1`) defines five named rules. In pabcd_initiative,
   these are defined in `dev-pabcd/SKILL.md` and cross-referenced from
   `dev-scaffolding` and `dev/SKILL.md`. Jawcode has NO `dev-pabcd` or
   `dev-scaffolding` — it blocks `dev-pabcd` at the system-prompt level
   ("Blocked skills: dev-pabcd — blocked; jwc orchestrate owns PABCD guidance
   natively"). The port injects the rules directly into the native orchestrate
   prompts and jaw-interview skill, which is how jawcode delivers all PABCD
   guidance.

2. **MOC file convention.** Jawcode uses `00_moc.md` (not `00_plan.md`) as the
   master index for loop plans. The DIFFLEVEL-ROADMAP-01 text references
   `00_moc.md` to match jawcode's existing system-prompt convention
   (`devlog/_plan/*/00_moc.md` — see system-prompt.md L46).

3. **Plan skill untouched.** `plan/SKILL.md` is marked SUPERSEDED (see its
   frontmatter: "SUPERSEDED by the native orchestrate plan stage"). All
   planning goes through `orchestrate p`. The port targets `orchestrate-p.md`
   only.

4. **Goal skill untouched.** `goal/SKILL.md` already references loop-spec
   headers, loop archetypes, and LOOP-PESSIMIST-01. It does not reference
   naming or documentation conventions — those belong in P, which is where
   plans are written. The goal skill delegates planning to `jwc orchestrate p`
   when no approved plan exists (see goal/SKILL.md "Role-agent delegation
   guidance" section).

5. **jaw-interview spec metadata.** The After text for INTERVIEW-CLASSIFY-01
   adds "record the unit path in the spec metadata." This is a semantic
   extension to the jaw-interview spec crystallization (Phase 4), not a
   structural change to the YAML frontmatter schema. The existing spec
   structure already has freeform `## Metadata` entries; the unit path
   fits there as a new line item.

6. **System prompt loop-execution paragraph untouched.** The system prompt
   (system-prompt.md L46, L93) already references `devlog/_plan/*/00_moc.md`
   and describes the loop plan structure. It does NOT contain naming
   conventions or documentation rules — those live in `orchestrate-p.md`.
   The system prompt needs no changes for this port.

7. **LOOP-CONTINUITY-01 cross-reference deliberately omitted.** The source
   contract (DIFFLEVEL-ROADMAP-01 in `dev-pabcd/SKILL.md`) ends with a
   trailing LOOP-CONTINUITY-01 cross-reference. This port omits it because
   jawcode already has its own loop-continuity surfaces that serve the same
   purpose: `orchestrate-p.md` L9 (loop-aware planning: identify next
   `pending` phase, reference "Phase N of M"), and `system-prompt.md` L46
   (loop-execution paragraph with MOC status table) / L93 (re-enter
   `orchestrate p` when `pending` phases remain). These native mechanisms
   make a separate LOOP-CONTINUITY-01 tag redundant in the jawcode port.

8. **No implementation-log reference document.** The canonical
   `dev-scaffolding/references/implementation-log.md` PABCD-routine table
   defines SOT-SYNC-01 at its C row; the scaffolding `dev-scaffolding/SKILL.md`
   section 2.1 defines the pre-patch SoT-discovery rule. Jawcode folds all
   PABCD-phase guidance into the `orchestrate-*.md` prompt files, not separate
   reference docs. The SOT-SYNC-01 C-row content is therefore ported to
   `orchestrate-c.md` (block 4.2) and the P-target/scaffolding content to
   `orchestrate-p.md` (block 3.3), matching the jawcode convention of inline
   orchestrate-prompt delivery.

## Open risks

1. **Snapshot tests.** Jawcode has extensive prompt snapshot tests under
   `packages/coding-agent/test/`. If any test snapshots include the exact
   text of `orchestrate-p.md`, `orchestrate-i.md`, `orchestrate-c.md`, or `jaw-interview/SKILL.md`,
   they will need updating after the patch. The B executor should run
   `bun run test:ts` and update snapshots if failures are snapshot mismatches
   only.

2. **cli-jaw dev-skill discovery.** The system prompt's `<dev-skill-routing>`
   block lists cli-jaw `dev-*` skills discovered from `~/.cli-jaw/skills/`.
   If a user has `dev-pabcd` installed via cli-jaw in their global skills,
   it will be listed but blocked ("Blocked skills: dev-pabcd"). The five
   rules are now duplicated between `dev-pabcd` (for pabcd_initiative /
   cli-jaw) and `orchestrate-p.md` / `orchestrate-c.md` (for jawcode). This is intentional:
   jawcode explicitly blocks `dev-pabcd` and delivers PABCD guidance natively.
   Future edits to the rules must be synced across both locations manually.

3. **Upstream changes.** Jawcode is a fork that tracks an upstream. If the
   upstream `orchestrate-p.md`, `orchestrate-c.md`, or `jaw-interview/SKILL.md`
   is updated, the port additions may conflict during merge. The additions are
   block-level insertions, not line edits (except the de-brand in 3.1), so
   merge conflicts should be resolvable.
