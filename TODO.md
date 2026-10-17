# TODO

Current version: **0.0.0** (see [`VERSION`](VERSION) and [`scripts/version.sh`](scripts/version.sh)). Versions are `MAJOR.MINOR.BUILD`; BUILD counts up with every push to `main`, MINOR and MAJOR are planned and set by hand.

Items are numbered `[CAT].[NUMBER]`, for example `API.1`. Each item shows its phase in square brackets (the MINOR version that delivers it) and `needs:` the ids it depends on, so the list forms a tree rooted in phase 0.0 research and the foundation. Phases 0.1 to 0.8 are building blocks; **0.9 is the pre-release working version**; 1.0 is the release. See the [phase plan](docs/plan/tiers.html) and the [dependency tree](docs/plan/tree.html).

**Standing requirement (integrity):** every stored artifact has a checksum and is classed as source of truth or rebuildable, with parity data and a tested recovery path (INT category).

**Standing requirement:** every UI item is responsive and works in light and dark mode from the start (UI.11 to UI.13 are the base; UI.13 is the checklist all later UI items meet).

Each category is a GitHub issue holding the same checklist (ids, titles, phases). Bugs and suggestions arrive as their own issues and are folded in here when accepted. Numbers are never reused; new items are appended. This file is kept by the TODO thread and is the source of truth: change it and the matching issue together.


## REL: Release, versioning and process

