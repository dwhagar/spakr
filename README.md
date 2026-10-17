# spakr
A free form game and story database for characters, technology, places, and all other game information, covering three settings: high fantasy, modern / cosmic horror, and science fiction.

**Status:** planning, version 0.0.0. No application code yet. Work items are in [`TODO.md`](TODO.md), history in [`CHANGELOG.md`](CHANGELOG.md). Target for 1.0 is a working, functional, usable web site.

## Layout
| Path | Purpose |
|---|---|
| `src/` | All source code |
| `src/html/` | Web site code |
| `docs/` | All documents (published with GitHub Pages from `/docs`) |
| `docs/archive/` | Old docs |
| `docs/research/` | Research docs |
| `docs/design/` | Design docs |
| `docs/plan/` | The plan, as HTML, in tiers with version numbers |
| `TODO.md`, `CHANGELOG.md`, `VERSION` | Work items `[CAT].[NUMBER]`, change history, MAJOR.MINOR |
| `examples/` | Configuration and service examples (Apache vhost, systemd units) |
| `scripts/` | Maintenance scripts (`version.sh` prints `MAJOR.MINOR.BUILD`) |

All `*.json` files are git-ignored because they hold configuration. Commit `*.example` files instead.

## Licence
Code: MIT ([`LICENSE`](LICENSE)). Game content: CC BY-SA 4.0 ([`CONTENT-LICENSE.md`](CONTENT-LICENSE.md)). Copyright notice and removal requests: [`COPYRIGHT.md`](COPYRIGHT.md).

## Plan
Start at [`docs/plan/index.html`](docs/plan/index.html). Once GitHub Pages is enabled (Settings, Pages, deploy from branch, folder `/docs`) it is served at `/plan/`.
