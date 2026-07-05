# 00_plan — Implementation-unit discipline as the harness default (de-branded, strict)

Date: 2026-07-05 (rev 3 — scope expanded to 4-harness roadmap by user directive)
Unit: `devlog/_plan/260705_difflevel_roadmap_default/`
Class: C3 (cross-agent contract change to the canonical methodology spec; durable audit trail required)

## Loop-spec

- **Loop archetype**: spec-satisfaction (verifier defines done)
- **Trigger**: user interview 2026-07-05 — the harness spec does not enforce the
  difflevel-plan routine; agents keep producing research-only units, effort-bucketed
  phase splits, bare-named plan files, and undocumented small work. Root causes: the
  routine is branded ("Jawdev style") and therefore opt-in; deferred concretization
  ("fill per cycle") is the default; no effort-bucketing ban; unit residence gated on
  work class.
- **Goal**: any agent following the pabcd_initiative skill family must, without being
  asked: (1) treat implementation-unit documentation as the unbranded DEFAULT process,
  (2) for multi-phase work produce the full roadmap with EVERY phase doc at diff-level
  up front, dependency-ordered, (3) never write bare-named or mixed research/implementation
  docs, (4) leave a numbered record in a unit for ALL work, down to C0 hotfixes.
- **Non-goals**: FSM/server code changes; renumbering existing unit folders;
  blind-copying text across harnesses (each port adapts to that repo's conventions).
- **Verifier**:
  - `grep -ric jawdev skills/` → 0 hits (full de-brand)
  - `DIFFLEVEL-ROADMAP-01` / `PHASE-SPLIT-01` / `LEXICO-SPLIT-01` / `UNIT-RESIDENCE-01`
    present at definition site (dev-pabcd §3.1/§3) and at every consumer touchpoint
    listed in 10_phase1
  - `grep -rn "fill per cycle" skills/` → 0; `grep -n "scaffold per-phase decade docs" skills/dev-pabcd/SKILL.md` → 0
  - independent A-phase audit (opus-4-6 per user instruction) + B read-back
- **Stop condition**: all MODIFY blocks in `10_phase1_harness_patch.md` applied and
  verified; no files outside the 4 listed touched.
- **Memory artifact**: this unit folder.
- **Expected terminal states**: DONE, or NEEDS_HUMAN if a gate decision is rejected.
- **Escalation condition**: any patch target text no longer matches (files drifted).

## Evidence baseline (why the harness fails today)

1. **Branding = opt-in escape hatch**: `dev-scaffolding/SKILL.md` gates the routine on
   "The user asks for Jawdev/Lidge-style structure" (3 places). A named style invites
   "the user didn't ask for that style" as a skip reason.
2. **Deferred concretization is the default**: `implementation-log.md` L37-38 "written
   in P of ITS cycle (pre-scaffold … fill per cycle)"; `dev-pabcd` §5 "scaffold
   per-phase decade docs up front" — empty scaffolds satisfy the letter of the rule.
3. **No effort-bucketing ban**: 0 grep hits across the skill family.
4. **Unit residence gated on class**: `implementation-log.md` "C0-C2 work does not get
   a unit folder"; `dev` §0.1 keeps change documentation only "when a worklog/changelog
   file is provided".
5. **Field evidence** (opus-4-6 scan of 12 recent units, 2026-07-05): newest unit
   `codexclaw/…/260705_hook_diet_skill_implicit` = master plan + 6 research docs,
   0 phase docs, 0 diff markers; bare-name violations still occur
   (`chatcli/devlog/_plan/mvpplan/`, historical `PLAN.md`/`DIFF_PLAN.md`).
   Good exemplar for the target state: `260703_gui_production_hardening`
   (8 phase docs, 27 NEW/MODIFY/DELETE blocks).
6. **Downstream reference survey** (for later port units, out of scope here):
   cli-jaw skills_ref has identical weaknesses incl. the 3 opt-in gates; codexclaw
   partial (decade numbering present, no upfront/ban rules); jawcode jwc family has
   no implementation-unit concept at all (6 skills, no devlog/numbering rules).

## Interview decisions (2026-07-05, binding)

1. **Depth**: ALL phases fully diff-level up front; later cycles' P does a stale
   re-verify of the pre-written doc, never writes it fresh.
2. **Split criterion**: dependency/architecture order (foundations → core →
   integration → hardening). Effort bucketing FORBIDDEN.
3. **Nature of fix**: harness spec improvement — the spec text enforces this, not
   per-request triggers.
4. **Scope (rev 3, supersedes rev 1-2)**: full 4-harness roadmap in THIS unit —
   Phase 1 pabcd_initiative (canonical), then cli-jaw, jawcode, codexclaw, each
   adapted to its own conventions, INCLUDING system-prompt and hook/config surfaces
   that inject planning/devlog rules, not only skill files.
5. **De-brand**: remove the "Jawdev" name entirely; the routine becomes anonymous
   STRICT rules — a named style is skippable, a rule is not. Interview phase also
   settles unit residence, not just class/archetype.
6. **Lexicographic strictness**: bare plan filenames are an A-phase FAIL; research
   (00-range) and implementation phase designs (decade ranges) are strictly separate
   documents.
7. **Universal unit residence**: every piece of work lands in an implementation unit.
   Ceremony scales down (C0/C1 skip PABCD), residence never does — a hotfix leaves a
   numbered record doc (e.g. `40_hotfix_slug.md`) in its owning unit stating what was
   done and why the fast path applied.
8. **SoT sync (rev 4)**: before patching a repo, FIND its general source-of-truth
   docs (`structure/`, architecture/INDEX) first; units that change
   architecture/contracts patch the SoT doc in the SAME unit (C gate); if the repo
   has no SoT doc, RECOMMEND creating one.

## New rule IDs introduced

| ID | Class | One-line summary | Definition site |
|----|-------|------------------|-----------------|
| DIFFLEVEL-ROADMAP-01 | STRICT | Multi-phase unit ⇒ first P writes EVERY phase doc to diff-level (copy-paste PRD); later P = stale re-verify + amend | dev-pabcd §3.1 |
| PHASE-SPLIT-01 | STRICT | Phases sliced/ordered by dependency/architecture; effort bucketing (quick-win/heavy, impact-effort) forbidden | dev-pabcd §3 P |
| LEXICO-SPLIT-01 | STRICT | Every unit doc numbered (lexicographic); bare names FAIL the audit; research and implementation designs never mix in one doc | dev-pabcd §3.1 |
| UNIT-RESIDENCE-01 | STRICT | All work belongs to an implementation unit; C0-C1 skip ceremony but MUST leave a numbered record doc | dev-pabcd §3.1 |
| SOT-SYNC-01 | DEFAULT | Find the repo's general SoT docs first; patch them in the same unit at C; recommend creating one if absent | dev-pabcd §3 C / dev-scaffolding §2.1 |

## Work-phase map (dependency-ordered)

Order rationale: canonical rule text must land first (Phase 1 defines the rule IDs
and wording every port adapts); cli-jaw is the live-deploy source the user works in
daily (Phase 2); codexclaw already partially adopts the routine so its port is a
delta (Phase 3); jawcode lacks the concept entirely and needs the largest adapted
surface, informed by all prior ports (Phase 4). One full PABCD cycle per phase.

| Phase | Doc | Outcome | Verifier |
|-------|-----|---------|----------|
| 1 | `10_phase1_harness_patch.md` | pabcd_initiative: 4 files patched — rule definitions (dev-pabcd), routine spec (implementation-log), scaffolding consumer (dev-scaffolding), router fast-path (dev); de-branded and hardened | grep assertions above + read-back audit |
| 2 | `20_phase2_cli_jaw.md` | cli-jaw: same contract ported into `skills_ref` + any system-prompt/hook surface that injects planning rules, per cli-jaw conventions | per-doc grep assertions + read-back audit |
| 3 | `30_phase3_codexclaw.md` | codexclaw: cxc/pabcd skill family + plugin hooks/prompt surfaces hardened (delta port — partial adoption exists) | per-doc grep assertions + read-back audit |
| 4 | `40_phase4_jawcode.md` | jawcode: jwc skill family + role agent prompts/defaults gain the implementation-unit contract (largest adaptation) | per-doc grep assertions + read-back audit |

Docs 20/30/40 are written to diff-level in THIS first P (DIFFLEVEL-ROADMAP-01),
from per-repo touchpoint inventories (opus-4-6 agents, exact paths + verbatim
quotes). A audits in two rounds: round 1 = 00+10 (canonical), round 2 = 20/30/40
once the inventories land. Later cycles' P re-verifies each pre-written doc for
staleness before B, per the rule itself.

## Risks

- **Semantic reversal (carried from rev 1)**: PHASE-SPLIT-01 replaces the
  "user-visible outcome unit" default and deletes "Do not plan a whole database/API
  foundation as one PABCD before any usable outcome exists." Intentional (user: 정석 /
  unlimited-time process); mitigated by "every phase closes verifiable".
