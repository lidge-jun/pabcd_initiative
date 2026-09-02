#!/usr/bin/env bash
# Reproducible rule-id census across the three skill trees.
#
# Named rules in this ecosystem follow the FAMILY-TOPIC-NN convention
# (DEV-GIT-COMMIT-01, FE-RENDER-PATH-02, ...). Counting the ids is a cheap,
# exact parity signal: a rule either has an id in the tree or it does not.
#
# What it cannot tell you: whether a rule that exists in both trees says the
# SAME thing. Drift detection is a read, not a count -- see 001_rule_gap_census.md
# "What the census cannot see".
#
# Usage:  bash gap-census.sh [path-to-700_projects]
# Exit:   0 always; this is a report, not a gate.
set -uo pipefail

# --added <base> <head> runs the reverse (invention) check instead of the gap census.
MODE=gap; REV_BASE=origin/main; REV_HEAD=HEAD
if [ "${1:-}" = "--added" ]; then
  MODE=added; REV_BASE="${2:-origin/main}"; REV_HEAD="${3:-HEAD}"; shift 3 || shift $#
fi
ROOT="${1:-$HOME/Developer/new/700_projects}"
RGX='\b[A-Z][A-Z0-9]+(-[A-Z0-9]+)+-[0-9]{2}\b'
# PCRE form for the reverse check at the bottom: git grep's default ERE has no \b, so the
# same intent needs --perl-regexp there.
RULE_PCRE='\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{2}\b'
CXC="$ROOT/codexclaw/plugins/codexclaw/skills"
# The reverse check needs the WHOLE source repo, not the dev-family scope: a rule may
# legitimately live in a codexclaw runtime skill and still be a real upstream rule, and
# calling that an invention is the error this check exists to avoid making.
CXC_ALL="$ROOT/codexclaw"
PI="$ROOT/pabcd_initiative/skills"
JW="$ROOT/cli-jaw/skills_ref"

for d in "$CXC" "$PI" "$JW"; do
  [ -d "$d" ] || { echo "missing tree: $d" >&2; exit 2; }
done

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

# codexclaw skills that have a counterpart in BOTH targets. Rules defined only
# in codexclaw-runtime skills (loop, qa, search, orchestrate, recall, remote,
# interview, skill-hub, worktree-guardian, ast-grep, goalplan, kwrite,
# lunasearch, repo-map, dev-diagram-viewer) are reported separately because
# they need a HOME DECISION in the targets, not a copy.
devfam=(dev pabcd dev-architecture dev-backend dev-code-reviewer dev-data
        dev-debugging dev-devops dev-frontend dev-scaffolding dev-security
        dev-testing dev-uiux-design)

ids() { rg -o "$RGX" "$1" -N --no-filename 2>/dev/null | sort -u; }

for s in "${devfam[@]}"; do ids "$CXC/$s"; done | sort -u > "$TMP/cxc.txt"
ids "$PI" > "$TMP/pi.txt"
for d in "$JW"/jaw-dev "$JW"/jaw-dev-*; do ids "$d"; done | sort -u > "$TMP/jaw.txt"

# The FULL codexclaw tree, runtime skills included. Needed only to classify
# target-only rules: a rule the targets own can be absent from the dev family
# yet present in a runtime skill (DIVERGE-TIER-01 lives in loop/SKILL.md), in
# which case "codexclaw does not have it" is an artifact of the dev-family
# scope rather than a fact about the ecosystem. Diffing target-only against
# the dev-family set alone reports those as upstream inventions and invites a
# port that removes them.
ids "$CXC" > "$TMP/cxc_all.txt"

comm -23 "$TMP/cxc.txt" "$TMP/pi.txt"  > "$TMP/gap_pi.txt"
comm -23 "$TMP/cxc.txt" "$TMP/jaw.txt" > "$TMP/gap_jaw.txt"

# target-only, split by whether codexclaw has the id anywhere at all
comm -13 "$TMP/cxc.txt" "$TMP/pi.txt"  > "$TMP/only_pi.txt"
comm -13 "$TMP/cxc.txt" "$TMP/jaw.txt" > "$TMP/only_jaw.txt"
comm -23 "$TMP/only_pi.txt"  "$TMP/cxc_all.txt" > "$TMP/only_pi_true.txt"
comm -23 "$TMP/only_jaw.txt" "$TMP/cxc_all.txt" > "$TMP/only_jaw_true.txt"
comm -12 "$TMP/only_pi.txt"  "$TMP/cxc_all.txt" > "$TMP/only_pi_artifact.txt"
comm -12 "$TMP/only_jaw.txt" "$TMP/cxc_all.txt" > "$TMP/only_jaw_artifact.txt"

n() { wc -l < "$1" | tr -d ' '; }

