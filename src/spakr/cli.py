"""Command-line entry point: python -m spakr / spakr."""

import argparse
import sys

from spakr.version import software_version
from spakr.config import ConfigError, load_settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spakr")
    parser.add_argument("--config", help="path to config.json (default: $SPAKR_CONFIG, ./config.json, /etc/spakr/config.json)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version", help="print the software version")
    sub.add_parser("check-config", help="validate config.json and exit")
    return parser


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
    except ConfigError as exc:
        print(f"spakr: configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
