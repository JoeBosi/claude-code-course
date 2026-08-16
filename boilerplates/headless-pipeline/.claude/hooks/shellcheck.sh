#!/usr/bin/env bash
# Ogni script della pipeline gira in cron senza nessuno che guardi:
# uno shellcheck fallito è un incidente delle 7 del mattino.
set -uo pipefail

FILE=$(jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0
[ -f "$FILE" ] || exit 0

command -v shellcheck >/dev/null 2>&1 || exit 0

if ! OUT=$(shellcheck -S warning "$FILE" 2>&1); then
  printf '%s\n' "$OUT" >&2
  exit 2
fi

exit 0
