#!/usr/bin/env python3
"""Phase-1 verifier for catalog-discovery.yaml (design/UX-first invariants).

Checks referential integrity + the design-LEADS ordering invariants, including the
audit fix #5 stage/axis-match check. Prints PASS/FAIL per invariant, exits non-zero on any FAIL.
"""
import sys, pathlib

try:
    import yaml
except ImportError:
    print("FAIL: pyyaml not installed (pip install pyyaml)"); sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[3]
CAT = ROOT / "skills/dev-pabcd/references/catalog-discovery.yaml"

def main() -> int:
    doc = yaml.safe_load(CAT.read_text(encoding="utf-8"))
    entries = doc["entries"]
    ids = {e["id"] for e in entries}
    order = doc["axis_order"]
    # axis -> declared stage from axis_order
    axis_stage = {a["axis"]: a["stage"] for a in order}
    fails = []

    def check(name, ok, detail=""):
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" — {detail}" if detail and not ok else ""))
        if not ok: fails.append(name)

    # 1. design leads: axis_order[0] is design at stage 1
    check("axis_order[0] is design/stage1", order[0]["axis"] == "design" and order[0]["stage"] == 1)

    # 2. only design may be stage 1
    s1 = [a["axis"] for a in order if a["stage"] == 1]
    check("only design at stage 1", s1 == ["design"], f"stage1 axes={s1}")

    # 3. all 6 design dials present at stage 1, required, with question_options
    DIALS = {"design.mood","design.lightness","design.density","design.shape","design.typography","design.motion"}
    dmap = {e["id"]: e for e in entries if e.get("axis") == "design"}
    check("all 6 design dials present", DIALS <= set(dmap), f"missing={DIALS - set(dmap)}")
    for d in sorted(DIALS & set(dmap)):
        e = dmap[d]
        check(f"{d} stage==1", e.get("stage") == 1)
        check(f"{d} required", e.get("required") is True)
        check(f"{d} has question_options", bool(e.get("question_options")))

    # 4. every entry's stage matches its axis in axis_order (audit fix #5)
    for e in entries:
        exp = axis_stage.get(e["axis"])
        check(f"{e['id']} stage matches axis_order", e.get("stage") == exp, f"got {e.get('stage')} want {exp}")

    # 5. every stage-3 entry has non-empty derived_from
    for e in entries:
        if e.get("stage") == 3:
            check(f"{e['id']} has derived_from", bool(e.get("derived_from")))

    # 6. referential integrity: implies/conflicts/derived_from ids all resolve
    for e in entries:
        for field in ("implies", "conflicts", "derived_from"):
            for ref in e.get(field, []) or []:
                check(f"{e['id']}.{field} -> {ref} resolves", ref in ids)

    print(f"\n{'ALL PASS' if not fails else 'FAILED: ' + ', '.join(fails)}")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
