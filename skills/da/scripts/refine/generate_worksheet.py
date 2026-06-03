#!/usr/bin/env python3
"""Render a non-tech per-section review worksheet from a report's data-bind anchors.

Usage: generate_worksheet.py <report.html>   # writes worksheet text to stdout
Section = dotted prefix of data-bind (f0.aum, drivers[0], scqr ...), titled by the
nearest preceding <h2>. Text-ish fields (takeaway/reading/note/resolution/lede/...) are
shown as "Noi dung hien tai"; the rest as "So lieu key=value".
"""
import sys, argparse
from html.parser import HTMLParser

TEXT_FIELDS = ("takeaway", "reading", "note", "resolution", "situation",
               "complication", "question", "lede", "signal", "headline")

def prefix_of(bind):
    # f0.aum.total -> f0.aum ; drivers[0].delta -> drivers[0] ; scqr.situation -> scqr
    return bind.rsplit(".", 1)[0] if "." in bind else bind

def leaf_of(bind):
    return bind.rsplit(".", 1)[1] if "." in bind else bind

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cur_title = "Mo dau"
        self.in_h2 = False
        self.cur_bind = None
        self.buf = []
        self.sections = []          # list of [prefix, title]
        self.seen = {}              # prefix -> index in self.sections
        self.values = {}            # (prefix, leaf) -> text

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "h2":
            self.in_h2 = True; self._h2 = []
        if "data-bind" in ad:
            self.cur_bind = ad["data-bind"]; self.buf = []

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_h2 = False
            self.cur_title = "".join(self._h2).strip() or self.cur_title
        if self.cur_bind is not None:
            bind, text = self.cur_bind, "".join(self.buf).strip()
            pre, leaf = prefix_of(bind), leaf_of(bind)
            if pre not in self.seen:
                self.seen[pre] = len(self.sections)
                self.sections.append([pre, self.cur_title])
            self.values[(pre, leaf)] = text
            self.cur_bind = None

    def handle_data(self, data):
        if self.in_h2: self._h2.append(data)
        if self.cur_bind is not None: self.buf.append(data)

def build(html):
    ex = Extractor(); ex.feed(html)
    lines = ["=== prof-DA REVIEW WORKSHEET ===",
             "HOW TO USE: type into 'SUA DOI / FEEDBACK' per section. Blank = section OK.",
             "Do NOT edit the [anchor: ...] line.", ""]
    for i, (pre, title) in enumerate(ex.sections, 1):
        leaves = [(p, l) for (p, l) in ex.values if p == pre]
        texts = [ex.values[(p, l)] for (p, l) in leaves if l in TEXT_FIELDS and ex.values[(p, l)]]
        nums = [(l, ex.values[(p, l)]) for (p, l) in leaves
                if l not in TEXT_FIELDS and ex.values[(p, l)]]
        lines += ["-" * 60, f"PHAN {i} - {title}", f"[anchor: {pre}]",
                  "- Noi dung hien tai: " + (" | ".join(texts) if texts else "(khong co)"),
                  "- So lieu: " + (" | ".join(f"{l}={v}" for l, v in nums) if nums else "(khong co)"),
                  "- SUA DOI / FEEDBACK:", ""]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    args = ap.parse_args()
    with open(args.report, encoding="utf-8") as f:
        html = f.read()
    sys.stdout.write(build(html))

if __name__ == "__main__":
    main()
