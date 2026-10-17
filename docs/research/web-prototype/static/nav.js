// Small enhancements, each independent and optional (pages work without them):
//  - lightbox on a native <dialog>
//  - roving-tabindex tab list for the editor (Write / Preview)
//  - spatial (arrow key) navigation for TV remotes, active in TV mode only
export function initLightbox() {
  const dlg = document.querySelector("dialog.lightbox");
  if (!dlg) return;
  const img = dlg.querySelector("img");
  const cap = dlg.querySelector("p");
  for (const t of document.querySelectorAll("[data-lightbox]")) {
    t.addEventListener("click", () => {
      const src = t.querySelector("img");
      img.src = t.dataset.lightbox; img.alt = src.alt; cap.textContent = t.dataset.caption || "";
      dlg.showModal();                        // focus moves in; Esc closes; focus returns to the trigger
    });
  }
  dlg.querySelector("[data-close]").addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
}

export function initTabs() {
  const list = document.querySelector('[role="tablist"]');
  if (!list) return;
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  const show = (tab) => {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    }
  };
  tabs.forEach((t) => t.addEventListener("click", () => show(t)));
  list.addEventListener("keydown", (e) => {
    const i = tabs.indexOf(document.activeElement);
    const next = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
    if (next === undefined) return;
    e.preventDefault();
    const t = tabs[(next + tabs.length) % tabs.length];
    t.focus(); show(t);
  });
}

// Arrow-key focus movement by geometry. Browsers do not ship CSS spatial navigation, so this is
// ~25 lines of our own, used only when the page is in TV mode; Tab/Enter keep working as normal.
export function initSpatialNav() {
  const sel = 'a[href], button:not([disabled]), input, textarea, select, [tabindex="0"]';
  addEventListener("keydown", (e) => {
    if (document.documentElement.dataset.ui !== "tv") return;
    const dir = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0] }[e.key];
    if (!dir || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName)) return;
    const cur = document.activeElement?.getBoundingClientRect();
    if (!cur || document.activeElement === document.body) return;
    const cx = cur.left + cur.width / 2, cy = cur.top + cur.height / 2;
    let best = null, bestScore = Infinity;
    for (const el of document.querySelectorAll(sel)) {
      if (el === document.activeElement || el.offsetParent === null) continue;
      const r = el.getBoundingClientRect();
      const dx = r.left + r.width / 2 - cx, dy = r.top + r.height / 2 - cy;
      const along = dx * dir[0] + dy * dir[1], across = Math.abs(dx * dir[1]) + Math.abs(dy * dir[0]);
      if (along <= 0) continue;                       // must lie in the pressed direction
      const score = along + across * 2;               // prefer elements in line with the current one
      if (score < bestScore) { best = el; bestScore = score; }
    }
    if (best) { e.preventDefault(); best.focus({ preventScroll: false }); best.scrollIntoView({ block: "nearest", inline: "nearest" }); }
  });
}
