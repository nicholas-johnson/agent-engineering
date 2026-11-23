#!/bin/sh
# After every edit, run the tests. If any fail, exit with 2, which shows Claude the failures so it fixes them first.
cd "$CLAUDE_PROJECT_DIR" || exit 0
if ! result=$(python3 -m unittest 2>&1); then
  echo "$result" | tail -15 >&2
  exit 2
fi
