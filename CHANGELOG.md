# Changelog

All notable changes to spakr are recorded here, newest first. Versions are `MAJOR.MINOR.BUILD`; BUILD counts up with every push to `main` (see [`scripts/version.sh`](scripts/version.sh)), so entries are written per MAJOR.MINOR tier and name the TODO ids they close. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Database layer (DB.1, DB.5, first part of DB.2): `spakr.db` with a SQLAlchemy engine (MySQL through PyMySQL, utf8mb4, optional unix socket), Alembic migrations 0001 (schema version, config, users, roles and permissions with seeds, settings, audit log) and 0002 (pages, aliases, revisions, tags, relation kinds, relations, links), and an integer schema version in the `schema_version` table that counts up with every migration (`get_schema_version`, `SCHEMA_VERSION`, `schema_status`). `spakr init-db` creates the data folders and applies migrations; `spakr db-version` prints applied and expected versions. Tests run on SQLite always and on MySQL 8 when `SPAKR_TEST_DATABASE_URL` is set (the daily workflow starts a MySQL service).
- Flask API skeleton (API.1, API.7, FND.4): app factory `spakr.api.create_app()` and `spakr/wsgi.py` for Apache mod_wsgi (daemon mode, pass-authorization on); `GET /api/v1/health` reports status, configuration state, the software version (MAJOR.MINOR.BUILD), the integer API version and the database schema version (`unknown` until the database layer lands); a missing or invalid `config.json` leaves the app running, health says `not_configured` (HTTP 503) and every other route answers a 503 problem. All errors are `application/problem+json` with a request id (`X-Request-ID`); every response carries `X-API-Version`; JSON-lines logging to stderr without query strings; OpenAPI served at `/api/v1/openapi.json`. The API version is one constant (`spakr/api/versions.py`); a test fails if the generated OpenAPI description differs from `tests/api_contract.snapshot` or changes without a higher version than main. Shared outbound User-Agent helper `spakr/outbound.py` (`spakr/<version> spakr-api/<n> (+contact)`).
- Python package skeleton in `src/spakr` with `pyproject.toml` (Python 3.12 or newer, start-up error otherwise), data paths under `/data` (`SPAKR_DATA_DIR` and `SPAKR_CONFIG` overrides), the software version helper and the first tests (FND.1, FND.10).
- Package skeleton and config loader (FND.1, FND.2, CFG.3): `src/spakr` package for Python 3.12, `pyproject.toml`, frozen settings objects with a `Secret` wrapper, `python -m spakr check-config|version`. A missing or invalid `config.json` ends with a clear message and exit status 2, never a traceback. `paths.data_dir` (default `/data`, git-ignored; `SPAKR_DATA_DIR` overrides it for tests) holds all runtime data.
- Platform and security research (RES.5, RES.6, RES.9, RES.12, RES.14, RES.15, RES.16, RES.17, RES.18, RES.20 done) as pages under `docs/research`, with experiments run on Ubuntu 24.04: Flask, pydantic and argon2 under apt mod_wsgi, file-type sniffing, an OpenAPI spike and atomic `config.json` rewrites under contention. Plus a platform conventions page (queue, logging, MySQL, outbound HTTP, testing and CI, privacy).
- New suggested items: AUTH.12 (user data export), MED.9 (optional ClamAV scan), MED.10 (captions and transcripts), DOC.7 (privacy page).

