import subprocess, sys, os, tempfile

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "wrap_annotation_harness.py")

def test_injects_overlay_before_body_close_and_writes_annotate_file():
    html = "<html><body><p data-bind='f0.aum.takeaway'>x</p></body></html>"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); path = f.name
    outp = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True).stdout.strip()
    assert outp.endswith(".annotate.html") and os.path.exists(outp)
    body = open(outp, encoding="utf-8").read()
    assert "Export gop y" in body and "comments-out" in body         # overlay present
    assert body.index("<script>") < body.lower().index("</body>")    # injected before </body>
