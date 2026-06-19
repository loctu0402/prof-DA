/**
 * deck-stage — custom element for HTML slide decks.
 *
 * Features:
 *   - Keyboard navigation: Arrow keys, PageUp/Down, Space, Home, End,
 *     number keys (jump), R (reset to slide 1).
 *   - Touch navigation: tap left / right half of stage to go prev / next;
 *     taps on interactive slide content (links, buttons, inputs) pass through.
 *   - Auto-scaling: fixed design canvas (default 1920x1080) scaled via
 *     CSS transform to fill the viewport, letterboxed.
 *   - Slide counter + on-screen controls overlay (fades after idle).
 *   - Thumbnail rail: left-hand column of scaled slide previews; click to
 *     navigate. Hidden in noscale mode (PPTX export) and on narrow viewports.
 *   - Print / PDF: one slide per page at design size (via @media print).
 *   - Speaker notes: read from <script type="application/json" id="speaker-notes">
 *     (array indexed by slide); posted to parent via postMessage on navigation.
 *   - noscale attribute: disables transform scaling so the PPTX exporter
 *     captures unscaled geometry.
 *
 * Usage:
 *   <style>deck-stage:not(:defined){visibility:hidden}</style>
 *   <deck-stage width="1920" height="1080">
 *     <section data-label="Title">...</section>
 *     <section data-label="Agenda">...</section>
 *   </deck-stage>
 *   <script src="deck-stage.js"></script>
 *
 * Each slide section receives:
 *   data-deck-slide="N"   (0-based index)
 *   data-screen-label="NN Label"
 *   data-deck-active      (present only on the currently visible slide)
 *
 * Entrance animations must gate on [data-deck-active] and the motion query
 * so print and reduced-motion always show the finished slide state.
 *
 * slidechange CustomEvent fires on the element on every navigation:
 *   e.detail.index, e.detail.previousIndex, e.detail.total, e.detail.slide, e.detail.reason
 */

