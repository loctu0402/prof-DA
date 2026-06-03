import subprocess, sys, os, tempfile, textwrap, json

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "parse_feedback.py")

FILLED = textwrap.dedent('''\
    === prof-DA REVIEW WORKSHEET ===
    Do NOT edit the [anchor: ...] line.

    ------------------------------------------------------------
    PHAN 1 - Chi so Bac Dau
    [anchor: f0.aum]
    - Noi dung hien tai: Muc giam nam trong bien dao dong.
    - So lieu: total=11.493,8 | z=-1,1
    - SUA DOI / FEEDBACK: Doi takeaway: nhan manh rut som tang manh.

    ------------------------------------------------------------
    PHAN 2 - Driver families
    [anchor: drivers[0]]
    - Noi dung hien tai: Cashout P2P vuot ky vong.
    - So lieu: delta=-12,3
    - SUA DOI / FEEDBACK:
''')

def run(path):
    return subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)

def test_only_filled_sections_returned_with_anchors_and_text():
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(FILLED); path = f.name
    out = json.loads(run(path).stdout)
    assert len(out) == 1                       # PHAN 2 had empty feedback -> excluded
    item = out[0]
    assert item["section"] == "f0.aum"
    assert item["title"] == "Chi so Bac Dau"
    assert item["feedback"] == "Doi takeaway: nhan manh rut som tang manh."
    assert item["anchors"] == ["f0.aum.total", "f0.aum.z"] or item["anchors"] == ["f0.aum"]
