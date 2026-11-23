#!/bin/sh
# Before an edit to anything in tests/, block it with exit code 2. Claude reads the message and has to ask you.
if grep -q '"file_path": *"[^"]*/tests/'; then
  echo "Don't change a test without asking. Say which test, and why the ticket needs the change." >&2
  exit 2
fi
