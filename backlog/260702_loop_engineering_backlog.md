# Loop-Engineering Alignment Backlog — 2026-07-02

Record of the PABCD × loop-engineering investigation (three independent lanes:
Claude Fable 5 web research, ChatGPT 5.5 Pro session, Codex gpt-5.5 xhigh repo-grounded
research) and the resulting adoption/backlog split. The adopted subset now lives in
`skills/dev-pabcd/SKILL.md` §11; everything else is future work tracked here.

## 1. Genealogy (for the eventual write-up)

Loop engineering was not born in June 2026 — it was *named* then. Simon Willison framed
"designing agentic loops" as a critical skill in September 2025; the June 2026 cluster is
Peter Steinberger ("design loops that prompt your agents") → Boris Cherny ("my job is to
write loops") → Addy Osmani's explainer that fixed the name, then press amplification and
an arXiv position paper formalizing a loop spec as trigger · goal · verification ·
stopping rule · memory.

Sources:
- https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
- https://addyosmani.com/blog/loop-engineering/ (also https://addyo.substack.com/p/loop-engineering)
- https://www.businessinsider.com/what-are-loops-ai-engineering-tips-2026-6
- https://arxiv.org/abs/2607.00038
- https://www.anthropic.com/engineering/building-effective-agents
- https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex

Three-lane consensus verdict: PABCD is a macro-loop instance of loop engineering with
precursor-like qualities (independently derived from a failure thesis: intent loss,
runaway "go", stale knowledge, hallucinated builds, compounding bias). The HITL→HOTL
shift (checkpoint approvals → Interview-front-loaded `/goal`) is *enabled* by model
capability gains but *justified* only by a strong external verification loop —
capability is a necessary condition, not the whole cause.

## 2. The plateau finding (900-nypc-mushroom / NEXT NATION)

Concrete counterexample to "just run more PABCD cycles": the NEXT NATION bot beats
reference and rush opponents across map sizes but plateaus against a strong economy
opponent on small maps (2W 4D 4L at N=51). The tournament verifier is deterministic and
perfect, yet C→B repair cycles cannot close the gap — the verifier says *losing*, never
*why*, and repair rings only produce local tweaks (hill climbing) on the existing
strategy. Return loops are corrective, not generative: they cannot inject the missing
strategic concept.

Adopted consequence (`dev-pabcd` §11.4, LOOP-ARCHETYPE-01): classify the problem type
before choosing loop shape —

- **Spec-satisfaction** (verifier defines *done*) → repair loop; converges.
- **Open-ended optimization** (verifier defines only *better*) → explore-and-select
  loop: parallel diverse candidates → same-instance evaluation → keep best-so-far →
  regenerate from winner; stop on plateau or budget; exit is `BUDGET_EXHAUSTED` with
  best candidate adopted, never `DONE`.

What breaks plateaus (ranked): (1) diversity injection — candidate strategies sourced
from domain-state evidence, not parameter space (extends §10 LOOP-CANDIDATE-ANCHOR-01);
(2) knowledge front-loading at P/Interview (playbooks, domain theory — the proactive
counterpart to reactive repair); (3) a stronger generator (frontier API raises each
candidate's ceiling but, inside an unchanged repair ring, still plateaus).

Open research lane (dispatched 2026-07-02, spark ×3 + ChatGPT Pro session continuation):
paper-grounded methods for the explore-and-select loop — LLM-guided evolutionary search
(FunSearch/AlphaEvolve line), quality-diversity (MAP-Elites), population self-play and
opponent modeling, plateau/no-progress detection and exploration scheduling. Results to
be appended here.

## 3. Adopted in this pass (skills/dev-pabcd §11 + P/§2.1 insertions)

- Loop-spec header in P for C2+ (trigger/goal/non-goals/verifier/stop/memory/terminal
  states/escalation; + resource scope in goal mode).
- Attestation evidence pointers (ATTEST-EVIDENCE-01): `did` carries artifact pointers
  (paths, changed files, command + exit code) even though the server gate stays
  form-only.
- Loop values (§11.1): feedback must change the next action; verifier > prompt; memory
  on disk; budget ≠ done; Interview yields a testable loop-spec, not solved intent.
- Terminal-state vocabulary (§11.2): DONE/NOOP/BLOCKED/UNSAFE/NEEDS_HUMAN/
  BUDGET_EXHAUSTED — skill-level (agent-recognized), per the design decision to keep the
  server thin (threat model = laziness, not malice).
- Repair-loop discipline (§11.3): repair-only-the-failing-delta; 2 fails → root-cause
  mode; 3 → replan/Interview; LOOP-DOOM-01 no-progress heuristic (3 same-phase
  attestation failures → forced Interview return, self-applied).
- Loop archetype split (§11.4) and unattended-loop resource policy (§11.5).

## 4. Future work (not in this pass)

| Item | Where | Notes |
|------|-------|-------|
| Server-side doom-loop gate | cli-jaw FSM | Count same-phase attestation failures per work-phase; N=3 → forced `orchestrate I`. Mechanical counting only — semantics stay in the skill. |
| Evidence-bound attestation (phase-specific artifact checks: diff exists, plan path resolves, checkOutput parsed) | cli-jaw FSM | Upgrade path from form-only; keep the human free pass. |
| Explore-and-select tooling | cli-jaw / project harnesses | Candidate matrix runner (parallel strategy variants × same seeds), best-so-far ledger, plateau detector wired to §10 death log. |
| Worktree isolation for parallel candidates/checkers | runtime-specific | Osmani loop primitive; needed once B parallelism is real. |
| Verifier ladder codification (deterministic → artifact → independent agent → human → model-judge+rubric) | dev-testing | GPT Pro proposal; dev-testing §9.5 is the natural owner. |
| Downstream ports of this delta | codexclaw `plugins/codexclaw/skills/`, jawcode `packages/coding-agent/src/defaults/jwc/skills/` | Per freshness-sweep propagation rules: adapt, never blind-copy, fork's own gates, local commits only. Dispatched 2026-07-02. |
| Observability for loops (where time/tokens go per phase) | cli-jaw dashboard | Currently a blind spot; harness-engineering sources treat it as a core layer. |

## 5. Rejected / deferred framings

- "Frontier API solves the plateau" — rejected as stated; adopted as component (3) of
  the plateau-breaking triad in §2 above.
- "Intent transfer is solved by Interview" — reframed per Codex lane: Interview produces
  a testable initial loop-spec; the Interview-return path is the mechanism for cyclic
  refinement (now §11.1 last bullet).
- Server-enforced terminal states — deferred by design decision (skill-level only).
