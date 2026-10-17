# Changelog

All notable changes to spakr are recorded here, newest first. Versions are `MAJOR.MINOR.BUILD`; BUILD counts up with every push to `main` (see [`scripts/version.sh`](scripts/version.sh)), so entries are written per MAJOR.MINOR tier and name the TODO ids they close. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