(() => {
  const DESIGN_W = 1920;
  const DESIGN_H = 1080;
  const OVERLAY_HIDE_MS = 1800;
  const NARROW_MQ = matchMedia('(max-width: 640px)');

  // Elements that should absorb a tap rather than triggering slide navigation.
  const INTERACTIVE_SEL = 'a[href], button, input, select, textarea, summary, label, [role="button"], [onclick], [tabindex]:not([tabindex^="-"]), [contenteditable]:not([contenteditable="false" i])';

  const pad2 = (n) => String(n).padStart(2, '0');

  const getLabel = (el) => {
    const explicit = el.getAttribute('data-label');
    if (explicit) return explicit;
    const h = el.querySelector('h1, h2, h3, [data-title]');
    const t = h && (h.textContent || '').trim().slice(0, 40);
    return t || 'Slide';
  };

  // Shadow DOM stylesheet — chrome only; slide content styles live in the page.
  const shadowCss = `
    :host {
      position: fixed; inset: 0; display: block;
      background: #000; color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      overflow: hidden; -webkit-tap-highlight-color: transparent;
    }
    :host([data-fonts-pending]) .stage,
    :host([data-fonts-pending]) .rail { opacity: 0; pointer-events: none; }

    .stage {
      position: absolute; inset: 0;
      display: flex; align-items: center; justify-content: center;
    }
    .canvas {
      position: relative; transform-origin: center center;
      flex-shrink: 0; background: #fff; will-change: transform;
    }

    ::slotted(*) {
      position: absolute !important; inset: 0 !important;
      width: 100% !important; height: 100% !important;
      box-sizing: border-box !important; overflow: hidden;
      opacity: 0; pointer-events: none; visibility: hidden;
    }
    ::slotted([data-deck-active]) {
      opacity: 1; pointer-events: auto; visibility: visible;
    }

    /* Slide counter + nav overlay */
    .overlay {
      position: fixed; left: 50%; bottom: 22px;
      transform: translate(-50%, 6px) scale(0.92);
      filter: blur(6px);
      display: flex; align-items: center; gap: 4px;
      padding: 4px; background: #000; color: #fff;
      border-radius: 999px; font-size: 12px;
      font-feature-settings: "tnum" 1; letter-spacing: 0.01em;
      opacity: 0; pointer-events: none;
      transition: opacity 260ms ease, transform 260ms cubic-bezier(.2,.8,.2,1), filter 260ms ease;
      transform-origin: center bottom; z-index: 2147483000; user-select: none;
    }
    .overlay[data-visible] {
      opacity: 1; pointer-events: auto;
      transform: translate(-50%, 0) scale(1); filter: blur(0);
    }

    .btn {
      appearance: none; -webkit-appearance: none;
      background: transparent; border: 0; margin: 0; padding: 0;
      color: rgba(255,255,255,0.72); font: inherit; cursor: default;
      display: inline-flex; align-items: center; justify-content: center;
      height: 28px; min-width: 28px; border-radius: 999px;
      transition: background 140ms ease, color 140ms ease;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:hover { background: rgba(255,255,255,0.12); color: #fff; }
    .btn:active { background: rgba(255,255,255,0.18); }
    .btn:focus { outline: none; }
    .btn svg { width: 14px; height: 14px; display: block; }
    .btn.reset {
      font-size: 11px; font-weight: 500; letter-spacing: 0.02em;
      padding: 0 10px 0 12px; gap: 6px;
    }
    .btn.reset .kbd {
      display: inline-flex; align-items: center; justify-content: center;
      min-width: 16px; height: 16px; padding: 0 4px;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      font-size: 10px; line-height: 1;
      color: rgba(255,255,255,0.88); background: rgba(255,255,255,0.12);
      border-radius: 4px;
    }
    .count {
      font-variant-numeric: tabular-nums; color: #fff; font-weight: 500;
      padding: 0 8px; min-width: 42px; text-align: center; font-size: 12px;
    }
    .count .sep { color: rgba(255,255,255,0.45); margin: 0 3px; font-weight: 400; }
    .count .total { color: rgba(255,255,255,0.55); }
    .divider { width: 1px; height: 14px; background: rgba(255,255,255,0.18); margin: 0 2px; }

    /* Thumbnail rail */
    .rail {
      position: fixed; left: 0; top: 0; bottom: 0;
      width: var(--deck-rail-w, 180px);
      background: #141414; border-right: 1px solid rgba(255,255,255,0.08);
      overflow-y: auto; overflow-x: hidden; padding: 12px 10px;
      box-sizing: border-box; display: flex; flex-direction: column; gap: 12px;
      z-index: 2147482500; scrollbar-width: thin;
      scrollbar-color: rgba(255,255,255,0.18) transparent;
    }
    .rail::-webkit-scrollbar { width: 8px; }
    .rail::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.18); border-radius: 4px;
      border: 2px solid transparent; background-clip: content-box;
    }
    :host([no-rail]) .rail,
    :host([noscale]) .rail { display: none; }
    @media (max-width: 640px) { .rail { display: none; } }

    .thumb {
      display: flex; align-items: flex-start; gap: 8px;
      cursor: pointer; user-select: none;
    }
    .thumb .num {
      width: 16px; flex-shrink: 0; font-size: 11px; font-weight: 500;
      text-align: right; color: rgba(255,255,255,0.55); padding-top: 2px;
      font-variant-numeric: tabular-nums;
    }
    .thumb .frame {
      flex: 1; min-width: 0; aspect-ratio: var(--deck-aspect, 16/9);
      background: #fff; border-radius: 4px;
      outline: 2px solid transparent; outline-offset: 0; overflow: hidden;
      transition: outline-color 120ms ease;
    }
    .thumb:hover .frame { outline-color: rgba(255,255,255,0.25); }
    .thumb[data-current] .num { color: #fff; }
    .thumb[data-current] .frame { outline-color: rgba(255,255,255,0.7); }
    .thumb .frame .inner {
      transform-origin: top left; pointer-events: none;
    }

    /* Print: one slide per page */
    @media print {
      :host { position: static; inset: auto; background: none; overflow: visible; color: inherit; }
      .stage { position: static; display: block; }
      .canvas { transform: none !important; width: auto !important; height: auto !important; background: none; will-change: auto; }
      ::slotted(*) {
        position: relative !important; inset: auto !important;
        width: var(--deck-design-w) !important; height: var(--deck-design-h) !important;
        opacity: 1 !important; visibility: visible !important; pointer-events: auto;
        break-after: page; page-break-after: always; break-inside: avoid; overflow: hidden;
      }
      ::slotted([data-deck-last-visible]) { break-after: auto; page-break-after: auto; }
      .overlay, .rail { display: none !important; }
    }
  `;

  class DeckStage extends HTMLElement {
    static get observedAttributes() { return ['width', 'height', 'noscale', 'no-rail']; }

    constructor() {
      super();
      this._root = this.attachShadow({ mode: 'open' });
      this._index = 0;
      this._slides = [];
      this._notes = [];
      this._hideTimer = null;

      this._onKey = this._onKey.bind(this);
      this._onResize = this._onResize.bind(this);
      this._onSlotChange = this._onSlotChange.bind(this);
      this._onMouseMove = this._onMouseMove.bind(this);
      this._onTap = this._onTap.bind(this);
    }

    get designWidth() { return parseInt(this.getAttribute('width'), 10) || DESIGN_W; }
    get designHeight() { return parseInt(this.getAttribute('height'), 10) || DESIGN_H; }

    connectedCallback() {
      this._render();
      this._loadNotes();
      this._syncPrintPageRule();
      window.addEventListener('keydown', this._onKey);
      window.addEventListener('resize', this._onResize);
      window.addEventListener('mousemove', this._onMouseMove, { passive: true });
      this.addEventListener('click', this._onTap);

      this._onBeforePrint = () => {
        const freeze = document.createElement('style');
        freeze.id = 'deck-print-freeze';
        freeze.textContent = '*,*::before,*::after{transition-duration:0s !important}';
        document.head.appendChild(freeze);
        this._slides.forEach((s) => s.setAttribute('data-deck-active', ''));
      };
      this._onAfterPrint = () => {
        const f = document.getElementById('deck-print-freeze');
        if (f) f.remove();
        this._applyIndex({ showOverlay: false, broadcast: false });
      };
      window.addEventListener('beforeprint', this._onBeforePrint);
      window.addEventListener('afterprint', this._onAfterPrint);

      // Hold stage until fonts are ready.
      this.setAttribute('data-fonts-pending', '');
      const reveal = () => this.removeAttribute('data-fonts-pending');
      requestAnimationFrame(() => {
        Promise.race([
          document.fonts ? document.fonts.ready : Promise.resolve(),
          new Promise((r) => setTimeout(r, 2000)),
        ]).then(reveal, reveal);
      });
    }

    disconnectedCallback() {
      window.removeEventListener('keydown', this._onKey);
      window.removeEventListener('resize', this._onResize);
      window.removeEventListener('mousemove', this._onMouseMove);
      window.removeEventListener('beforeprint', this._onBeforePrint);
      window.removeEventListener('afterprint', this._onAfterPrint);
      this.removeEventListener('click', this._onTap);
      if (this._hideTimer) clearTimeout(this._hideTimer);
    }

    attributeChangedCallback() {
      if (!this._canvas) return;
      this._canvas.style.width = this.designWidth + 'px';
      this._canvas.style.height = this.designHeight + 'px';
      this._canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
      this._canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
      if (this._rail) {
        this._rail.style.setProperty('--deck-aspect', this.designWidth + '/' + this.designHeight);
      }
      this._fit();
      this._syncPrintPageRule();
    }

    _render() {
      const style = document.createElement('style');
      style.textContent = shadowCss;

      const stage = document.createElement('div');
      stage.className = 'stage';

      const canvas = document.createElement('div');
      canvas.className = 'canvas';
      canvas.style.width = this.designWidth + 'px';
      canvas.style.height = this.designHeight + 'px';
      canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
      canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');

      const slot = document.createElement('slot');
      slot.addEventListener('slotchange', this._onSlotChange);
      canvas.appendChild(slot);
      stage.appendChild(canvas);

      const overlay = document.createElement('div');
      overlay.className = 'overlay';
      overlay.setAttribute('role', 'toolbar');
      overlay.setAttribute('aria-label', 'Deck controls');
      overlay.innerHTML = `
        <button class="btn prev" type="button" aria-label="Previous slide" title="Previous (Left arrow)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>
        </button>
        <span class="count" aria-live="polite">
          <span class="current">1</span><span class="sep">/</span><span class="total">1</span>
        </span>
        <button class="btn next" type="button" aria-label="Next slide" title="Next (Right arrow)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
        </button>
        <span class="divider"></span>
        <button class="btn reset" type="button" aria-label="Reset to first slide" title="Reset (R)">
          Reset<span class="kbd">R</span>
        </button>
      `;
      overlay.querySelector('.prev').addEventListener('click', () => this._advance(-1, 'click'));
      overlay.querySelector('.next').addEventListener('click', () => this._advance(1, 'click'));
      overlay.querySelector('.reset').addEventListener('click', () => this.goTo(0, 'click'));

      const rail = document.createElement('div');
      rail.className = 'rail';
      rail.style.setProperty('--deck-aspect', this.designWidth + '/' + this.designHeight);

      this._root.append(style, rail, stage, overlay);
      this._canvas = canvas;
      this._stage = stage;
      this._slot = slot;
      this._overlay = overlay;
      this._rail = rail;
      this._countEl = overlay.querySelector('.current');
      this._totalEl = overlay.querySelector('.total');
    }

    _syncPrintPageRule() {
      const id = 'deck-stage-print-page';
      let tag = document.getElementById(id);
      if (!tag) { tag = document.createElement('style'); tag.id = id; document.head.appendChild(tag); }
      tag.textContent =
        '@page { size: ' + this.designWidth + 'px ' + this.designHeight + 'px; margin: 0; } ' +
        '@media print { html, body { margin: 0 !important; padding: 0 !important; background: none !important; overflow: visible !important; } ' +
        '* { -webkit-print-color-adjust: exact; print-color-adjust: exact; } ' +
        '*, *::before, *::after { animation-delay: -99s !important; animation-duration: .001s !important; ' +
        'animation-fill-mode: both !important; transition-duration: 0s !important; } }';
    }

    _onSlotChange() {
      this._collectSlides();
      this._applyIndex({ showOverlay: false, broadcast: true, reason: 'init' });
      this._fit();
    }

    _collectSlides() {
      const assigned = this._slot.assignedElements({ flatten: true });
      this._slides = assigned.filter((el) => {
        const t = el.tagName;
        return t !== 'TEMPLATE' && t !== 'SCRIPT' && t !== 'STYLE';
      });
      this._slides.forEach((s, i) => {
        s.setAttribute('data-deck-slide', String(i));
        s.setAttribute('data-screen-label', `${pad2(i + 1)} ${getLabel(s)}`);
      });
      // Mark last visible for print break handling.
      let last = null;
      this._slides.forEach((s) => { s.removeAttribute('data-deck-last-visible'); last = s; });
      if (last) last.setAttribute('data-deck-last-visible', '');

      if (this._totalEl) this._totalEl.textContent = String(this._slides.length || 1);
      if (this._index >= this._slides.length) this._index = Math.max(0, this._slides.length - 1);
      this._renderRail();
    }

    _loadNotes() {
      const tag = document.getElementById('speaker-notes');
      if (!tag) { this._notes = []; return; }
      try {
        const parsed = JSON.parse(tag.textContent || '[]');
        this._notes = Array.isArray(parsed) ? parsed : [];
      } catch (e) {
        console.warn('[deck-stage] Could not parse #speaker-notes JSON:', e);
        this._notes = [];
      }
    }

    _applyIndex({ showOverlay = true, broadcast = true, reason = 'init' } = {}) {
      if (!this._slides.length) return;
      const curr = this._index;
      try { history.replaceState(null, '', '#' + (curr + 1)); } catch (e) {}
      this._slides.forEach((s, i) => {
        if (i === curr) s.setAttribute('data-deck-active', '');
        else s.removeAttribute('data-deck-active');
      });
      if (this._countEl) this._countEl.textContent = String(curr + 1);
      this._syncRailCurrent();
      if (broadcast) {
        try { window.postMessage({ slideIndexChanged: curr, deckTotal: this._slides.length }, '*'); } catch (e) {}
        this.dispatchEvent(new CustomEvent('slidechange', {
          bubbles: true, composed: true,
          detail: { index: curr, total: this._slides.length, slide: this._slides[curr] || null, reason },
        }));
      }
      if (showOverlay) this._flashOverlay();
    }

    // Public API used by PPTX exporter: deck.goTo(N)
    goTo(n, reason = 'api') {
      if (!this._slides.length) return;
      this._index = Math.max(0, Math.min(this._slides.length - 1, n));
      this._applyIndex({ reason });
    }

    _advance(delta, reason = 'keyboard') {
      const n = this._index + delta;
      if (n < 0 || n >= this._slides.length) return;
      this._index = n;
      this._applyIndex({ reason });
    }

    _onKey(e) {
      // Number keys 1-9: jump to that slide index.
      if (e.key >= '1' && e.key <= '9' && !e.metaKey && !e.ctrlKey && !e.altKey) {
        const n = parseInt(e.key, 10) - 1;
        if (n < this._slides.length) { this.goTo(n, 'keyboard'); e.preventDefault(); }
        return;
      }
      const map = {
        ArrowRight: 1, ArrowDown: 1, PageDown: 1, ' ': 1,
        ArrowLeft: -1, ArrowUp: -1, PageUp: -1,
      };
      if (e.key in map && !e.metaKey && !e.ctrlKey) {
        this._advance(map[e.key], 'keyboard');
        e.preventDefault();
      } else if (e.key === 'Home') {
        this.goTo(0, 'keyboard'); e.preventDefault();
      } else if (e.key === 'End') {
        this.goTo(this._slides.length - 1, 'keyboard'); e.preventDefault();
      } else if ((e.key === 'r' || e.key === 'R') && !e.metaKey && !e.ctrlKey) {
        this.goTo(0, 'keyboard'); e.preventDefault();
      }
    }

    _onTap(e) {
      // Tapping interactive content inside a slide must not trigger navigation.
      if (e.target && e.target.closest && e.target.closest(INTERACTIVE_SEL)) return;
      // Taps on the overlay buttons are handled by their own listeners.
      if (this._overlay && this._overlay.contains(e.target)) return;
      const rect = this.getBoundingClientRect();
      const mid = rect.left + rect.width / 2;
      this._advance(e.clientX < mid ? -1 : 1, 'tap');
    }

    _onMouseMove() { this._flashOverlay(); }

    _flashOverlay() {
      if (!this._overlay) return;
      this._overlay.setAttribute('data-visible', '');
      if (this._hideTimer) clearTimeout(this._hideTimer);
      this._hideTimer = setTimeout(() => {
        this._overlay.removeAttribute('data-visible');
      }, OVERLAY_HIDE_MS);
    }

    _fit() {
      if (!this._canvas) return;
      if (this.hasAttribute('noscale')) {
        this._canvas.style.transform = 'none';
        if (this._stage) this._stage.style.left = '0';
        return;
      }
      const rw = (!this.hasAttribute('no-rail') && !NARROW_MQ.matches) ? (this._railPx || 0) : 0;
      if (this._stage) this._stage.style.left = rw + 'px';
      const vw = window.innerWidth - rw;
      const vh = window.innerHeight;
      const s = Math.min(vw / this.designWidth, vh / this.designHeight);
      this._canvas.style.transform = `scale(${s})`;
    }

    _onResize() { this._fit(); this._renderRail(); }

    _renderRail() {
      if (!this._rail || this.hasAttribute('noscale') || NARROW_MQ.matches) return;
      this._rail.innerHTML = '';
      const aspect = this.designWidth / this.designHeight;
      const thumbW = (this._railPx || 180) - 36;
      const thumbH = Math.round(thumbW / aspect);
      const slideScale = thumbW / this.designWidth;

      this._slides.forEach((slide, i) => {
        const thumb = document.createElement('div');
        thumb.className = 'thumb';
        if (i === this._index) thumb.setAttribute('data-current', '');
        thumb.setAttribute('tabindex', '0');
        thumb.setAttribute('role', 'button');
        thumb.setAttribute('aria-label', `Slide ${i + 1}`);

        const num = document.createElement('span');
        num.className = 'num';
        num.textContent = String(i + 1);

        const frame = document.createElement('div');
        frame.className = 'frame';
        frame.style.width = thumbW + 'px';
        frame.style.height = thumbH + 'px';

        // Shallow clone of the slide scaled down for the thumbnail.
        const inner = slide.cloneNode(true);
        inner.className = 'inner';
        inner.removeAttribute('data-deck-active');
        inner.removeAttribute('data-deck-skip');
        inner.style.cssText = [
          'position:absolute', 'top:0', 'left:0',
          `width:${this.designWidth}px`, `height:${this.designHeight}px`,
          `transform:scale(${slideScale})`, 'transform-origin:top left',
          'pointer-events:none', 'opacity:1', 'visibility:visible',
        ].join(';');
        frame.appendChild(inner);
        thumb.append(num, frame);

        thumb.addEventListener('click', () => this.goTo(i, 'click'));
        thumb.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') { this.goTo(i, 'keyboard'); e.preventDefault(); }
        });
        this._rail.appendChild(thumb);
      });

      this._railPx = this._railPx || 180;
    }

    _syncRailCurrent() {
      if (!this._rail) return;
      this._rail.querySelectorAll('.thumb').forEach((t, i) => {
        if (i === this._index) t.setAttribute('data-current', '');
        else t.removeAttribute('data-current');
      });
    }
  }

  customElements.define('deck-stage', DeckStage);
})();
