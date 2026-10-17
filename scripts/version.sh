#!/bin/sh
# Print the spakr version as MAJOR.MINOR.BUILD.
#
# MAJOR.MINOR come from the VERSION file and are changed by hand.
# BUILD is the number of first-parent commits on the current branch (main in
# practice) since the commit that last changed VERSION, so it counts up with
# every push to main and restarts at 0 when MAJOR or MINOR changes.
#
# Usage: scripts/version.sh            print the version
#        scripts/version.sh --write F  also write it to file F (for installs)
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
base=$(tr -d '[:space:]' < "$root/VERSION")
build=0
if git -C "$root" rev-parse --git-dir >/dev/null 2>&1; then
    stamp=$(git -C "$root" log --first-parent -1 --format=%H -- VERSION 2>/dev/null || true)
    if [ -n "$stamp" ]; then
        build=$(git -C "$root" rev-list --first-parent --count "$stamp..HEAD")
    fi
fi
version="$base.$build"
if [ "${1:-}" = "--write" ] && [ -n "${2:-}" ]; then
    printf '%s\n' "$version" > "$2"
fi
printf '%s\n' "$version"
