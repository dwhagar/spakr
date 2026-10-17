# TODO

Current version: **0.0.0** (see [`VERSION`](VERSION) and [`scripts/version.sh`](scripts/version.sh)).

Items are numbered `[CAT].[NUMBER]`, for example `API.1`. Each category is a GitHub issue that holds the same checklist; bugs and suggestions arrive as their own issues and are folded in here when accepted. Numbers are never reused. The tier (version) each item belongs to is in brackets; the tiers are described in [`docs/plan/tiers.html`](docs/plan/tiers.html).

This file is kept by the TODO thread. To change the plan, change this file and the matching issue together.


## REL: Release, versioning and process

Issue: [#8](https://github.com/dwhagar/spakr/issues/8)

- [x] **REL.1** Version file and build-number script (scripts/version.sh) [0.0]
- [x] **REL.2** TODO.md, CHANGELOG.md and category issues created and linked [0.0]
- [x] **REL.3** Issue templates for bugs and suggestions [0.0]
- [ ] **REL.4** Script to check TODO.md against GitHub issues (scripts/todo-sync) [0.1]
- [ ] **REL.5** Expose the version in the app: /api/v1/version, page footer, outbound User-Agent [0.1]
- [ ] **REL.6** Release checklist and 1.0 tagging [0.9]

## DOC: Documentation

Issue: [#9](https://github.com/dwhagar/spakr/issues/9)

- [x] **DOC.1** Plan rewritten as tiers 0.0 to 0.9 with TODO ids [0.0]
- [ ] **DOC.2** Enable GitHub Pages from /docs (owner action in repository settings) [0.0]
- [ ] **DOC.3** Admin install and upgrade guide [0.9]
- [ ] **DOC.4** Editor guide: writing pages, links, media syntax, visibility [0.9]
- [ ] **DOC.5** API reference generated from the OpenAPI description [0.9]

## FND: Foundation

Issue: [#10](https://github.com/dwhagar/spakr/issues/10)

- [ ] **FND.1** Python package skeleton in src/ with pyproject and pinned dependencies [0.1]
- [ ] **FND.2** JSON configuration loader with validation against examples/spakr.conf.example [0.1]
- [ ] **FND.3** WSGI entry point and the small CGI shim [0.1]
- [ ] **FND.4** Shared outbound HTTP helper with the required User-Agent (software, version, API version) [0.1]
- [ ] **FND.5** Dev setup script for Ubuntu 24.04 [0.1]
- [ ] **FND.6** Apache vhost and systemd unit examples in examples/ [0.1]
- [ ] **FND.7** Lint, format and test tooling; tests workflow stays on the 07:00 UTC schedule only [0.1]
- [ ] **FND.8** Structured logging [0.1]

## API: API (Flask, /api/v1)

Issue: [#11](https://github.com/dwhagar/spakr/issues/11)

- [ ] **API.1** Flask app factory and /api/v1 skeleton with health endpoint [0.1]
- [ ] **API.2** Error format, pagination and filtering conventions [0.1]
- [ ] **API.3** OpenAPI description kept in step with the routes [0.1]
- [ ] **API.4** Permission decorator used by every route (session or API key) [0.4]
- [ ] **API.5** Generic CRUD helpers for page-backed resources [0.5]

## DB: Database

Issue: [#12](https://github.com/dwhagar/spakr/issues/12)

- [ ] **DB.1** SQLAlchemy engine and session setup [0.1]
- [ ] **DB.2** Alembic migrations creating the schema in docs/design/database.html [0.1]
- [ ] **DB.3** Command to rebuild the MySQL index from the git content store [0.2]
- [ ] **DB.4** Database backup and restore script [0.9]

## QUE: Task queue

Issue: [#13](https://github.com/dwhagar/spakr/issues/13)

- [ ] **QUE.1** Redis connection and RQ configuration [0.1]
- [ ] **QUE.2** Worker process and systemd unit [0.1]
- [ ] **QUE.3** Task status API [0.7]
- [ ] **QUE.4** Reindex and cache-warm jobs [0.7]

## GIT: Git-backed content store

Issue: [#14](https://github.com/dwhagar/spakr/issues/14)

- [ ] **GIT.1** Repository initialisation, commit author mapping and write locking [0.2]
- [ ] **GIT.2** Create, read and update a page (Markdown with front matter) [0.2]
- [ ] **GIT.3** Page history and diff [0.2]
- [ ] **GIT.4** Revert to an earlier revision [0.2]
- [ ] **GIT.5** MySQL page index kept in step on every write [0.2]
- [ ] **GIT.6** Slug rules, rename and move [0.2]
- [ ] **GIT.7** Edit conflict detection based on the base commit [0.2]

## RND: Rendering and sanitising

Issue: [#15](https://github.com/dwhagar/spakr/issues/15)

- [ ] **RND.1** MultiMarkdown rendering [0.3]
- [ ] **RND.2** LaTeX math rendered server-side to static markup [0.3]
- [ ] **RND.3** HTML sanitiser with the admin-approved allowlist [0.3]
- [ ] **RND.4** Strict Content-Security-Policy and security headers (no inline script or style) [0.3]
- [ ] **RND.5** Rendered-page cache keyed by revision [0.3]
- [ ] **RND.6** Preview endpoint [0.3]

## AUTH: Accounts, roles and API keys

Issue: [#16](https://github.com/dwhagar/spakr/issues/16)

- [ ] **AUTH.1** Users and password hashing [0.4]
- [ ] **AUTH.2** Login, logout, cookie sessions and CSRF header [0.4]
- [ ] **AUTH.3** Roles and permissions: reader, editor, GM, mod, admin [0.4]
- [ ] **AUTH.4** Invitation flow (7-day tokens) [0.4]
- [ ] **AUTH.5** Password reset flow (1-hour tokens) [0.4]
- [ ] **AUTH.6** API keys: users limited to their own permissions, admins unlimited, per-user cap [0.4]
- [ ] **AUTH.7** Audit log [0.4]
- [ ] **AUTH.8** Admin settings API [0.4]
- [ ] **AUTH.9** HTML allowlist approval API [0.4]
- [ ] **AUTH.10** Account editing API (profile, email, password, roles) [0.4]

## MAIL: Email

Issue: [#17](https://github.com/dwhagar/spakr/issues/17)

- [ ] **MAIL.1** SMTP sender through the local MTA or a configured relay (blocked on the open SMTP question) [0.4]
- [ ] **MAIL.2** Invitation and password-reset templates, sent via the queue [0.4]

## VIS: Page visibility

Issue: [#18](https://github.com/dwhagar/spakr/issues/18)

- [ ] **VIS.1** Public or GM-only flag per page, with the reserved visibility-group column [0.4]
- [ ] **VIS.2** One central query filter enforcing visibility everywhere [0.4]
- [ ] **VIS.3** Leak tests: views, search, links, backlinks, history and downloads [0.6]

## ENT: Entity types

Issue: [#19](https://github.com/dwhagar/spakr/issues/19)

- [ ] **ENT.1** Entity type registry and structured field definitions [0.5]
- [ ] **ENT.2** Characters [0.5]
- [ ] **ENT.3** Items and technology [0.5]
- [ ] **ENT.4** Places [0.5]
- [ ] **ENT.5** Magic and psionics [0.5]
- [ ] **ENT.6** Abilities [0.5]
- [ ] **ENT.7** Skills [0.5]
- [ ] **ENT.8** Entities (creatures and beings) [0.5]
- [ ] **ENT.9** Races [0.5]
- [ ] **ENT.10** Nation-states [0.5]
- [ ] **ENT.11** Free pages [0.5]
- [ ] **ENT.12** Settings as tags (high fantasy, modern/cosmic horror, scifi) [0.5]

## LNK: Links, relations and browsing

Issue: [#20](https://github.com/dwhagar/spakr/issues/20)

- [ ] **LNK.1** Wiki-style links between pages [0.6]
- [ ] **LNK.2** Backlinks [0.6]
- [ ] **LNK.3** Relations between pages (needs the relation-vocabulary decision) [0.6]
- [ ] **LNK.4** Browse by type and setting [0.6]
- [ ] **LNK.5** Tags [0.6]

## SEARCH: Content search, SEO and caching

Issue: [#21](https://github.com/dwhagar/spakr/issues/21)

- [x] **SEARCH.1** Reconcile the page_search design in docs/design/database.html (type, summary, name/aliases, tags, settings, field text, indexes) [0.0]
- [ ] **SEARCH.2** Search document builder: plain text of the Markdown plus title, summary, aliases, tags, settings and type-field text, written on every page save [0.2]
- [ ] **SEARCH.3** Full-text query endpoint over the full page index: natural and boolean modes, relevance ranking, highlighted snippets, pagination [0.6]
- [ ] **SEARCH.4** Field search: type, setting, tag, name/title and type-specific fields (for example race, place, occupation) as API parameters and query syntax such as type:character setting:scifi tag:undead [0.6]
- [ ] **SEARCH.5** Filters and facet counts by type, setting and tag [0.6]
- [ ] **SEARCH.6** Visibility in search: GM-only pages excluded for users without the GM role, using the copied visibility column [0.6]
- [ ] **SEARCH.7** Name and alias autocomplete for search-as-you-type and the link picker [0.6]
- [ ] **SEARCH.8** Tokeniser decision: InnoDB default parser or ngram, minimum token size and stopword settings, set by the admin [0.6]
- [ ] **SEARCH.9** SEO metadata, sitemap.xml and robots.txt [0.6]
- [ ] **SEARCH.10** Memory (Redis, per-process) and disk caches for rendered pages [0.6]

## MED: Uploads and media

Issue: [#22](https://github.com/dwhagar/spakr/issues/22)

- [ ] **MED.1** Upload endpoint: type sniffing, size limits (10 MB, 100 MB video), safe-list [0.7]
- [ ] **MED.2** Quarantine and admin override [0.7]
- [ ] **MED.3** Hashed media directories; originals kept privately [0.7]
- [ ] **MED.4** Image processing with ImageMagick as queue tasks [0.7]
- [ ] **MED.5** Video and audio transcoding with ffmpeg as queue tasks [0.7]
- [ ] **MED.6** Gated thumbnail series, never enlarged [0.7]
- [ ] **MED.7** media: Markdown syntax and HTML5 players [0.7]
- [ ] **MED.8** Admin purge of originals [0.7]

## UI: Web UI (first-party JavaScript client)

Issue: [#23](https://github.com/dwhagar/spakr/issues/23)

- [ ] **UI.1** JavaScript client scaffold, served from our origin with hashed assets [0.1]
- [ ] **UI.2** Server-rendered public reading pages with SEO markup [0.8]
- [ ] **UI.3** Login, invitation and account screens [0.8]
- [ ] **UI.4** Page editor with preview [0.8]
- [ ] **UI.5** History, diff and revert screens [0.8]
- [ ] **UI.6** Browse and search screens [0.8]
- [ ] **UI.7** Admin screens: settings, allowlist, users, API keys [0.8]
- [ ] **UI.8** Upload and media screens [0.8]
- [ ] **UI.9** Licence statement in the footer and on edit/upload pages [0.8]

## OPS: Hardening and operations

Issue: [#24](https://github.com/dwhagar/spakr/issues/24)

- [ ] **OPS.1** Security review [0.9]
- [ ] **OPS.2** Rate limiting [0.9]
- [ ] **OPS.3** Error pages [0.9]
- [ ] **OPS.4** Accessibility pass [0.9]
- [ ] **OPS.5** Backup script covering git store, MySQL and media [0.9]
- [ ] **OPS.6** Import and export [0.9]
- [ ] **OPS.7** Clean-install test on Ubuntu 24.04; best-effort pass on 26.04 [0.9]
