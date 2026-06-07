import subprocess, sys, os, tempfile, textwrap

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "generate_worksheet.py")

SAMPLE_HTML = textwrap.dedent('''\
    <div class="scqr">
      <span data-bind="scqr.situation">Boi canh ngay bao cao.</span>
      <span data-bind="scqr.resolution">Ket luan mot cau.</span>
    </div>
    <div class="sechead"><h2>Chi so Bac Dau</h2></div>
    <div class="block">
      <div class="lb" data-bind="f0.aum.total">11.493,8</div>
      <p class="lt" data-bind="f0.aum.takeaway">Muc giam nam trong bien dao dong.</p>
      <span data-bind="f0.aum.z">-1,1</span>
    </div>
    <div class="sechead"><h2>Driver families</h2></div>
    <div class="drv">
      <span data-bind="drivers[0].reading">Cashout P2P vuot ky vong.</span>
      <span data-bind="drivers[0].delta">-12,3</span>
    </div>
''')

def run(args, stdin=None):
    return subprocess.run([sys.executable, SCRIPT] + args, input=stdin,
                          capture_output=True, text=True)

def test_emits_one_block_per_section_with_anchor_and_feedback_field():
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(SAMPLE_HTML); path = f.name
    out = run([path]).stdout
    assert "PHAN 1 - scqr" in out
    assert "[anchor: scqr]" in out
    assert "PHAN 2 - Chi so Bac Dau" in out
    assert "[anchor: f0.aum]" in out
    assert "PHAN 3 - Driver families" in out
    assert "[anchor: drivers[0]]" in out
    # current insight text surfaced
    assert "Muc giam nam trong bien dao dong." in out
    # an empty feedback field per section (line ends right after the label)
    assert out.count("SUA DOI / FEEDBACK:") == 3
    # numbers surfaced as key=value
    assert "total=11.493,8" in out

def test_section_before_h2_uses_prefix_not_mo_dau():
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(SAMPLE_HTML); path = f.name
    out = run([path]).stdout
    assert "Mo dau" not in out
    assert "PHAN 1 - scqr" in out