### Changed
- Decisions for the first build: Python 3.12 required (FND.10); integer database and API versions that count up on every change (DB.5, API.7), reported with the software version by the health and status endpoint (API.8); all data under git-ignored `/data` (FND.11); graceful failure without a config file (CFG.8). `/data/` added to `.gitignore`; config example paths moved under `data`.
- Web UI layer research added for Research C: RES.21 to RES.24 (CSS and design system, Node.js justification, device range from phone and foldable to TV, component approach) and UI.15 (TV and foldable layouts), UI.16 (device test matrix); UI.1, UI.11, UI.12 and UI.13 now need the matching research.
- Assumption recorded: Apache2 handles TLS and a valid domain certificate is in place; no certificate handling in the app. Added API.6 (trust Apache HTTPS signal, Secure and __Host- cookies, HSTS only if the admin enables it).
- CSRF design is a synchronizer token tied to the server session plus a Fetch Metadata check, replacing the double-submit token (RES.5, AUTH.2); invitation and reset tokens travel in the URL fragment and are consumed by a POST (AUTH.4, AUTH.5); API keys cannot manage keys or account security (AUTH.6).
- Hosting: apt mod_wsgi in daemon mode must set `WSGIPassAuthorization On` or the app never sees `Authorization: Bearer` (verified), plus `WSGIApplicationGroup %{GLOBAL}` (FND.3, FND.6).
- Packaging: Python libraries come from a hashed virtualenv lock, not apt (24.04 ships SQLAlchemy 1.4 and pydantic 1.10); PyMySQL (MIT) is the MySQL driver instead of the GPL mysqlclient (FND.1, DB.1).
- Backups become one `spakr backup` / `spakr restore` command pair (OPS.5, FND.9); the daily CI run opens an issue when it fails (FND.7); API validation and OpenAPI use pydantic v2 with SpecTree (API.3).
- Git commits use a pseudonymous per-account identity so history never holds personal data (GIT.1, conventions page).

### Changed
- Decided: the app rewrites `config.json` atomically at mode 0600; secret fields are write-only in the UI. RES.20 now only confirms implementation details (CFG.5).
- Email goes through an external SMTP relay, never a local MTA; relay settings and sender address are configuration (MAIL.1 unblocked, RES.6 reworded).
- Media: ffmpeg and ImageMagick are the preferred tools; Python libraries allowed where measurably better (RES.10, MED.4).
- Config: secrets live in `config.json`, everything is editable in the web interface except the MySQL credentials. Admin settings API (AUTH.8) never returns secrets.

### Added
- CFG category (CFG.1 to CFG.7): config example, settings registry, manual-only MySQL credentials, settings store, secrets handling, live reload, admin settings screens. RES.20 (settings and secrets approach) and MAIL.3 (email settings with test message).

### Added
- Standing requirement: every screen is responsive and has light and dark modes from the start. Foundation items UI.11 (responsive layout base), UI.12 (light/dark theme tokens with a user toggle), UI.13 (acceptance checklist for every UI item), UI.14 (themed tables, code and media players), and DOC.6 (plan pages responsive with dark mode, done). Later UI items now need UI.13.

### Changed
- Plan reworked as a dependency tree: 140 TODO items, each naming the ids it needs, in phases 0.0 to 0.9 matched to version numbers. 0.9 is now the pre-release working version; 0.1 to 0.8 are building blocks; 1.0 is the release (DOC.1).
- Preview endpoint (RND.6) moved to phase 0.5 because it needs the permission decorator.

### Added
- Phase 0.0 research items RES.1 to RES.19 for open library and approach choices (math, MultiMarkdown, sanitiser, git access, email, search, SEO, uploads, front end, rate limiting, entity fields, OpenAPI, packaging, hosting, backups, accessibility, import/export).
- TST category (test harness, API test client, sample content, end-to-end smoke test) and items FND.9, AUTH.11, ENT.13, LNK.7, UI.10.
- `docs/plan/tree.html` with a phase ladder and item tree.

### Changed
- Relation types are a fixed, admin-managed vocabulary (`relation_kind` table), not free-form labels; added LNK.6 for its admin API (LNK.3).

## [0.0.0] - 2026-10-17

First stamped version. Planning and process only; there is no application code yet.

### Added
- Project plan in `docs/plan`, database design, media research, licences (MIT code, CC BY-SA 4.0 content) and `COPYRIGHT.md`.
- `TODO.md` with items numbered `[CAT].[NUMBER]`, one GitHub issue per category (REL.2).
- This changelog.
- `VERSION` and `scripts/version.sh` for MAJOR.MINOR.BUILD stamping (REL.1).
- Issue templates for bugs and suggestions (REL.3).
- Plan rewritten as tiers 0.0 to 0.9 listing their TODO ids (DOC.1).
- Content search planned with a full page index and search fields; `page_search` redesigned (SEARCH.1).
- Daily 07:00 UTC test workflow (no push or pull request triggers).
