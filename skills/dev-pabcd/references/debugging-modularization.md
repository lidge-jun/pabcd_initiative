# Debugging Modularization (SoT, agent-neutral)

> Source-of-truth contract for runtime-specific debugging references shared across
> the pabcd_initiative harnesses (codexclaw, cli-jaw, jawcode). This file names the
> structure and content contract; each harness ships the references in its own
> skill directory.

## Status

| Harness | Location | Status |
| --- | --- | --- |
| codexclaw | `plugins/codexclaw/skills/dev-debugging/references/runtimes/` + `tools/` | SHIPPED (2026-07-07) |
| cli-jaw | `skills_ref/dev-debugging/references/runtimes/` + `tools/` | SHIPPED (2026-07-07, synced from codexclaw) |
| jawcode | n/a (fork upstream) | NOT STARTED — port when jawcode's dev-debugging gains references |

## Structure Contract

```text
references/
  runtimes/
    node.md     # Node.js / tsx / Bun / Deno
    python.md   # CPython 3.9+
    rust.md     # cargo / tokio
    go.md       # Delve / pprof
  tools/
    playwright.md   # browser-surface deterministic repro
```

Each runtime file MUST include: Phase 0 environment detection, attach/launch
recipes, the runtime's debugging hierarchy (lightest tool first), a
silent-failure pattern table, and a cleanup section. Lineage: lazycodex
`debugging/references/runtimes/` + gpt-5.5 Tier-2 external research round.

## Slop Cleanup Checklist (REVIEW-SLOP-01)

Shipped in `dev-code-reviewer` SKILL.md on both codexclaw and cli-jaw. 9
categories adapted from lazycodex `remove-ai-slops`: stylistic (obvious
comments, over-defensive, excessive complexity), structural (needless
abstraction, boundary violations, oversized >250L as smell not mandate),
hidden cost (perf equivalences, scope leaks), coverage (missing behavior
tests). Safety invariant: green tests before removing code.

## Sources

- lazycodex `debugging/references/runtimes/{node,python,rust,go}.md`
- lazycodex `remove-ai-slops/SKILL.md` (9-category taxonomy)
- gpt-5.5 research round (2026-07-07): Node 22+ inspect-wait, Python 3.14
  PEP 768, Vitest 4 debugging, Miri/tokio-console, Delve/pprof, Playwright
  agent integration