cat <<EOF
== inventory ==
codexclaw dev-family rule ids : $(n "$TMP/cxc.txt")
pabcd_initiative skills/      : $(n "$TMP/pi.txt")
cli-jaw jaw-dev* family       : $(n "$TMP/jaw.txt")

== gap ==
absent anywhere in pabcd_initiative : $(n "$TMP/gap_pi.txt")
absent anywhere in jaw-dev*         : $(n "$TMP/gap_jaw.txt")
needed by both                      : $(comm -12 "$TMP/gap_pi.txt" "$TMP/gap_jaw.txt" | wc -l | tr -d ' ')
pabcd_initiative only               : $(comm -23 "$TMP/gap_pi.txt" "$TMP/gap_jaw.txt" | wc -l | tr -d ' ')
cli-jaw only                        : $(comm -13 "$TMP/gap_pi.txt" "$TMP/gap_jaw.txt" | wc -l | tr -d ' ')

== target-only rules, genuinely absent from ALL of codexclaw (NEVER delete these) ==
pabcd_initiative : $(tr '\n' ' ' < "$TMP/only_pi_true.txt")
cli-jaw          : $(tr '\n' ' ' < "$TMP/only_jaw_true.txt")

== target-only by dev-family scope ONLY -- codexclaw has these in a runtime skill ==
pabcd_initiative : $(tr '\n' ' ' < "$TMP/only_pi_artifact.txt")
cli-jaw          : $(tr '\n' ' ' < "$TMP/only_jaw_artifact.txt")
EOF

DEVPATHS=()
for s in "${devfam[@]}"; do DEVPATHS+=("$CXC/$s"); done

# Locate a rule's text. Search the dev-family skills FIRST, then the whole tree.
# Order matters: a runtime-only skill often carries a POINTER to a rule the
# dev family owns -- loop/SKILL.md:364 says "Canonical rule ids:
# DEV-GIT-COMMIT-01, ..." while the rule itself lives at dev/SKILL.md:406.
# Searching the whole tree first reports the pointer and mis-attributes
# ownership, which is how a port ends up copying a cross-reference instead of
# a rule.
locate() {
  local id="$1" hit=""
  for scope in "dev-family" "whole-tree"; do
    local -a paths
    if [ "$scope" = "dev-family" ]; then paths=("${DEVPATHS[@]}"); else paths=("$CXC"); fi
    hit=$(rg -n "^#{2,4}.*\b$id\b" "${paths[@]}" --no-heading 2>/dev/null | head -1)
    [ -z "$hit" ] && hit=$(rg -n "^\s*[-*]\s*\*\*.*\b$id\b" "${paths[@]}" --no-heading 2>/dev/null | head -1)
    [ -z "$hit" ] && hit=$(rg -n "^\|\s*\**$id" "${paths[@]}" --no-heading 2>/dev/null | head -1)
    [ -z "$hit" ] && hit=$(rg -n "\b$id\b" "${paths[@]}" --no-heading 2>/dev/null | head -1)
    [ -n "$hit" ] && { local f=${hit%%:*} r=${hit#*:}; echo "${f#"$CXC"/}:${r%%:*} [$scope]"; return; }
  done
  echo "UNLOCATED"
}

echo
echo "== agent-neutrality scan =="
# Runs on the TARGET tree, not the source. Every token here is a host-specific name
# that has no meaning in an agent-neutral publication.
#
# `ima2` is in this list because it got through. The 010 commit's hand-written grep
# covered `cxc`, `.codexclaw`, `SubagentStop`, `cli-jaw` and `jaw ` -- but not the name
# of a local image-generation CLI, so six references to it rode in with two reference
# files and were only caught later by a wider sweep. A gate you retype per commit
# checks what you remembered that day; this one is the same every time.
#
# Attribution is allowed and deliberately not matched: "via codexclaw", "the codexclaw
# devlog", and a cross-runtime comparison row naming several runtimes are provenance,
# not vocabulary. Provenance a reader cannot verify is still better than a claim with
# no source.
NEUTRALITY_TOKENS='\bcxc [a-z]|\bcxc-[a-z]|\.codexclaw|SubagentStop|UserPromptSubmit|PreToolUse|PLUGIN_ROOT|LOOP_ARM|spawn_agent|wait_agent|followup_task|send_input|close_agent|resume_agent|interrupt_agent|tool_search|update_plan|request_user_input|agent_type|create_goal|browser:control|chrome:control|computer-use:|agbrowse|\bima2\b|clawhub|hermes|Codexclaw-First|E1-E8|testReceiptPath|auditVerdict|auditResidual|coerceAttest'
# references/repo-map-capability.md is exempt by design. Its whole purpose is a
# cross-harness comparison of how each downstream runtime ships the same capability, so
# it names codexclaw's `cxc-repo-map`, cli-jaw's `repo-map`, and jawcode's search table
# side by side. Naming another ecosystem's skill IN A COMPARISON is not adopting its
# vocabulary -- stripping those names would leave a comparison table with nothing to
# compare. Scoped to that one file rather than to the token, so a `cxc-` reference
# anywhere else still fails.
hits=$(rg -n "$NEUTRALITY_TOKENS" "$PI" 2>/dev/null \
  | rg -v 'cxc map|via codexclaw' \
  | rg -v 'repo-map-capability\.md' || true)
if [ -z "$hits" ]; then
  echo "clean: no host-specific vocabulary in pabcd_initiative/skills"
else
  echo "$(echo "$hits" | wc -l | tr -d ' ') LEAK(S):"
  echo "$hits" | sed 's/^/  /'
fi

echo
echo "== gap detail: rule -> codexclaw source file:line =="
for list in "$TMP/gap_pi.txt" "$TMP/gap_jaw.txt"; do
  case "$list" in *gap_pi*) echo "-- pabcd_initiative --";; *) echo "-- cli-jaw --";; esac
  while read -r id; do
    [ -z "$id" ] && continue
    printf '  %-34s %s\n' "$id" "$(locate "$id")"
  done < "$list"
