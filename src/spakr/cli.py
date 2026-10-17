"""Command-line entry point: python -m spakr / spakr."""

import argparse
import sys

from spakr.config import ConfigError, load_settings
from spakr.version import software_version


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spakr")
    parser.add_argument("--config", help="path to config.json (default: $SPAKR_CONFIG, ./config.json, the application root, /etc/spakr/config.json)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version", help="print the software version")
    sub.add_parser("check-config", help="validate config.json and exit")
    sub.add_parser("db-version", help="print the applied and expected database schema versions")
    sub.add_parser("init-db", help="create the data folders and apply database migrations (back up first on a live site)")
    return parser


def _db_commands(args, settings) -> int:
    from sqlalchemy.exc import SQLAlchemyError

    from spakr.datadir import ensure_data_dirs
    from spakr.db import SCHEMA_VERSION, create_db_engine, get_schema_version
    from spakr.db.migrate import upgrade

    engine = create_db_engine(settings)
    try:
        if args.command == "init-db":
            ensure_data_dirs(settings)
            version = upgrade(engine)
            print(f"Database schema version {version} (expected {SCHEMA_VERSION}).")
        else:
            applied = get_schema_version(engine)
            print(f"applied: {applied if applied is not None else 'none'}")
            print(f"expected: {SCHEMA_VERSION}")
    except SQLAlchemyError as exc:
        reason = str(getattr(exc, "orig", None) or type(exc).__name__)
        raise ConfigError(f"Cannot use the database {settings.database.name!r}: {reason}") from None
    finally:
        engine.dispose()
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "version":
        print(software_version())
        return 0
    try:
        settings = load_settings(args.config)
        if args.command == "check-config":
            print(f"Configuration OK: {settings.source}")
            return 0
        return _db_commands(args, settings)
    except ConfigError as exc:
        print(f"spakr: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
