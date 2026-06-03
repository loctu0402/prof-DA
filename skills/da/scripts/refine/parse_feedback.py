#!/usr/bin/env python3
"""Extract filled sections from a review worksheet. Mechanical only - no interpretation.

Usage: parse_feedback.py <worksheet.txt>   # prints JSON list to stdout
Emits one object per section whose 'SUA DOI / FEEDBACK' field is non-empty.
"""
import sys, re, json, argparse

SECT = re.compile(r"^PHAN\s+\d+\s*-\s*(.+)$")
ANCH = re.compile(r"^\[anchor:\s*(.+?)\]\s*$")
NUMS = re.compile(r"^- So lieu:\s*(.*)$")
FB   = re.compile(r"^- SUA DOI / FEEDBACK:\s*(.*)$")

DELIM = re.compile(r"^-{6,}$")

def parse(text):
    blocks, cur, collecting_fb = [], None, False
    for line in text.splitlines():
        m = SECT.match(line.strip())
        if m:
            if cur: blocks.append(cur)
            cur = {"title": m.group(1).strip(), "section": None, "anchors": [], "feedback": []}
            collecting_fb = False
            continue
        if cur is None:
            continue
        if DELIM.match(line.strip()):
            collecting_fb = False
            continue
        if collecting_fb:
            cur["feedback"].append(line)
            continue
        a = ANCH.match(line.strip())
        if a:
            cur["section"] = a.group(1).strip(); continue
        n = NUMS.match(line)
        if n and n.group(1).strip() not in ("", "(khong co)"):
            leaves = [kv.split("=", 1)[0].strip() for kv in n.group(1).split("|") if "=" in kv]
            cur["anchors"] = [f"{cur['section']}.{lf}" for lf in leaves] if leaves else [cur["section"]]
            continue
        fb = FB.match(line)
        if fb:
            cur["feedback"] = [fb.group(1)]
            collecting_fb = True
            continue
    if cur: blocks.append(cur)
    out = []
    for b in blocks:
        feedback = "\n".join(b["feedback"]).strip()
        if feedback:
            b["feedback"] = feedback
            if not b["anchors"]:
                b["anchors"] = [b["section"]] if b["section"] else []
            out.append(b)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("worksheet")
    args = ap.parse_args()
    with open(args.worksheet, encoding="utf-8") as f:
        print(json.dumps(parse(f.read()), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