- **Doc staleness**: all-upfront diffs go stale as earlier phases land. Accepted;
  mitigated by mandatory stale re-verify in each later cycle's P.
- **Record-doc overhead**: UNIT-RESIDENCE-01 adds one small numbered doc per hotfix.
  Accepted by user (rev-2 interview); the rule text keeps the record minimal
  (what/why-fast-path/evidence — not ceremony docs).
- **Cross-repo reference drift**: downstream harnesses still reference "§3.1 Jawdev
  Document Numbering" by its old heading; those repos are out of scope and will be
  fixed in their own port units. Within THIS repo all internal references are updated
  in the same patch.

## Attestation log

- 2026-07-05 P (rev 1): plan written; FSM server down ("port undefined") — per the
  agent-neutral runtime adapter, transition announced in reply and attested here.
  `{"from":"I","to":"P","did":"interview settled 4 binding decisions; wrote 00_plan.md + 10_phase1_harness_patch.md with 8 MODIFY blocks at diff-level"}`
- 2026-07-05 P (rev 2): user feedback expanded scope within the repo (de-brand,
  LEXICO-SPLIT-01, UNIT-RESIDENCE-01); downstream survey attached as evidence; both
  plan docs rewritten.
- 2026-07-05 P (rev 3) + P→A: user approved and expanded scope to the 4-harness
  roadmap ("pabcd 돌고 첫번째는 initiative에만, 그다음 cli-jaw/jawcode/codexclaw 전부,
  시스템 프롬프트·hook 설정 포함"). FSM server still down — attested here per the
  runtime adapter.
  `{"from":"P","to":"A","did":"rev-3 plan: 00_plan.md 4-phase dependency-ordered map + 10_phase1_harness_patch.md (4 files, 21 diff-level blocks); dispatched opus-4-6 audit (round 1: 00+10) and 3 parallel opus-4-6 port-touchpoint inventories for phases 2-4 docs"}`
- 2026-07-05 A round 1 (phase 1): opus-4-6 audit verdict **PASS**, 0 blockers, 3 warns
  + 1 note. All warns incorporated into the plan as blocks 1.6 (§9 depth-table record
  cell), 3.10 (folder-approval gate exemption), and a fixed verification grep. Note
  (self-compliance: A entered before 20/30/40 existed) acknowledged — round 2 audits
  those docs before any phase 2-4 B.
  `{"from":"A","to":"B","did":"opus-4-6 worker audited 00_plan.md + 10_phase1_harness_patch.md against repo: PASS with 3 warns, all folded into plan rev 3 (blocks 1.6/3.10 + grep fix)"}`
- 2026-07-05 B (phase 1): all 23 blocks applied to the 4 target files
  (skills/dev-pabcd/SKILL.md, skills/dev-scaffolding/references/implementation-log.md,
  skills/dev-scaffolding/SKILL.md, skills/dev/SKILL.md). Doc deviations (audit warns)
  were edited into 10_phase1 BEFORE coding past them, per the routine.
  `{"from":"B","to":"C","did":"applied 23 MODIFY blocks across 4 skill files in pabcd_initiative; plan doc amended first (blocks 1.6/3.10)"}`
- 2026-07-05 C (phase 1): verification greps all green —
  `jawdev hits: 0 files · DIFFLEVEL dev-pabcd:3 · LEXICO dev-pabcd:2 · UNIT-RES dev-pabcd:4 ·
  PHASE-SPLIT dev-pabcd:2 · UNIT-RES impl-log:2 · UNIT-RES dev-scaffolding:2 · UNIT-RES dev:1 ·
  fill-per-cycle:0 · pre-scaffold:0 · scaffold-EOL dev-pabcd:0`
  `{"from":"C","to":"D","did":"ran the 10_phase1 verification grep suite","checkOutput":"jawdev:0 files; DIFFLEVEL:3; LEXICO:2; UNIT-RES:4/2/2/1; PHASE-SPLIT:2; fill-per-cycle:0; pre-scaffold:0; scaffold-EOL:0","exitCode":0}`
- 2026-07-05 D (phase 1): **DONE**. Planned (rev 1-3 interview-driven), audited
  (round-1 PASS + warns), built (23 blocks), checked (grep suite green). Changed:
  4 skill files. Negative delta / pessimistic close-out: the FSM server being down
  means no server-side gate exercised these attestations — they are worklog-only;
  evidence that the direction is wrong would be a future unit where all-upfront
  diff docs went stale faster than the stale-recheck could absorb. Next: phases 2-4
  port docs (20/30/40) authored + audited, then one PABCD cycle per port.
- 2026-07-05 P (port docs) + A round 2: three opus-4-6 authors wrote 20/30/40 from
  the patched canonical + direct repo inspection; three independent auditors ran per
  doc. Verdicts: cli-jaw **FAIL** (3 blockers: file-count header, JDS-003 rename
  missing from test rewrite, verification-count self-inconsistency), codexclaw
  **FAIL** (1 blocker: "fill per cycle" verification self-hit — the prohibition
  sentence trips its own anti-regression grep), jawcode **PASS** (2 warns: dropped
  PHASE-SPLIT subtask/closure clause, contradictory snapshot-test verification
  line). Cross-cutting lesson: two of three ports independently dropped the same
  canonical subtask/closure clause — flagged for future rule-sync tooling.
  FAIL → fix → re-audit loop dispatched (fix all three docs; re-audit the two
  FAILs), per the A-phase repair rule.
- 2026-07-05 A round 3: fix agents resolved all findings (cli-jaw now 13 files incl.
  structure/ de-brand + HTML-regen deploy note; codexclaw verification self-hit fixed,
  PHASE-SPLIT clause restored, style normalized; jawcode warns applied). Re-audits:
  cli-jaw **PASS** (0 findings), codexclaw **PASS** (0 findings), jawcode PASS carried.
  All three port docs are now approved P artifacts.
- 2026-07-05 P amendment (rev 4, user directive): SOT-SYNC-01 added — find general
  SoT docs first, patch them in the same unit at C, recommend creation when absent.
  Blocks 1.7/1.8/2.5/3.11 added to 10_phase1 and applied to canonical (B delta);
  C greps: SOT dev-pabcd 2, dev-scaffolding 1, impl-log 1, jawdev still 0.
  Port docs receive equivalent SOT-SYNC-01 blocks before their B execution.
- 2026-07-05 B (phases 2-4, opus-4-6 executors + boss trailing observation):
  - **cli-jaw**: 13 files (skills_ref ×5 incl. goal, src ×5, test rename
    jawdev→devlog-skill-contract with JDS→DLC ×3, structure ×2). One legit B repair:
    builder.ts guide line shortened to fit test PSC-004's 1600-char window (both
    rule IDs kept); plan doc block 6.1 synced to the applied text afterward.
    Gates: tsc exit 0; gate:all 12/12; renamed test 3/3; npm test failures = 2
    pre-existing in untouched files. dev-pabcd skills_ref blocks were pre-applied
    by the parallel render-grounding session — verified verbatim, no conflict.
  - **codexclaw**: only dev/SKILL.md ×3 needed application (pabcd + dev-scaffolding
    + implementation-log pre-applied identically by the parallel session). Build 84
    files exit 0; tests 687/687.
  - **jawcode**: 4 prompt/skill files, zero drift, all 6 blocks verbatim; target
    tests pass (jaw-interview-skill-policy, workflow-surface-orchestrate, snapshots
    29/29); check:ts/test:ts failures all pre-existing in unrelated TS sources.
  `{"from":"B","to":"C","did":"three opus-4-6 executors applied 20/30/40 to their repos; boss trail-reviewed every runtime-prompt diff live (state-machine.ts, builder.ts, planaudit.ts, orchestrate-i/p/c.md, structure docs)"}`
