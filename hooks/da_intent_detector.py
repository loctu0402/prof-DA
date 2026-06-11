#!/usr/bin/env python3
"""
prof-DA dispatch layer 2/2 - UserPromptSubmit hook: deterministic DA-intent catch.

Skill auto-fire from frontmatter descriptions is probabilistic; this hook is the
deterministic floor under it. It folds the prompt to lowercase ASCII (diacritics
stripped, so "du doan" and "dự đoán" both match), scans for DA-intent signals grouped
by mode, and injects a routing nudge naming the matched keywords + likely mode.

Layer 1/2 is session_start_dispatch.py (SessionStart) - the standing protocol that
tells the agent to treat this nudge as a hard signal.

It only ADDS context (never blocks). Fail-open: any error -> add nothing. Silent when
the prompt is a slash command, mentions prof-DA explicitly, or matches nothing.

- part of prof-DA . Loc Tu, 2026
"""
from __future__ import annotations
import json
import re
import sys
import unicodedata

# Signals are stored FOLDED (lowercase ASCII, diacritics stripped). Each is matched with a
# left word boundary so prefixes work ("predict" catches "prediction") while embedded hits
# don't ("con chua" does not catch "on chua", "macron" does not catch "cron").
MODE_SIGNALS = {
    "query": [
        "so lieu", "lay data", "pull data", "show me data", "get the numbers",
        "breakdown", "ty le", "ti le", "bao nhieu user", "tong so", "trung binh",
        "so sanh", "compare", "trend", "xu huong", "viet sql", "write sql",
        "query data", "thong ke",
    ],
    "insight": [
        "tai sao", "vi sao", "why is", "why did", "root cause", "nguyen nhan",
        "dot bien", "deep dive", "phan tich", "analyze", "analysis",
        "dieu gi xay ra", "what happened", "what changed", "hypothesis",
        "gia thuyet", "giai thich", "insight",
    ],
    "process": [
        "du doan", "du bao", "forecast", "predict", "seasonal", "mua vu",
        "time series", "chuoi thoi gian", "sarima", "arima", "prophet",
        "machine learning", "train model", "build model", "hoi quy", "regression",
        "classification", "phan loai", "clustering", "phan cum", "segmentation",
        "phan khuc", "churn", "propensity", "scoring", "uplift", "anomaly",
        "bat thuong", "a/b test", "ab test", "clean data", "lam sach data",
        "data quality", "chat luong du lieu", "feature engineering", "eda",
        "kham pha data", "missing value", "outlier", "tien xu ly", "preprocess",
        "wrangle", "ml case study",
    ],
    "model": [
        "data model", "dbt", "kimball", "medallion", "design schema", "build mart",
        "data mart", "table contract", "dwh",
    ],
    "frame": [
        "kickoff", "khong biet bat dau", "frame project", "scope project",
        "metric nao", "metric define", "do luong", "phuong phap tinh",
        "phuong phap do", "tiem nang", "potential size", "opportunity sizing",
        "cohort", "stakeholder muon", "kpi",
    ],
    "automate": [
        "schedule job", "schedule pipeline", "schedule report", "len lich chay",
        "cron", "tu dong hoa", "automation", "automate", "chay hang ngay",
        "chay hang tuan", "chay hang thang", "airflow", "dagster", "prefect",
        "backfill", "recurring", "fail-alert", "email on fail",
    ],
    "report": [
        "bao cao", "dashboard", "executive summary", "exec summary", "share-out",
        "trinh bay ket qua", "bieu do", "report", "slide", "deck",
        "visualization", "visualisation", "chart",
    ],
    "review": [
        "review report", "review bai", "review lai", "audit", "ok chua",
        "on chua", "gop y", "kiem tra bai", "du muc chua", "feedback bai",
    ],
    "fix": [
        "fix pipeline", "sua pipeline", "pipeline loi", "pipeline fail", "so sai",
        "sai so", "wrong number", "missing data", "thieu data", "rerun",
        "patch report", "cache loi", "khong co data", "so lieu sai",
    ],
    "submit": [
        "submit report", "nop bao cao", "finalize", "duyet lan cuoi",
    ],
    "workspace": [
        "don workspace", "workspace bua", "to chuc lai workspace",
        "sap xep lai thu muc", "rebuild index", "scaffold workspace", "build index",
    ],
}


def fold(text: str) -> str:
    text = text.lower().replace("đ", "d").replace("Đ", "d")
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def main() -> int:
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        data = json.loads(raw) if raw.strip() else {}
        prompt = (data.get("prompt") or "").strip()
        if not prompt or prompt.startswith("/"):
            return 0

        folded = fold(prompt)
        if "prof-da" in folded:
            return 0

        matched, mode_hits = [], {}
        for mode, signals in MODE_SIGNALS.items():
            for sig in signals:
                if re.search(r"\b" + re.escape(sig), folded):
                    matched.append(sig)
                    mode_hits[mode] = mode_hits.get(mode, 0) + 1

        if not matched:
            return 0

        top_modes = sorted(mode_hits, key=mode_hits.get, reverse=True)[:2]
        note = (
            "[prof-DA dispatch] DA-intent keywords detected in this prompt: "
            + ", ".join(matched[:6])
            + ". Likely mode: " + " / ".join(top_modes)
            + ". Invoke Skill(prof-DA:da) - or /prof-DA:" + top_modes[0]
            + " directly if the mode is obvious - BEFORE answering. Do not hand-answer "
            "DA work without the skill. Skip only if the user explicitly declined "
            "prof-DA or the match is clearly incidental (e.g. the prompt is about "
            "code/tooling, not the user's data)."
        )
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": note,
            }
        }, ensure_ascii=False))
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
