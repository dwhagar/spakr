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
| `docs/plan/` | The plan, as HTML, as phases matched to version numbers (0.0 to 0.9, then 1.0) with a dependency tree |
| `TODO.md`, `CHANGELOG.md`, `VERSION` | Work items `[CAT].[NUMBER]`, change history, MAJOR.MINOR |
| `examples/` | Configuration and service examples (Apache vhost, systemd units) |
| `scripts/` | Maintenance scripts (`version.sh` prints `MAJOR.MINOR.BUILD`) |

All `*.json` files are git-ignored because they hold configuration. Commit `*.example` files instead.

## Licence
Code: MIT ([`LICENSE`](LICENSE)). Game content: CC BY-SA 4.0 ([`CONTENT-LICENSE.md`](CONTENT-LICENSE.md)). Copyright notice and removal requests: [`COPYRIGHT.md`](COPYRIGHT.md).

## Plan
Start at [`docs/plan/index.html`](docs/plan/index.html). Once GitHub Pages is enabled (Settings, Pages, deploy from branch, folder `/docs`) it is served at `/plan/`.

## Development

Requires **Python 3.12** or newer.

```sh
python3.12 -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
python -m pytest
```

Copy `examples/config.json.example` to `config.json` (mode 0600) and fill in the database section. All runtime data lives under `/data` (git-ignored; set `SPAKR_DATA_DIR` or `paths.data_dir` to move it, for example in tests). `python -m spakr check-config` validates the file, `python -m spakr init-db` creates the data folders and applies the database migrations, and `python -m spakr db-version` shows the applied and expected schema versions. To run the database tests against MySQL as well, point `SPAKR_TEST_DATABASE_URL` at a throwaway schema (every table in it is dropped), for example `mysql+pymysql://user:pw@127.0.0.1/spakr_test`.
