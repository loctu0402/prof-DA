#!/usr/bin/env python3
"""comments.json (from the inline annotation overlay) -> change-set JSON.
Output shape matches parse_feedback.py so the apply step is identical.
Usage: parse_comments.py <comments.json>
"""
import sys, json, argparse
from collections import OrderedDict

def prefix_of(anchor):
    return anchor.rsplit(".", 1)[0] if "." in anchor else anchor

def parse(comments):
    groups = OrderedDict()
    for c in comments:
        anchor = (c.get("anchor") or "").strip()
        if not anchor:
            continue
        pre = prefix_of(anchor)
        g = groups.setdefault(pre, {"section": pre, "title": "(inline)", "anchors": [], "feedback": []})
        if anchor not in g["anchors"]:
            g["anchors"].append(anchor)
        sel = (c.get("selected_text") or "").strip()
        com = (c.get("comment") or "").strip()
        if com:
            g["feedback"].append((f'[selected: "{sel}"] ' if sel else "") + com)
    out = []
    for g in groups.values():
        if g["feedback"]:
            g["feedback"] = "\n".join(g["feedback"])
            out.append(g)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("comments")
    a = ap.parse_args()
    with open(a.comments, encoding="utf-8") as f:
        print(json.dumps(parse(json.load(f)), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