done

# ─── reverse direction: did anything get INVENTED? ──────────────────────────
# The gap above proves codexclaw ⊆ target. A rule invented here satisfies that too, so it
# cannot answer "is every ported rule traceable to codexclaw" -- the question the
# acceptance criteria actually ask. This checks the other direction: every rule id that a
# branch ADDS must exist somewhere in codexclaw, or be a known repository-original.
#
# Two mechanical hazards, both of which produced a wrong answer before being fixed:
#   - macOS grep has no -P, so a \b pattern silently matches nothing. A reference set that
#     comes back empty makes EVERY added rule look invented; this aborts instead.
#   - git grep's default ERE has no \b either, so the pattern needs --perl-regexp.
#
# Usage: gap-census.sh --added <base-rev> <head-rev>
if [ "$MODE" = "added" ]; then
  base="$REV_BASE"; head="$REV_HEAD"
  echo
  echo "== reverse check: rules ADDED between $base and $head =="
  git grep -ohP "$RULE_PCRE" "$base" -- 'skills/' 2>/dev/null | sort -u > "$TMP/rev_base.txt"
  git grep -ohP "$RULE_PCRE" "$head" -- 'skills/' 2>/dev/null | sort -u > "$TMP/rev_head.txt"
  comm -13 "$TMP/rev_base.txt" "$TMP/rev_head.txt" > "$TMP/rev_added.txt"
  rg -oIN --pcre2 "$RULE_PCRE" "$CXC_ALL" -g '*.md' 2>/dev/null | sort -u > "$TMP/rev_cxc.txt"
  echo "  base=$(wc -l <"$TMP/rev_base.txt"|tr -d ' ')  head=$(wc -l <"$TMP/rev_head.txt"|tr -d ' ')  added=$(wc -l <"$TMP/rev_added.txt"|tr -d ' ')  codexclaw=$(wc -l <"$TMP/rev_cxc.txt"|tr -d ' ')"
  if [ ! -s "$TMP/rev_cxc.txt" ]; then
    echo "  ABORT: codexclaw reference set is empty -- the result would be meaningless."
    exit 2
  fi
  # Rules this repository owns. Each is here because it is genuinely absent from codexclaw
  # and that absence is intended, not because the check was inconvenient.
  #   FE-MOTION-EXPERIENCE-01  arrived with the pre-existing uncommitted design work the
  #                            objective required be committed rather than discarded.
  #   INTERVIEW-DIVERGE-01     existed in this repo's own devlog and docs metadata before
  #                            the port; the port realized it in the skills tree.
  OWNED='^(FAMILY-FRESH-01|FE-MOTION-EXPERIENCE-01|INTERVIEW-CLASSIFY-01|INTERVIEW-DIVERGE-01|PABCD-AUTO-01|PROMPT-ROUTING-01)$'
  n=0
  while read -r id; do
    [ -z "$id" ] && continue
    grep -qxF "$id" "$TMP/rev_cxc.txt" && continue
    if echo "$id" | rg -q "$OWNED"; then
      echo "  repository-original (expected): $id"
    else
      echo "  UNTRACEABLE -- neither in codexclaw nor a known original: $id"
      n=$((n+1))
    fi
  done < "$TMP/rev_added.txt"
  echo "  >>> unexplained additions: $n"
  exit $([ "$n" -eq 0 ] && echo 0 || echo 1)
fi
