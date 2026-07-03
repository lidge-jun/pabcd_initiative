# Dispatch Affordance Port Backlog — 2026-07-03

cli-jaw shipped the dispatch-affordance work (4 PABCD work-phases,
`cli-jaw/devlog/_plan/260703_dispatch_affordance_consolidation/`): server-side
task_tags forwarding + batch verdict persistence + batch wait:false→202
(pre-claimed runIds) + dead buildPlanPrompt removal; CLI `--task-file` /
`--agents-file` / `--task-tags` / `--async`; boss-prompt rewrite to async-first
file-based dispatch (all `timeout=600000` fear-prose removed); dev-pabcd skill
§7 example ported to repo + instance copies (both `last-verified: 2026-07-03`).

## Port status per copy

| Copy | Status |
|------|--------|
| cli-jaw `skills_ref/dev-pabcd` | DONE (same change) |
| `~/.cli-jaw/skills_ref/dev-pabcd` (instance) | DONE (same change, dispatch-delta only — full re-sync of unrelated lag still pending, tracked separately) |
| **This initiative** `skills/dev-pabcd` | **NO CHANGE NEEDED** — verified 2026-07-03: the agent-neutral copy contains zero `cli-jaw dispatch` references (grep evidence in session log); its generic "worker dispatch" language already covers file-based briefs. |
| codexclaw `plugins/codexclaw/skills/` (cxc-*) | TODO — adapt, never blind-copy: if the cxc runtime exposes an employee-dispatch surface, mirror the async-first + brief-file principle in its own idiom; run the fork's own gates; local commits only. |
| jawcode `packages/coding-agent/src/defaults/jwc/skills/` | TODO — same adaptation rule; jwc role-agent prompts may also reference dispatch mechanics. |

## Principle delta worth porting (not just wording)

1. **Async-first delegation**: blocking-with-foreign-timeout is a failure class,
   not a configuration; delegation surfaces should return a handle immediately
   and re-inject results.
2. **Brief-file over inline-quoting**: multi-line task briefs never belong in
   shell-quoted arguments (motor-task failure).
3. **Zero failure-compensation prose**: prompts that shout about a footgun are
   fossil evidence — fix the tool, delete the warning (cli-jaw removed ~26
   lines of ⏰/pendingReplay fear-content after the CLI fix).
