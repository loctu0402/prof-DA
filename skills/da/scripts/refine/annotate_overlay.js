(function () {
  const comments = [];
  function anchorFor(node) {
    let el = node.nodeType === 3 ? node.parentElement : node;
    while (el && el !== document.body) {
      if (el.dataset && (el.dataset.anchor || el.dataset.bind)) return el.dataset.anchor || el.dataset.bind;
      el = el.parentElement;
    }
    return "(unknown)";
  }
  let btn, pop;
  function hide(el){ if(el) el.style.display="none"; }
  document.addEventListener("mouseup", (e) => {
    if (btn && e.target === btn) return;
    const sel = window.getSelection();
    const text = sel && sel.toString().trim();
    if (!text) { hide(btn); return; }
    if (!btn) {
      btn = document.createElement("button");
      btn.textContent = "Them gop y";
      btn.style.cssText = "position:absolute;z-index:99999;font:12px sans-serif;padding:3px 8px;background:#d82d8b;color:#fff;border:0;border-radius:4px;cursor:pointer";
      document.body.appendChild(btn);
    }
    const r = sel.getRangeAt(0).getBoundingClientRect();
    btn.style.left = (window.scrollX + r.left) + "px";
    btn.style.top = (window.scrollY + r.bottom + 4) + "px";
    btn.style.display = "block";
    const anchor = anchorFor(sel.anchorNode);
    btn.onclick = () => { hide(btn); openPopup(anchor, text, r); };
  });
  function openPopup(anchor, text, r) {
    if (pop) pop.remove();
    pop = document.createElement("div");
    pop.style.cssText = "position:absolute;z-index:99999;background:#fff;border:1px solid #d6cdb9;border-radius:8px;padding:10px;box-shadow:0 2px 10px rgba(0,0,0,.15);width:280px;font:12px sans-serif";
    pop.innerHTML = '<div style="font-size:10px;color:#7a7264;margin-bottom:4px">['+anchor+']</div>'
      + '<textarea style="width:100%;height:60px;box-sizing:border-box"></textarea>'
      + '<div style="margin-top:6px;text-align:right"><button data-x="c">Huy</button> <button data-x="s" style="background:#d82d8b;color:#fff;border:0;padding:3px 10px;border-radius:4px">Luu</button></div>';
    pop.style.left = (window.scrollX + r.left) + "px";
    pop.style.top = (window.scrollY + r.bottom + 8) + "px";
    document.body.appendChild(pop);
    const ta = pop.querySelector("textarea"); ta.focus();
    pop.querySelector('[data-x="c"]').onclick = () => pop.remove();
    document.addEventListener("keydown", function esc(ev){ if(ev.key==="Escape"){ pop&&pop.remove(); document.removeEventListener("keydown",esc);} });
    pop.querySelector('[data-x="s"]').onclick = () => {
      const c = ta.value.trim();
      if (c) { comments.push({ anchor, selected_text: text, comment: c }); refreshExport(); }
      pop.remove();
    };
  }
  let exp, out;
  function refreshExport() {
    if (!exp) {
      exp = document.createElement("button");
      exp.style.cssText = "position:fixed;z-index:99999;right:16px;bottom:16px;background:#161412;color:#fff;border:0;padding:8px 14px;border-radius:6px;font:12px sans-serif;cursor:pointer";
      document.body.appendChild(exp);
      out = document.createElement("textarea");
      out.id = "comments-out";
      out.style.cssText = "position:fixed;z-index:99999;right:16px;bottom:56px;width:280px;height:80px;display:none";
      document.body.appendChild(out);
      exp.onclick = () => {
        const json = JSON.stringify(comments, null, 2);
        out.value = json; out.style.display = "block";
        const a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([json], {type:"application/json"}));
        a.download = "comments.json"; a.click();
      };
    }
    exp.textContent = "Export gop y (" + comments.length + ")";
  }
  refreshExport();
})();
