# Changelog

All notable changes to spakr are recorded here, newest first. Versions are `MAJOR.MINOR.BUILD`; BUILD counts up with every push to `main` (see [`scripts/version.sh`](scripts/version.sh)), so entries are written per MAJOR.MINOR tier and name the TODO ids they close. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
