import subprocess, sys, os, tempfile, json

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "parse_comments.py")
COMMENTS = json.dumps([
    {"anchor": "f0.aum.takeaway", "selected_text": "Muc giam nam trong bien dao dong", "comment": "Doi: nhan manh rut som"},
    {"anchor": "f0.aum.total", "selected_text": "11.493,8", "comment": "So dung la 296,4"},
    {"anchor": "drivers[0].reading", "selected_text": "Cashout P2P", "comment": "Sai, la cashin"},
])

def run(path):
    return subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)

def test_groups_by_section_and_embeds_selected_text():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        f.write(COMMENTS); path = f.name
    out = json.loads(run(path).stdout)
    secs = {o["section"]: o for o in out}
    assert set(secs) == {"f0.aum", "drivers[0]"}          # two comments on f0.aum grouped
    aum = secs["f0.aum"]
    assert sorted(aum["anchors"]) == ["f0.aum.takeaway", "f0.aum.total"]
    assert "Doi: nhan manh rut som" in aum["feedback"]
    assert "So dung la 296,4" in aum["feedback"]
    assert "Muc giam" in aum["feedback"]                  # selected_text embedded for context
