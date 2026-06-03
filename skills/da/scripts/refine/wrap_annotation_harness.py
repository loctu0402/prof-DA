#!/usr/bin/env python3
"""Wrap a report HTML in the inline-annotation harness (Tier 3, refine-time only).
Usage: wrap_annotation_harness.py <report.html>  # writes <report>.annotate.html, prints its path
"""
import sys, os, argparse
HERE = os.path.dirname(os.path.abspath(__file__))

def wrap(html, overlay_js):
    script = "\n<script>\n" + overlay_js + "\n</script>\n"
    low = html.lower()
    i = low.rfind("</body>")
    return (html[:i] + script + html[i:]) if i != -1 else (html + script)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("report")
    a = ap.parse_args()
    with open(a.report, encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(HERE, "annotate_overlay.js"), encoding="utf-8") as f:
        overlay = f.read()
    base, ext = os.path.splitext(a.report)
    outp = base + ".annotate" + ext
    with open(outp, "w", encoding="utf-8") as f:
        f.write(wrap(html, overlay))
    print(outp)

if __name__ == "__main__":
    main()