- 2026-07-05 C (phases 2-4) + polish (boss, direct):
  1. jawcode orchestrate-c.md header said "four-stage" while the body numbers
     Stage 1-5 — polished to "five-stage … SoT sync → render grounding
     (conditional) → verdict"; 40_phase4 block 4.1 + greps synced.
  2. 40_phase4 verification self-hits corrected: "fill per cycle"/"quick win"
     expect 1 (the prohibition sentences themselves), not 0.
  3. 20_phase2 block 6.1 After synced to the applied PSC-004-window text
     (doc-code convergence).
  4. SOT-SYNC-01 dogfood: pabcd_initiative README.md (this repo's SoT) patched
     with the 2026-07-05 hardening record. cli-jaw structure/ docs were patched in
     phase 2; codexclaw has no structure/ SoT (recommendation: create one — noted);
     jawcode SoT surfaces are the prompt files themselves.
  Final cross-repo greps: jawdev = 0 on all target surfaces (canonical, cli-jaw
  skills_ref+src+tests+structure, codexclaw skills, jawcode jwc+prompts — the two
  jawcode "hits" are the `cliJawDevSkills` camelCase template variable, a false
  positive, not the brand); SOT-SYNC-01 present at all five runtime surfaces;
  jawcode header five-stage 1 / three|four-stage 0.
  `{"from":"C","to":"D","did":"final cross-repo grep suite + per-repo gates","checkOutput":"jawdev 0/0/0/0 (2 camelCase false positives); SOT-SYNC-01 2/2/1/2/1; five-stage 1, three|four-stage 0; tsc 0, gate:all 12/12, codexclaw 687 pass, jawcode target tests pass","exitCode":0}`
- 2026-07-05 D (unit close-out): **DONE** — all four phases executed and verified.
  Changed: canonical 5 files (4 skills + README SoT), cli-jaw 13, codexclaw 4 (3 by
  parallel session, 1 file this unit's executor), jawcode 5 (4 planned + header
  polish). NOT done (user-owned follow-ups): commits in all four repos (working
  trees left dirty for review, per no-proactive-git rule); cli-jaw deploy
  (`npm run build` + `jaw skill sync` + server restart) and docs/dev HTML
  regeneration; codexclaw ships on next session load; jawcode on next build.
  Negative delta (pessimistic close-out): FSM server was down the whole unit, so no
  server-side gate exercised any attestation — worklog-only discipline; the
  parallel render-grounding session pre-applying blocks in two repos means our
  "pre-applied" verification trusted verbatim-match, not independent application;
  the `cliJawDevSkills` variable keeps a case-insensitive jawdev grep from ever
  reaching literal 0 in jawcode. Evidence that would falsify the direction: a
  future multi-phase unit where upfront diff docs went stale faster than the
  stale-recheck absorbed, or record-doc fatigue on C0-C1 hotfixes.
