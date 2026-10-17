// Theme and TV-mode toggles. In the real app the choice is stored on the account (PATCH /api/v1/me)
// and rendered by the server into <html data-theme data-ui>, so there is no flash and no inline script.
// Here it only uses localStorage so the prototype works from static files.
const root = document.documentElement;
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};

export function initPrefs() {
  for (const k of ["theme", "ui"]) {
    const v = store.get("spakr-" + k);
    if (v) root.dataset[k] = v;
  }
  const dark = () => root.dataset.theme === "dark" ||
    (!root.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
  const theme = document.querySelector("[data-toggle-theme]");
  theme?.addEventListener("click", () => {
    root.dataset.theme = dark() ? "light" : "dark";
    store.set("spakr-theme", root.dataset.theme);
    theme.setAttribute("aria-pressed", String(dark()));
  });
  theme?.setAttribute("aria-pressed", String(dark()));
  const tv = document.querySelector("[data-toggle-tv]");
  tv?.addEventListener("click", () => {
    root.dataset.ui = root.dataset.ui === "tv" ? "desktop" : "tv";
    store.set("spakr-ui", root.dataset.ui);
    tv.setAttribute("aria-pressed", String(root.dataset.ui === "tv"));
  });
  tv?.setAttribute("aria-pressed", String(root.dataset.ui === "tv"));
}