Issue: [#8](https://github.com/dwhagar/spakr/issues/8)

- [x] **REL.1** Version file and build-number script (scripts/version.sh) [0.0]
- [x] **REL.2** TODO.md, CHANGELOG.md and category issues created and linked [0.0]
- [x] **REL.3** Issue templates for bugs and suggestions [0.0]
- [ ] **REL.4** Script to check TODO.md against GitHub issues (scripts/todo-sync) [0.1] — needs: REL.2, FND.1
- [ ] **REL.5** Expose the version in the app: /api/v1/version, page footer, outbound User-Agent [0.1] — needs: REL.1, API.1, FND.4
- [ ] **REL.6** Release checklist and 1.0 tagging [0.9] — needs: OPS.7, DOC.3, TST.4

## DOC: Documentation

Issue: [#9](https://github.com/dwhagar/spakr/issues/9)

- [x] **DOC.1** Plan rewritten as tiers 0.0 to 0.9 with TODO ids [0.0]
- [ ] **DOC.2** Enable GitHub Pages from /docs (owner action in repository settings) [0.0]
- [ ] **DOC.3** Admin install and upgrade guide [0.9] — needs: FND.6, DB.2, QUE.2, OPS.5, CFG.1, BAK.27
- [ ] **DOC.4** Editor guide: writing pages, links, media syntax, visibility [0.9] — needs: UI.4, MED.7, LNK.1
- [ ] **DOC.5** API reference generated from the OpenAPI description [0.9] — needs: API.3
- [x] **DOC.6** Plan pages responsive with light and dark mode (style.css) [0.0]
- [ ] **DOC.7** Privacy page and notice (seeded text, admin-editable) linked from the footer [0.9] — needs: UI.9, AUTH.12
- [ ] **DOC.8** Media management guide: library, metadata, moderation, takedown, prune policy and the systemd timer [0.9] — needs: UI.23, MED.27

## FND: Foundation

Issue: [#10](https://github.com/dwhagar/spakr/issues/10)

- [x] **FND.1** Python package skeleton in src/ with pyproject and pinned dependencies [0.1] — needs: RES.15
- [x] **FND.2** JSON configuration loader: config.json (git-ignored) validated against examples/config.json.example [0.1] — needs: FND.1
- [ ] **FND.3** WSGI entry point (daemon mode, pass-authorization on) and the small CGI shim (health and maintenance only) [0.1] — needs: FND.1, API.1, RES.16
- [x] **FND.4** Shared outbound HTTP helper with the required User-Agent (software, version, API version) [0.1] — needs: FND.1
- [ ] **FND.5** Dev setup script for Ubuntu 24.04 [0.1] — needs: FND.1, RES.15
- [ ] **FND.6** Apache vhost and systemd unit examples in examples/ [0.1] — needs: FND.3, QUE.2, RES.16
- [ ] **FND.7** Lint, format and test tooling; tests workflow stays on the 07:00 UTC schedule only, and the daily run opens an issue when it fails [0.1] — needs: FND.1
- [ ] **FND.8** Structured logging [0.1] — needs: FND.1, FND.2
- [ ] **FND.9** Command-line tool (spakr): init-config, init-db, create-admin, reindex, load-sample, backup, restore, requeue-stuck, version [0.1] — needs: FND.2, DB.1
- [x] **FND.10** Python 3.12 required: `requires-python >=3.12` in pyproject and a clear startup error on older versions [0.1] — needs: FND.1
- [ ] **FND.11** Data directory `/data` (git-ignored): holds the articles (content repository) and the system's data (media, originals, uploads, cache) and nothing else; never config.json, examples or docs; created and checked at startup [0.1] — needs: FND.2, CFG.2
- [ ] **FND.12** Layout fix: config.json lives in the project root (search order: --config, SPAKR_CONFIG, ./config.json, /etc/spakr/config.json; drop the data-directory fallback), /data holds only articles and system data, examples/ and docs/ stay outside it; update the loader, paths, tests and docs [0.1] — needs: FND.2, FND.11

## API: API (Flask, /api/v1)

Issue: [#11](https://github.com/dwhagar/spakr/issues/11)

- [x] **API.1** Flask app factory and /api/v1 skeleton with health endpoint [0.1] — needs: FND.1, FND.2
- [ ] **API.2** Error format, pagination and filtering conventions [0.1] — needs: API.1
- [ ] **API.3** OpenAPI description kept in step with the routes [0.1] — needs: API.2, RES.14
- [ ] **API.4** Permission decorator used by every route (session or API key) [0.4] — needs: API.1, AUTH.2, AUTH.3
- [ ] **API.5** Generic CRUD helpers for page-backed resources [0.5] — needs: API.4, ENT.1, GIT.2
- [ ] **API.6** Request security context: trust HTTPS and client address from Apache (X-Forwarded-Proto) only from a configured trusted proxy; Secure and __Host- cookies; HSTS only when the admin enables it (TLS and certificates are Apache's job) [0.4] — needs: API.1, CFG.4, RND.4
- [x] **API.7** Integer API version: counts up with every API change, sent in a response header and kept in one place in the code [0.1] — needs: API.1
- [x] **API.8** Health and status endpoint reports the API version, the database schema version, the software version (MAJOR.MINOR.BUILD) and the configuration state [0.1] — needs: API.1, API.7, DB.5, REL.5

## DB: Database

Issue: [#12](https://github.com/dwhagar/spakr/issues/12)

- [x] **DB.1** SQLAlchemy engine and session setup [0.1] — needs: FND.2
- [ ] **DB.2** Alembic migrations creating the schema in docs/design/database.html [0.1] — needs: DB.1 — progress: migrations 0001 (foundation, accounts, roles, settings, audit) and 0002 (content core, relations) are in; still to add: api_key, invitation, password_reset, session, email_outbox, type tables, page_search, media, html_allowlist, upload_policy
- [ ] **DB.3** Command to rebuild all derived MySQL data (page index, search tables, relations) from the git content store; resumable, dry-run option [0.2] — needs: DB.2, GIT.5, SEARCH.2, INT.1, GIT.9
- [ ] **DB.4** Database restore into an empty schema with a schema-version check and integrity verification, used by `spakr restore` (the nightly dump is BAK.5) [0.1] — needs: DB.2, BAK.5
- [x] **DB.5** Integer database schema version: counts up with every schema change, stored in the database, bumped by each migration and checked at startup [0.1] — needs: DB.2

## QUE: Task queue

Issue: [#13](https://github.com/dwhagar/spakr/issues/13)

- [ ] **QUE.1** Redis connection and RQ configuration [0.1] — needs: FND.2
- [ ] **QUE.2** Worker process and systemd unit [0.1] — needs: QUE.1, FND.1
- [ ] **QUE.3** Task status API [0.7] — needs: QUE.1, API.4
- [ ] **QUE.4** Reindex and cache-warm jobs [0.7] — needs: QUE.2, DB.3

## GIT: Git-backed content store

Issue: [#14](https://github.com/dwhagar/spakr/issues/14)

- [ ] **GIT.1** Repository initialisation, commit author mapping and write locking [0.2] — needs: FND.1, DB.2, RES.4
- [ ] **GIT.2** Create, read and update a page (Markdown with front matter) [0.2] — needs: GIT.1
- [ ] **GIT.3** Page history and diff [0.2] — needs: GIT.2
- [ ] **GIT.4** Revert to an earlier revision [0.2] — needs: GIT.3
- [ ] **GIT.5** MySQL page index kept in step on every write [0.2] — needs: GIT.2, DB.2
- [ ] **GIT.6** Slug rules, rename and move [0.2] — needs: GIT.2
- [ ] **GIT.7** Edit conflict detection based on the base commit [0.2] — needs: GIT.2
- [ ] **GIT.9** Complete front matter: the page file carries everything about a page that is not derived (typed fields, tags, settings, visibility, aliases, relations), so the MySQL index can be rebuilt from git alone; page.content_sha256 records the file hash for INT.4 (RES.29) [0.2] — needs: GIT.2, RES.13, RES.29

## RND: Rendering and sanitising

Issue: [#15](https://github.com/dwhagar/spakr/issues/15)

- [ ] **RND.1** MultiMarkdown rendering [0.3] — needs: FND.1, RES.1
- [ ] **RND.2** LaTeX math rendered server-side to MathML with pure-Python latex2mathml (no Node): aligned rewrite, 2,000-character cap, output guard (unknown commands, href, javascript, exceptions) and escaped TeX-source fallback [0.3] — needs: RND.1, RES.2
- [ ] **RND.3** HTML sanitiser with the admin-approved allowlist [0.3] — needs: RND.1, RES.3
- [ ] **RND.4** Strict Content-Security-Policy and security headers (no inline script or style) [0.3] — needs: API.1, UI.1
- [ ] **RND.5** Rendered-page cache keyed by content (commit, render version, allowlist version) [0.3] — needs: RND.1, GIT.2, RES.25
- [ ] **RND.6** Preview endpoint [0.5] — needs: RND.1, RND.3, API.4
- [ ] **RND.7** Link-status pass after the render cache: red links for missing pages, links to GM-only pages unwrapped for viewers without the GM role [0.6] — needs: RND.5, LNK.1, VIS.2

## AUTH: Accounts, roles and API keys

Issue: [#16](https://github.com/dwhagar/spakr/issues/16)

- [ ] **AUTH.1** Users and password hashing [0.4] — needs: DB.2, RES.5
- [ ] **AUTH.2** Login, logout, cookie sessions and CSRF header [0.4] — needs: AUTH.1, API.1, API.6
- [ ] **AUTH.3** Roles and permissions: reader, editor, GM, mod, admin [0.4] — needs: AUTH.1, DB.2
- [ ] **AUTH.4** Invitation flow (7-day tokens) [0.4] — needs: AUTH.1, MAIL.2
- [ ] **AUTH.5** Password reset flow (1-hour tokens) [0.4] — needs: AUTH.1, MAIL.2
- [ ] **AUTH.6** API keys: users limited to their own permissions, admins unlimited, per-user cap; keys cannot create keys or change account security [0.4] — needs: AUTH.2, AUTH.3
- [ ] **AUTH.7** Audit log [0.4] — needs: DB.2
- [ ] **AUTH.8** Admin settings API: reads and writes every web-editable setting; never returns secret values [0.4] — needs: AUTH.3, API.4, CFG.4, CFG.5
- [ ] **AUTH.9** HTML allowlist approval API [0.4] — needs: AUTH.8, RND.3
- [ ] **AUTH.10** Account editing API (profile, email, password, roles) [0.4] — needs: AUTH.2, AUTH.3
- [ ] **AUTH.11** Bootstrap the first admin account from the command line [0.4] — needs: FND.9, AUTH.1, AUTH.3
- [ ] **AUTH.12** User data export: profile, contributions and audit entries about the account as JSON [0.4] — needs: AUTH.3, AUTH.10

## MAIL: Email

Issue: [#17](https://github.com/dwhagar/spakr/issues/17)

- [ ] **MAIL.1** SMTP sender through an external relay (host, port, TLS mode, username, password and sender address are all configuration) [0.4] — needs: FND.2, RES.6, CFG.2, CFG.5
- [ ] **MAIL.2** Invitation and password-reset templates, sent via the queue [0.4] — needs: MAIL.1, QUE.2, DB.2
- [ ] **MAIL.3** Email settings in the admin settings with a send-test-message action [0.4] — needs: MAIL.1, AUTH.8, CFG.4, MAIL.2

## VIS: Page visibility

Issue: [#18](https://github.com/dwhagar/spakr/issues/18)

- [ ] **VIS.1** Public or GM-only flag per page, with the reserved visibility-group column [0.4] — needs: DB.2, GIT.2, AUTH.3
- [ ] **VIS.2** One central query filter enforcing visibility everywhere [0.4] — needs: VIS.1, DB.1
- [ ] **VIS.3** Leak tests: views, search, links, backlinks, history and downloads [0.6] — needs: VIS.2, SEARCH.3, LNK.2, GIT.3

## ENT: Entity types

Issue: [#19](https://github.com/dwhagar/spakr/issues/19)

- [ ] **ENT.1** Entity type registry and structured field definitions [0.5] — needs: GIT.2, DB.2, RES.13
- [ ] **ENT.2** Characters [0.5] — needs: ENT.1
- [ ] **ENT.3** Items and technology [0.5] — needs: ENT.1
- [ ] **ENT.4** Places [0.5] — needs: ENT.1
- [ ] **ENT.5** Magic and psionics [0.5] — needs: ENT.1
- [ ] **ENT.6** Abilities [0.5] — needs: ENT.1
- [ ] **ENT.7** Skills [0.5] — needs: ENT.1
- [ ] **ENT.8** Entities (creatures and beings) [0.5] — needs: ENT.1
- [ ] **ENT.9** Races [0.5] — needs: ENT.1
- [ ] **ENT.10** Nation-states [0.5] — needs: ENT.1
- [ ] **ENT.11** Free pages [0.5] — needs: ENT.1
- [ ] **ENT.12** Settings as tags (high fantasy, modern/cosmic horror, scifi) [0.5] — needs: ENT.1
- [ ] **ENT.13** Per-type form schemas served by the API for the UI to render [0.5] — needs: ENT.1, API.5

## LNK: Links, relations and browsing

Issue: [#20](https://github.com/dwhagar/spakr/issues/20)

- [ ] **LNK.1** Wiki-style links between pages [0.6] — needs: RND.1, GIT.5
- [ ] **LNK.2** Backlinks [0.6] — needs: LNK.1
- [ ] **LNK.3** Relations between pages, using the fixed admin-managed relation_kind vocabulary (decided) [0.6] — needs: ENT.1, DB.2
- [ ] **LNK.4** Browse by type and setting [0.6] — needs: ENT.1, API.5
- [ ] **LNK.5** Tags [0.6] — needs: ENT.1
- [ ] **LNK.6** Admin API and screen for the relation_kind vocabulary (add, rename, retire, reorder; starter set seeded by migration) [0.6] — needs: LNK.3, AUTH.8
- [ ] **LNK.7** Recent changes feed [0.6] — needs: GIT.3, VIS.2

## SEARCH: Content search, SEO and caching

Issue: [#21](https://github.com/dwhagar/spakr/issues/21)

- [x] **SEARCH.1** Reconcile the page_search design in docs/design/database.html (type, summary, name/aliases, tags, settings, field text, indexes) [0.0]
- [ ] **SEARCH.2** Search document builder: plain text of the Markdown plus title, summary, aliases, tags, settings and type-field text (with split and joined token forms: 8d6 also d6, Mi-Go also migo), written on every page save [0.2] — needs: GIT.5, DB.2, SEARCH.1
- [ ] **SEARCH.3** Full-text query endpoint over the full page index: natural and boolean modes, relevance ranking, highlighted snippets, pagination [0.6] — needs: SEARCH.2, VIS.2, RES.7
- [ ] **SEARCH.4** Field search: type, setting, tag, name/title and type-specific fields (for example race, place, occupation) as API parameters and query syntax such as type:character setting:scifi tag:undead [0.6] — needs: SEARCH.3, ENT.1, LNK.5
- [ ] **SEARCH.5** Filters and facet counts by type, setting and tag [0.6] — needs: SEARCH.4
- [ ] **SEARCH.6** Visibility in search: GM-only pages excluded for users without the GM role, using the copied visibility column [0.6] — needs: SEARCH.3, VIS.2
- [ ] **SEARCH.7** Name and alias autocomplete for search-as-you-type and the link picker [0.6] — needs: SEARCH.2
- [ ] **SEARCH.8** MySQL FULLTEXT server settings as an install requirement (default parser, innodb_ft_min_token_size=2, stopwords off; they are server variables, not web settings): start-up check and admin screen warning; ngram only as an install-time choice [0.6] — needs: SEARCH.2, RES.7
- [ ] **SEARCH.9** SEO metadata, sitemap.xml and robots.txt [0.6] — needs: GIT.5, VIS.2, RES.8
- [ ] **SEARCH.10** Per-process memory (LRU) and disk caches for rendered pages, size cap, no Redis for it [0.6] — needs: RND.5, QUE.1, RES.25

## MED: Uploads and media management

Issue: [#22](https://github.com/dwhagar/spakr/issues/22)

- [ ] **MED.1** Upload endpoint: type sniffing, size limits (10 MB, 100 MB video), safe-list [0.7] — needs: API.4, RES.9
- [ ] **MED.2** Quarantine and admin override [0.7] — needs: MED.1
- [ ] **MED.3** Hashed media directories; originals kept privately [0.7] — needs: MED.1
- [ ] **MED.4** Image processing with ImageMagick as queue tasks: one process per upload writes the whole ladder under the spakr policy file (Pillow only to verify) [0.7] — needs: MED.3, QUE.2, RES.10
- [ ] **MED.5** Video and audio transcoding with ffmpeg as queue tasks (probe first, protocol whitelist, forced input format, timeouts) [0.7] — needs: MED.3, QUE.2, RES.10
- [ ] **MED.6** Gated thumbnail series, never enlarged [0.7] — needs: MED.4, MED.5
- [ ] **MED.7** media: Markdown syntax and HTML5 players [0.7] — needs: RND.1, MED.6, UI.14
- [ ] **MED.8** Admin purge of originals [0.7] — needs: MED.3, AUTH.3
- [ ] **MED.9** Optional ClamAV scan of uploads (off by default, admin switch, clamdscan or INSTREAM socket) [0.7] — needs: MED.3, QUE.2
- [ ] **MED.10** Optional WebVTT captions per video and transcript link per audio file; renderer emits track elements [0.7] — needs: MED.7
- [ ] **MED.11** Media records and metadata: stable media id, title, description, alt text, credit and source, licence, tags, setting, uploader, content hash, sizes; metadata editing through the API and revisioned in the audit log [0.7] — needs: MED.3, DB.2, AUTH.7
- [ ] **MED.12** Usage index: which pages reference each file (current revision and history), updated on every page save, rebuild command, orphan detection [0.7] — needs: MED.7, GIT.2, MED.11
- [ ] **MED.13** Media library API: list, search, filter (type, setting, tag, uploader, visibility, orphaned, status) and sort with pagination; metadata read and patch [0.7] — needs: MED.11, API.4, VIS.2
- [ ] **MED.14** Per-file visibility (public or GM-only) enforced in file serving, library, search, embeds and downloads, with leak tests [0.7] — needs: MED.11, VIS.2
- [ ] **MED.15** Replace, re-process and rename without breaking embeds: embeds refer to the stable media id, old URLs redirect, replaced versions are kept as old versions until pruned [0.7] — needs: MED.11, MED.12, MED.6
- [ ] **MED.16** Variants view and regeneration: list variants of a file, regenerate one or all as queue tasks [0.7] — needs: MED.6, MED.11
- [ ] **MED.17** Moderation and approval queue: editor uploads wait as pending, moderators approve or reject with a reason, pending files are never served publicly [0.7] — needs: MED.2, MED.11, AUTH.3
- [ ] **MED.18** Duplicate detection by content hash at upload and in a library report, with merge of duplicates that rewrites embeds through the media id [0.7] — needs: MED.3, MED.12
- [ ] **MED.19** Bulk actions API: tag, set setting or visibility, delete, purge originals; run as queue tasks, one audit entry per action [0.7] — needs: MED.13, MED.8, QUE.2
- [ ] **MED.20** Storage statistics and quota: usage by type, user and setting, admin quota settings enforced at upload [0.7] — needs: MED.11, CFG.4
- [ ] **MED.21** Copyright and removal handling: takedown hides a file at once, removes originals and variants, leaves a tombstone and an audit entry; removal contact from COPYRIGHT.md is shown on the media page [0.7] — needs: MED.8, MED.14, AUTH.7
- [ ] **MED.22** Media permissions and API-key scopes: view, upload, edit own, edit any, moderate, delete, purge originals, prune [0.7] — needs: AUTH.3, API.4
- [ ] **MED.23** Prune policy (decide and record in docs/design/media.html): a file is in use when the current revision of any page references it; references only in git history count while the admin setting `media.history_counts` is on (default on) and are released otherwise; replaced versions and stale variants have a retention period; originals follow the admin purge policy; default grace period 30 days [0.7] — needs: MED.12, MED.8
- [ ] **MED.24** Locking: one lock shared by uploads, replace, regenerate and prune so prune never runs against an upload, and every deletion re-checks references under the lock [0.7] — needs: MED.3, QUE.2
- [ ] **MED.25** prune-media core: finds unreferenced media, old versions and stale variants; dry-run by default with a report; marks candidates and deletes only after the grace period; never deletes anything still referenced [0.7] — needs: MED.23, MED.24, MED.12
- [ ] **MED.26** scripts/prune-media command (--apply, --grace, --json report) writing one audit entry per run with counts and bytes freed [0.7] — needs: MED.25, AUTH.7
- [ ] **MED.27** systemd service and timer for prune-media in examples/ (runs as the app user, nice and ionice, dry-run unless apply is enabled in settings) with install notes in the admin guide [0.7] — needs: MED.26, FND.6
- [ ] **MED.28** Admin prune API: trigger a run, view status, last report and history, edit prune settings [0.7] — needs: MED.26, API.4, AUTH.8
- [ ] **MED.29** Media suite tests: prune never deletes referenced or history-held files, grace period, lock against concurrent upload, replace keeps embeds, visibility and takedown leak tests [0.7] — needs: MED.25, MED.15, MED.21, MED.14

## UI: Web UI (first-party JavaScript client)

Issue: [#23](https://github.com/dwhagar/spakr/issues/23)

- [ ] **UI.1** JavaScript client scaffold: no-build ES modules and hand-written CSS in src/spakr/web/static, served from our origin with hashed file names (Python script, no Node) [0.1] — needs: FND.3, RES.11, RES.22, RES.24
- [ ] **UI.2** Server-rendered public reading pages with SEO markup [0.8] — needs: UI.13, UI.14, RND.5, ENT.13
- [ ] **UI.3** Login, invitation and account screens [0.8] — needs: UI.13, AUTH.4, AUTH.5, AUTH.10
- [ ] **UI.4** Page editor with preview: textarea, small toolbar and server-rendered preview (CodeMirror only after 1.0, needs a CSP nonce) [0.8] — needs: UI.2, UI.13, RND.6, GIT.7
- [ ] **UI.5** History, diff and revert screens [0.8] — needs: UI.2, UI.13, GIT.4
- [ ] **UI.6** Browse and search screens [0.8] — needs: UI.2, UI.13, SEARCH.5, LNK.4
- [ ] **UI.7** Admin screens: allowlist, users, API keys [0.8] — needs: UI.3, UI.13, AUTH.6, AUTH.8, AUTH.9, LNK.6
- [ ] **UI.8** Upload and media screens [0.8] — needs: UI.2, UI.13, MED.7
- [ ] **UI.9** Licence statement in the footer and on edit/upload pages [0.8] — needs: UI.2, UI.13
- [ ] **UI.10** Home page, navigation and recent-changes screen [0.8] — needs: UI.2, UI.13, LNK.7
- [ ] **UI.11** Responsive layout base: mobile-first CSS, fluid grid and navigation, readable at phone width, no horizontal page scroll (standing requirement from the first screen) [0.1] — needs: UI.1, RES.21, RES.23
- [ ] **UI.12** Theme tokens: light and dark palettes as CSS variables following prefers-color-scheme, plus a user toggle stored server-side so it works without inline script [0.1] — needs: UI.11, RES.21
- [ ] **UI.13** UI acceptance checklist applied to every UI item: responsive from small phone and foldable through tablet and desktop to big-screen TV, correct in light and dark, keyboard and remote usable [0.1] — needs: UI.11, UI.12, RES.23
- [ ] **UI.14** Responsive, themed tables, code blocks and HTML5 media players in rendered pages [0.3] — needs: UI.12, RND.1
- [ ] **UI.15** Large-screen (TV) and foldable layouts: scaled type and spacing, visible focus and remote or keyboard navigation, safe areas, fold-aware spacing [0.1] — needs: UI.11, UI.12, RES.23
- [ ] **UI.16** Device test matrix and screenshot checks at phone, foldable, tablet, desktop and TV widths in light and dark [0.1] — needs: UI.13, UI.15, TST.1
- [ ] **UI.17** Asset tooling in Python: scripts/hash-assets, make-icons and check-contrast, THIRD-PARTY.md for vendored files, and per-page size budgets checked in the daily run [0.1] — needs: UI.1, FND.7
- [ ] **UI.18** Web app manifest and icons so the site can be installed; no service worker in 1.0 [0.8] — needs: UI.2
- [ ] **UI.19** Search-as-you-type combobox and the editor link picker (progressive ARIA combobox over the autocomplete endpoint) [0.8] — needs: UI.6, SEARCH.7
- [ ] **UI.20** Media library screens: browse as grid or list, search, filter, sort, select several; responsive and themed [0.8] — needs: UI.8, UI.13, MED.13
- [ ] **UI.21** Media detail screen: metadata editor, usage list, variants view and regeneration, replace and rename, visibility, takedown [0.8] — needs: UI.20, MED.12, MED.15, MED.16, MED.21
- [ ] **UI.22** Media moderation queue and bulk-action screens [0.8] — needs: UI.20, MED.17, MED.19
- [ ] **UI.23** Admin media screens: storage statistics and quota, duplicates report, prune settings, trigger and status of prune runs [0.8] — needs: UI.20, MED.18, MED.20, MED.28

## OPS: Hardening and operations

Issue: [#24](https://github.com/dwhagar/spakr/issues/24)

- [ ] **OPS.1** Security review [0.9] — needs: UI.7, UI.8, CFG.7, SEARCH.6, VIS.3, MED.14, MED.21
- [ ] **OPS.2** Rate limiting [0.9] — needs: API.4, RES.12
- [ ] **OPS.3** Error pages [0.9] — needs: UI.2
- [ ] **OPS.4** Accessibility pass [0.9] — needs: UI.8, UI.21, RES.18, UI.13
- [ ] **OPS.5** Backup acceptance on a clean install: the latest nightly backup, with parity, restores into a fresh server and matches the original (delivered by the BAK category) [0.9] — needs: BAK.12, BAK.13, BAK.14, BAK.26
- [ ] **OPS.6** Import and export [0.9] — needs: GIT.2, ENT.1, RES.19
- [ ] **OPS.7** Clean-install test on Ubuntu 24.04; best-effort pass on 26.04 [0.9] — needs: DOC.3, OPS.5

## RES: Research and decisions (phase 0.0)

Issue: [#27](https://github.com/dwhagar/spakr/issues/27)

- [x] **RES.1** MultiMarkdown options: libmultimarkdown vs Python-Markdown extensions vs pandoc; what Ubuntu 24.04 ships [0.0]
- [x] **RES.2** Server-side LaTeX math (decided: no Node anywhere): pure-Python latex2mathml (MIT) behind guards, TeX-source fallback; static markup, no client script [0.0]
- [x] **RES.3** HTML sanitiser library (nh3, bleach or own) and how the admin allowlist maps onto it [0.0]
- [x] **RES.4** Git access from Python: GitPython, dulwich or the git binary via subprocess; locking and speed [0.0]
- [x] **RES.5** Password hashing, sessions and CSRF: argon2-cffi and Flask extensions versus own code [0.0]
- [x] **RES.6** Email through an external SMTP relay (never a local MTA): library, TLS modes, relay settings as configuration, SPF/DKIM notes [0.0]
- [x] **RES.7** Search approach: InnoDB FULLTEXT (default parser or ngram) versus an external engine; relevance trials on sample pages [0.0]
- [x] **RES.8** SEO libraries and markup: sitemap writer, canonical URLs, meta and structured data [0.0]
- [x] **RES.9** Upload type sniffing: python-magic or filetype, and whether to add a virus scan [0.0]
- [x] **RES.10** Media toolchain per operation: confirm the efficient choice (ImageMagick or Pillow for images; ffmpeg for all audio and video). ffmpeg and ImageMagick are preferred; Python libraries allowed where measurably better (builds on docs/research/media-processing.html) [0.0]
- [x] **RES.11** Front-end approach: plain JavaScript modules or a small library, build and asset-hashing tooling, CSP-compatible [0.0]
- [x] **RES.12** Rate limiting: Flask-Limiter or own Redis counters [0.0]
- [ ] **RES.13** Entity field definitions: choose the structured fields and front matter schema for each entity type [0.0]
- [x] **RES.14** OpenAPI generation: apispec/flask-smorest or hand-written description [0.0]
- [x] **RES.15** Python packaging and dependencies on Ubuntu 24.04: apt versus venv, pyproject layout [0.0]
- [x] **RES.16** Apache hosting: mod_wsgi versus a proxy to gunicorn; which scripts stay CGI [0.0]
- [x] **RES.17** Backup approach for MySQL, the git store and media (mysqldump, git bundle, rsync) [0.0]
- [x] **RES.18** Accessibility checklist (WCAG 2.2 AA) for the UI [0.0]
- [ ] **RES.19** Import and export formats [0.0]
- [x] **RES.20** Settings and secrets implementation details: file locking, mode 0600, atomic rewrite of config.json and reload across workers (approach decided: the app rewrites config.json, secret fields write-only) [0.0]
- [x] **RES.21** CSS approach and design system: modern CSS (custom properties, container queries, grid, clamp, light-dark, logical properties) with no framework versus a small utility or component library; self-hosted fonts and inline SVG icons; no CSS-in-JS [0.0]
- [x] **RES.22** Is Node.js justified? Build-time-only tooling (esbuild or Vite versus none) for bundling, asset hashing and CSS processing; runtime stays Python; effect on install, CI and the CSP [0.0]
- [x] **RES.23** Device range from small phone and foldable to tablet, desktop and big-screen TV: breakpoints and fluid type, foldable viewport segments, 10-foot layout and remote or keyboard focus navigation, safe areas, test matrix [0.0]
- [x] **RES.24** Front-end component approach: plain modules versus web components versus a small library (size, accessibility, no inline script), plus state and routing for the API-driven client [0.0]
- [x] **RES.25** Caching of rendered pages in memory and on disk: key by content, layers, eviction, link-status pass (docs/research/caching.html) [0.0]
- [ ] **RES.26** Parity and redundancy for /data: par2-style parity versus erasure coding (zfec, reedsolo) versus filesystem options (ZFS or btrfs scrub, dm-integrity, RAID); cost for 100 MB videos and for git packs, how parity is stored and refreshed, recovery procedure [0.0]
- [ ] **RES.27** Source of truth versus rebuildable: classify every table and file; what lives only in MySQL (accounts, settings, audit, invitations) and so needs a checksummed journal; what is rebuilt from the git content store and media originals; depends on the MySQL-versus-git findings (done: RES.29) [0.0]
- [ ] **RES.28** Checksum design: hash algorithm (SHA-256 versus BLAKE2 in hashlib), manifest format and location, row or table checksums and an audit hash chain in MySQL, migration records, cost of scheduled verification [0.0]
- [x] **RES.29** MySQL or git for page content: measured saves, concurrency, history, growth, backups and corruption trials; git stays the source of truth (docs/research/content-store-choice.html) [0.0]
- [ ] **RES.30** Backup design: consistent snapshot of MySQL (mysqldump single-transaction), the git store and media without stopping the site; archive layout and naming; tar.bz2 versus tar.gz speed and size (and parallel bzip2); whether media is full nightly or incremental; par2cmdline on Ubuntu 24.04 and its redundancy defaults; retention scheme; restore order (builds on RES.17 and RES.29) [0.0] — needs: RES.17, RES.29
- [ ] **RES.31** Secrets and privacy in backups (decision): config.json holds secrets and the database holds password hashes and GM-only content; options are exclude secrets (back up a redacted config), include config unencrypted at 0600, or encrypt archives (age or gpg) and what the off-host copy must do; record the decision [0.0] — needs: RES.20

## TST: Testing and sample content

Issue: [#28](https://github.com/dwhagar/spakr/issues/28)

- [ ] **TST.1** Test harness: pytest fixtures for a temporary MySQL schema, git repository and Redis [0.1] — needs: FND.7, DB.2
- [ ] **TST.2** API test client and authentication helpers [0.4] — needs: TST.1, AUTH.2
- [ ] **TST.3** Sample content set across all entity types and the three settings (CC BY-SA), loadable by CLI [0.5] — needs: ENT.11, FND.9
- [ ] **TST.4** End-to-end smoke test: install, create admin, write, link, search, upload [0.9] — needs: UI.8, TST.3, OPS.7

## INT: Integrity, parity and recovery

Issue: [#51](https://github.com/dwhagar/spakr/issues/51)

Principle (owner decision): the system is built from the ground up with checksums and parity data so a damaged database or store can be detected and rebuilt. Every stored artifact has a checksum, every artifact is classed as source of truth or rebuildable (INT.1), and every class has a tested recovery path.

- [ ] **INT.1** Integrity principle and data classification recorded in docs/design/integrity.html: source of truth versus rebuildable for every table and file, checksum rules, recovery path per class; DB, GIT and MED items conform to it [0.1] — needs: RES.26, RES.27, RES.28
- [ ] **INT.2** Schema integrity rules: migration records carry a content hash and refuse to run on a mismatch, row checksums on source-of-truth tables, hash-chained audit log; added as a migration on top of DB.2 [0.1] — needs: DB.2, INT.1
- [ ] **INT.3** Hash manifest library: compute and verify SHA-256 manifests per directory with atomic writes, used by every store [0.1] — needs: FND.11, INT.1
- [ ] **INT.4** Content store checks: git fsck after maintenance and on schedule, ref and HEAD verification, page files compared with the MySQL index [0.2] — needs: GIT.1, INT.3
- [ ] **INT.5** Media rebuild: rebuild media records, usage index and variants from originals and manifests; resumable, dry-run option [0.7] — needs: MED.11, MED.12, INT.3
- [ ] **INT.6** Media checksums: originals and variants hashed at upload and processing, recorded in the media record and manifest, verified by scheduled checks and optionally on serve [0.7] — needs: MED.3, MED.6, INT.3
- [ ] **INT.7** Parity data for the content store, in the scheme chosen by RES.26, refreshed by a queue task and stored under /data/parity [0.2] — needs: RES.26, GIT.1, INT.3, QUE.2
- [ ] **INT.8** Parity data for media originals (and variants if cheap), same scheme, refreshed after upload and replace [0.7] — needs: INT.7, MED.3
- [ ] **INT.9** Journal of MySQL-only source-of-truth data (accounts, settings, audit, invitations) to checksummed files, written on change and compacted daily, so the database can be rebuilt from it [0.4] — needs: INT.2, AUTH.7, CFG.4
- [ ] **INT.10** `spakr verify` command: runs every check (git fsck, manifests, row checksums, migration hashes, parity), human and JSON reports, exit codes, repair plan output [0.2] — needs: INT.3, INT.4, FND.9
- [ ] **INT.11** Scheduled verification: systemd service and timer in examples/ (light daily, full weekly), results stored and the admin notified on failure [0.7] — needs: INT.10, FND.6, INT.6
- [ ] **INT.12** Health and status report integrity state (ok, degraded, corrupt, last verified) and bump the API version for the new fields [0.2] — needs: INT.10, API.8
- [ ] **INT.13** `spakr repair`: repair from parity, restore from backup, quarantine corrupt files, rebuild derived data; dry-run by default, audit entry per run [0.7] — needs: INT.10, INT.5, INT.7, INT.8, INT.9, AUTH.7, BAK.12
- [ ] **INT.14** Admin integrity screen: status, last verification, run verify, review repair plan [0.8] — needs: INT.12, INT.13, UI.7
- [ ] **INT.15** Damage-and-recover tests: corrupt git objects, drop the MySQL database, flip bytes in media, truncate manifests; assert detection and full recovery [0.7] — needs: INT.13, INT.5, INT.8
- [ ] **INT.16** Recovery guide for admins: what is checked, how to read a verify report, how to repair and rebuild, how backups and parity fit together [0.9] — needs: INT.13, OPS.5, BAK.27

## BAK: Backups and recovery pipeline

Issue: [#54](https://github.com/dwhagar/spakr/issues/54)

Owner decision: nightly backups of all data stored in /data/backups, each with a parity file; tar.bz2 by default, gz as an option. Built on the INT category (checksums, manifests, parity) and ordered so the basics (settings, layout, manifest, DB dump, config policy, restore) land first.

- [ ] **BAK.1** Backup design recorded in docs/design/backups.html: what a backup contains, naming, manifest, parity, retention, secrets policy, restore order, which data is source of truth (INT.1) [0.1] — needs: RES.30, RES.31, INT.1
- [ ] **BAK.2** Backup settings in config.json.example and the settings registry: enabled, directory (default /data/backups), format bz2 (default) or gz, parity redundancy percent, retention, off-host command, alert on failure, stale-after hours; validated [0.1] — needs: CFG.1, CFG.2, BAK.1
- [ ] **BAK.3** Directory layout and permissions: /data/backups created at startup, directory 0700 and files 0600 owned by the dedicated user; refuses to run when the path is world-readable or under a web-served path [0.1] — needs: FND.11, BAK.1
- [ ] **BAK.4** Backup manifest on the INT.3 helper: manifest.json per backup with name, time, software, API and schema versions, format, component list, SHA-256 and size per file, written atomically [0.1] — needs: INT.3, BAK.1
- [ ] **BAK.5** MySQL dump component: consistent single-transaction dump, credentials passed through a 0600 option file (never on the command line or in logs), schema version recorded [0.1] — needs: DB.2, BAK.2, BAK.4
- [ ] **BAK.6** Config component by explicit policy (RES.31): default is a redacted copy of config.json plus the list of secret keys to re-enter, with an optional encrypted full copy; the policy is logged in the manifest [0.1] — needs: FND.2, RES.31, BAK.4
- [ ] **BAK.7** Archive builder: tar.bz2 by default or tar.gz by setting, written to a temporary name and renamed atomically, named spakr-YYYYMMDDTHHMMSSZ-vVERSION [0.1] — needs: BAK.3, BAK.4, BAK.5, BAK.6
- [ ] **BAK.8** Parity file set per backup with par2, redundancy percent configurable (default 10), created after the archive and listed in the manifest; a clear error when par2 is missing [0.1] — needs: BAK.7, RES.30
- [ ] **BAK.9** Verify after write: re-read the archive against the manifest checksums, run par2 verify, list the archive; a failed backup is renamed .failed and reported, never counted as good [0.1] — needs: BAK.8
- [ ] **BAK.10** Consistent snapshot and locking: one backup lock, taken together with the git write lock so no page is half-written in the snapshot; extended to uploads and prune-media by BAK.14 [0.2] — needs: GIT.1, BAK.9
- [ ] **BAK.11** `spakr backup` command (--now, --format, --redundancy, --dry-run, --json) with exit codes for cron and systemd [0.1] — needs: BAK.9, FND.9
- [ ] **BAK.12** `spakr restore` command: --list, verify manifest and parity first, repair with par2 when damaged, restore into an empty target, refuse to overwrite without --force, secrets re-entered when the config was redacted [0.1] — needs: BAK.11, DB.4
- [ ] **BAK.13** Git content store component: snapshot under the write lock (git bundle or repository archive), restored copy checked with git fsck [0.2] — needs: GIT.1, BAK.10, BAK.12
- [ ] **BAK.14** Media component: originals and manifests (variants optional, off by default because they are rebuildable), coordinated with uploads and prune-media through the shared lock [0.7] — needs: MED.3, MED.24, BAK.10, BAK.12
- [ ] **BAK.15** Retention and rotation: keep N daily, W weekly and M monthly backups (settings); delete the oldest only after a newer backup verified; never delete the last verified backup; parity files go with their archive [0.2] — needs: BAK.9, BAK.2
- [ ] **BAK.16** Nightly systemd service and timer in examples/ (dedicated user, idle I/O class, randomised delay, ProtectSystem with /data/backups writable) and install notes [0.2] — needs: BAK.11, FND.6
- [ ] **BAK.17** Optional off-host copy hook: a configurable command run after a verified backup and given the archive, parity and manifest paths; a failed copy alerts but does not fail the backup; unencrypted copies only when the admin allows them [0.2] — needs: BAK.9, BAK.2, RES.31
- [ ] **BAK.18** Backup status: last backup time, result, size, verified flag and age kept in a status file and reported in health and status (degraded when older than the stale-after setting), with an API version bump [0.2] — needs: BAK.11, API.8, INT.12
- [ ] **BAK.19** Failure and staleness alerts through the configured mail relay and the log, throttled to avoid repeats [0.4] — needs: BAK.18, MAIL.1
- [ ] **BAK.20** Admin backup API: list, status, run now through the queue, verify, delete; admin permission only; restore stays command-line only in 1.0 [0.4] — needs: BAK.18, API.4, QUE.2, AUTH.8
- [ ] **BAK.21** Security hardening: no backups under a web-served path, Apache example denies /data, backup permission and ownership checks in `spakr verify`, dedicated user documented, no secrets in command lines or logs [0.2] — needs: BAK.3, FND.6, INT.10
- [ ] **BAK.22** Admin backup screen: list, status, last result, run now, verify, restore instructions [0.8] — needs: BAK.20, UI.7
- [ ] **BAK.23** Round-trip tests: backup, restore into fresh directories and schema, compare content, hashes and versions, for tar.bz2 and tar.gz; extended as BAK.13 and BAK.14 land [0.1] — needs: BAK.12
- [ ] **BAK.24** Damage-and-repair tests: flip bytes in and truncate the archive, damage the manifest, remove the parity file; assert par2 repair, clear failure messages and a successful restore after repair [0.2] — needs: BAK.8, BAK.23, BAK.13
- [ ] **BAK.25** `spakr verify` and `spakr repair` cover the backup set: checksums and parity of the latest backups, repair of a damaged backup from parity, and restore from backup as a repair source [0.2] — needs: INT.10, BAK.8
- [ ] **BAK.26** Restore drill: `spakr restore --drill` restores the latest backup into scratch space and compares it with the live data, run monthly by a timer, result kept in the status [0.7] — needs: BAK.14, BAK.16
- [ ] **BAK.27** Backup and recovery guide: settings, timer install, restore steps, secrets policy, off-host copy, retention, hardening, the drill [0.9] — needs: BAK.22, BAK.26, BAK.17

## CFG: Configuration and settings

Issue: [#31](https://github.com/dwhagar/spakr/issues/31)

- [ ] **CFG.1** examples/config.json.example listing every option, secrets marked, MySQL marked manual-only [0.1] — needs: FND.2, CFG.2
- [ ] **CFG.2** Settings registry: each option defined once (key, type, default, secret, web-editable, validation) and used by the loader, API, UI and example [0.1] — needs: FND.2, RES.20
- [x] **CFG.3** MySQL credentials: manual-only in config.json; never exposed or editable through the API or UI; clear startup error if missing [0.1] — needs: FND.2, CFG.2
- [ ] **CFG.4** Settings store: non-secret settings in the database config table with typed access, caching and audit of changes [0.4] — needs: CFG.2, DB.2
- [ ] **CFG.5** Secrets handling (decided): the app rewrites config.json atomically at mode 0600 with file locking; secret fields are write-only through the API and UI (set or unset, never returned), redacted in logs and audit [0.4] — needs: CFG.2, RES.20
- [ ] **CFG.6** Live reload of changed settings across WSGI workers and the queue worker [0.4] — needs: CFG.4, CFG.5, QUE.2
- [ ] **CFG.7** Admin settings screens for every web-editable option, grouped and validated, secret fields write-only [0.8] — needs: CFG.4, CFG.5, AUTH.8, UI.3, UI.13
- [x] **CFG.8** Graceful failure when config.json is missing or invalid: a clear message naming the file and examples/config.json.example, non-zero exit from the command line, no traceback, and the app reports itself as not configured [0.1] — needs: FND.2, CFG.2
