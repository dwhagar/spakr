# TODO

Current version: **0.0.0** (see [`VERSION`](VERSION) and [`scripts/version.sh`](scripts/version.sh)). Versions are `MAJOR.MINOR.BUILD`; BUILD counts up with every push to `main`, MINOR and MAJOR are planned and set by hand.

Items are numbered `[CAT].[NUMBER]`, for example `API.1`. Each item shows its phase in square brackets (the MINOR version that delivers it) and `needs:` the ids it depends on, so the list forms a tree rooted in phase 0.0 research and the foundation. Phases 0.1 to 0.8 are building blocks; **0.9 is the pre-release working version**; 1.0 is the release. See the [phase plan](docs/plan/tiers.html) and the [dependency tree](docs/plan/tree.html).

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
- [ ] **DOC.3** Admin install and upgrade guide [0.9] — needs: FND.6, DB.2, QUE.2, OPS.5
- [ ] **DOC.4** Editor guide: writing pages, links, media syntax, visibility [0.9] — needs: UI.4, MED.7, LNK.1
- [ ] **DOC.5** API reference generated from the OpenAPI description [0.9] — needs: API.3

## FND: Foundation

Issue: [#10](https://github.com/dwhagar/spakr/issues/10)

- [ ] **FND.1** Python package skeleton in src/ with pyproject and pinned dependencies [0.1] — needs: RES.15
- [ ] **FND.2** JSON configuration loader with validation against examples/spakr.conf.example [0.1] — needs: FND.1
- [ ] **FND.3** WSGI entry point and the small CGI shim [0.1] — needs: FND.1, API.1, RES.16
- [ ] **FND.4** Shared outbound HTTP helper with the required User-Agent (software, version, API version) [0.1] — needs: FND.1
- [ ] **FND.5** Dev setup script for Ubuntu 24.04 [0.1] — needs: FND.1, RES.15
- [ ] **FND.6** Apache vhost and systemd unit examples in examples/ [0.1] — needs: FND.3, QUE.2, RES.16
- [ ] **FND.7** Lint, format and test tooling; tests workflow stays on the 07:00 UTC schedule only [0.1] — needs: FND.1
- [ ] **FND.8** Structured logging [0.1] — needs: FND.1, FND.2
- [ ] **FND.9** Command-line tool (spakr): init-db, create-admin, reindex, load-sample, version [0.1] — needs: FND.2, DB.1

## API: API (Flask, /api/v1)

Issue: [#11](https://github.com/dwhagar/spakr/issues/11)

- [ ] **API.1** Flask app factory and /api/v1 skeleton with health endpoint [0.1] — needs: FND.1, FND.2
- [ ] **API.2** Error format, pagination and filtering conventions [0.1] — needs: API.1
- [ ] **API.3** OpenAPI description kept in step with the routes [0.1] — needs: API.2, RES.14
- [ ] **API.4** Permission decorator used by every route (session or API key) [0.4] — needs: API.1, AUTH.2, AUTH.3
- [ ] **API.5** Generic CRUD helpers for page-backed resources [0.5] — needs: API.4, ENT.1, GIT.2

## DB: Database

Issue: [#12](https://github.com/dwhagar/spakr/issues/12)

- [ ] **DB.1** SQLAlchemy engine and session setup [0.1] — needs: FND.2
- [ ] **DB.2** Alembic migrations creating the schema in docs/design/database.html [0.1] — needs: DB.1
- [ ] **DB.3** Command to rebuild the MySQL index from the git content store [0.2] — needs: DB.2, GIT.5, SEARCH.2
- [ ] **DB.4** Database backup and restore script [0.9] — needs: DB.2

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

## RND: Rendering and sanitising

Issue: [#15](https://github.com/dwhagar/spakr/issues/15)

- [ ] **RND.1** MultiMarkdown rendering [0.3] — needs: FND.1, RES.1
- [ ] **RND.2** LaTeX math rendered server-side to static markup [0.3] — needs: RND.1, RES.2
- [ ] **RND.3** HTML sanitiser with the admin-approved allowlist [0.3] — needs: RND.1, RES.3
- [ ] **RND.4** Strict Content-Security-Policy and security headers (no inline script or style) [0.3] — needs: API.1, UI.1
- [ ] **RND.5** Rendered-page cache keyed by revision [0.3] — needs: RND.1, GIT.2
- [ ] **RND.6** Preview endpoint [0.5] — needs: RND.1, RND.3, API.4

## AUTH: Accounts, roles and API keys

Issue: [#16](https://github.com/dwhagar/spakr/issues/16)

- [ ] **AUTH.1** Users and password hashing [0.4] — needs: DB.2, RES.5
- [ ] **AUTH.2** Login, logout, cookie sessions and CSRF header [0.4] — needs: AUTH.1, API.1
- [ ] **AUTH.3** Roles and permissions: reader, editor, GM, mod, admin [0.4] — needs: AUTH.1, DB.2
- [ ] **AUTH.4** Invitation flow (7-day tokens) [0.4] — needs: AUTH.1, MAIL.2
- [ ] **AUTH.5** Password reset flow (1-hour tokens) [0.4] — needs: AUTH.1, MAIL.2
- [ ] **AUTH.6** API keys: users limited to their own permissions, admins unlimited, per-user cap [0.4] — needs: AUTH.2, AUTH.3
- [ ] **AUTH.7** Audit log [0.4] — needs: DB.2
- [ ] **AUTH.8** Admin settings API [0.4] — needs: AUTH.3, API.4
- [ ] **AUTH.9** HTML allowlist approval API [0.4] — needs: AUTH.8, RND.3
- [ ] **AUTH.10** Account editing API (profile, email, password, roles) [0.4] — needs: AUTH.2, AUTH.3
- [ ] **AUTH.11** Bootstrap the first admin account from the command line [0.4] — needs: FND.9, AUTH.1, AUTH.3

## MAIL: Email

Issue: [#17](https://github.com/dwhagar/spakr/issues/17)

- [ ] **MAIL.1** SMTP sender through the local MTA or a configured relay (blocked on the open SMTP question) [0.4] — needs: FND.2, RES.6
- [ ] **MAIL.2** Invitation and password-reset templates, sent via the queue [0.4] — needs: MAIL.1, QUE.2, DB.2

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
- [ ] **SEARCH.2** Search document builder: plain text of the Markdown plus title, summary, aliases, tags, settings and type-field text, written on every page save [0.2] — needs: GIT.5, DB.2, SEARCH.1
- [ ] **SEARCH.3** Full-text query endpoint over the full page index: natural and boolean modes, relevance ranking, highlighted snippets, pagination [0.6] — needs: SEARCH.2, VIS.2, RES.7
- [ ] **SEARCH.4** Field search: type, setting, tag, name/title and type-specific fields (for example race, place, occupation) as API parameters and query syntax such as type:character setting:scifi tag:undead [0.6] — needs: SEARCH.3, ENT.1, LNK.5
- [ ] **SEARCH.5** Filters and facet counts by type, setting and tag [0.6] — needs: SEARCH.4
- [ ] **SEARCH.6** Visibility in search: GM-only pages excluded for users without the GM role, using the copied visibility column [0.6] — needs: SEARCH.3, VIS.2
- [ ] **SEARCH.7** Name and alias autocomplete for search-as-you-type and the link picker [0.6] — needs: SEARCH.2
- [ ] **SEARCH.8** Tokeniser decision: InnoDB default parser or ngram, minimum token size and stopword settings, set by the admin [0.6] — needs: SEARCH.2, RES.7
- [ ] **SEARCH.9** SEO metadata, sitemap.xml and robots.txt [0.6] — needs: GIT.5, VIS.2, RES.8
- [ ] **SEARCH.10** Memory (Redis, per-process) and disk caches for rendered pages [0.6] — needs: RND.5, QUE.1

## MED: Uploads and media

Issue: [#22](https://github.com/dwhagar/spakr/issues/22)

- [ ] **MED.1** Upload endpoint: type sniffing, size limits (10 MB, 100 MB video), safe-list [0.7] — needs: API.4, RES.9
- [ ] **MED.2** Quarantine and admin override [0.7] — needs: MED.1
- [ ] **MED.3** Hashed media directories; originals kept privately [0.7] — needs: MED.1
- [ ] **MED.4** Image processing with ImageMagick as queue tasks [0.7] — needs: MED.3, QUE.2, RES.10
- [ ] **MED.5** Video and audio transcoding with ffmpeg as queue tasks [0.7] — needs: MED.3, QUE.2, RES.10
- [ ] **MED.6** Gated thumbnail series, never enlarged [0.7] — needs: MED.4, MED.5
- [ ] **MED.7** media: Markdown syntax and HTML5 players [0.7] — needs: RND.1, MED.6
- [ ] **MED.8** Admin purge of originals [0.7] — needs: MED.3, AUTH.3

## UI: Web UI (first-party JavaScript client)

Issue: [#23](https://github.com/dwhagar/spakr/issues/23)

- [ ] **UI.1** JavaScript client scaffold, served from our origin with hashed assets [0.1] — needs: FND.3, RES.11
- [ ] **UI.2** Server-rendered public reading pages with SEO markup [0.8] — needs: UI.1, RND.5, ENT.13
- [ ] **UI.3** Login, invitation and account screens [0.8] — needs: UI.1, AUTH.4, AUTH.5, AUTH.10
- [ ] **UI.4** Page editor with preview [0.8] — needs: UI.2, RND.6, GIT.7
- [ ] **UI.5** History, diff and revert screens [0.8] — needs: UI.2, GIT.4
- [ ] **UI.6** Browse and search screens [0.8] — needs: UI.2, SEARCH.5, LNK.4
- [ ] **UI.7** Admin screens: settings, allowlist, users, API keys [0.8] — needs: UI.3, AUTH.6, AUTH.8, AUTH.9, LNK.6
- [ ] **UI.8** Upload and media screens [0.8] — needs: UI.2, MED.7
- [ ] **UI.9** Licence statement in the footer and on edit/upload pages [0.8] — needs: UI.2
- [ ] **UI.10** Home page, navigation and recent-changes screen [0.8] — needs: UI.2, LNK.7

## OPS: Hardening and operations

Issue: [#24](https://github.com/dwhagar/spakr/issues/24)

- [ ] **OPS.1** Security review [0.9] — needs: UI.7, UI.8, SEARCH.6, VIS.3
- [ ] **OPS.2** Rate limiting [0.9] — needs: API.4, RES.12
- [ ] **OPS.3** Error pages [0.9] — needs: UI.2
- [ ] **OPS.4** Accessibility pass [0.9] — needs: UI.8, RES.18
- [ ] **OPS.5** Backup script covering git store, MySQL and media [0.9] — needs: DB.4, GIT.1, MED.3, RES.17
- [ ] **OPS.6** Import and export [0.9] — needs: GIT.2, ENT.1, RES.19
- [ ] **OPS.7** Clean-install test on Ubuntu 24.04; best-effort pass on 26.04 [0.9] — needs: DOC.3, OPS.5

## RES: Research and decisions (phase 0.0)

Issue: [#27](https://github.com/dwhagar/spakr/issues/27)

- [ ] **RES.1** MultiMarkdown options: libmultimarkdown vs Python-Markdown extensions vs pandoc; what Ubuntu 24.04 ships [0.0]
- [ ] **RES.2** Server-side LaTeX math: KaTeX, MathJax, latex2mathml or pandoc; static markup, no client script [0.0]
- [ ] **RES.3** HTML sanitiser library (nh3, bleach or own) and how the admin allowlist maps onto it [0.0]
- [ ] **RES.4** Git access from Python: GitPython, dulwich or the git binary via subprocess; locking and speed [0.0]
- [ ] **RES.5** Password hashing, sessions and CSRF: argon2-cffi and Flask extensions versus own code [0.0]
- [ ] **RES.6** Email: SMTP relay and sender address (needs a decision from the owner), library, SPF/DKIM notes [0.0]
- [ ] **RES.7** Search approach: InnoDB FULLTEXT (default parser or ngram) versus an external engine; relevance trials on sample pages [0.0]
- [ ] **RES.8** SEO libraries and markup: sitemap writer, canonical URLs, meta and structured data [0.0]
- [ ] **RES.9** Upload type sniffing: python-magic or filetype, and whether to add a virus scan [0.0]
- [ ] **RES.10** Media tool policies on Ubuntu 24.04: ImageMagick policy.xml, ffmpeg builds and sandboxing (builds on docs/research/media-processing.html) [0.0]
- [ ] **RES.11** Front-end approach: plain JavaScript modules or a small library, build and asset-hashing tooling, CSP-compatible [0.0]
- [ ] **RES.12** Rate limiting: Flask-Limiter or own Redis counters [0.0]
- [ ] **RES.13** Entity field definitions: choose the structured fields and front matter schema for each entity type [0.0]
- [ ] **RES.14** OpenAPI generation: apispec/flask-smorest or hand-written description [0.0]
- [ ] **RES.15** Python packaging and dependencies on Ubuntu 24.04: apt versus venv, pyproject layout [0.0]
- [ ] **RES.16** Apache hosting: mod_wsgi versus a proxy to gunicorn; which scripts stay CGI [0.0]
- [ ] **RES.17** Backup approach for MySQL, the git store and media (mysqldump, git bundle, rsync) [0.0]
- [ ] **RES.18** Accessibility checklist (WCAG 2.2 AA) for the UI [0.0]
- [ ] **RES.19** Import and export formats [0.0]

## TST: Testing and sample content

Issue: [#28](https://github.com/dwhagar/spakr/issues/28)

- [ ] **TST.1** Test harness: pytest fixtures for a temporary MySQL schema, git repository and Redis [0.1] — needs: FND.7, DB.2
- [ ] **TST.2** API test client and authentication helpers [0.4] — needs: TST.1, AUTH.2
- [ ] **TST.3** Sample content set across all entity types and the three settings (CC BY-SA), loadable by CLI [0.5] — needs: ENT.11, FND.9
- [ ] **TST.4** End-to-end smoke test: install, create admin, write, link, search, upload [0.9] — needs: UI.8, TST.3, OPS.7
