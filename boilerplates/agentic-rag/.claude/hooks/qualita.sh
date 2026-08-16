#!/usr/bin/env bash
# Ruff e mypy dopo ogni modifica: gli errori tornano a Claude, che li corregge
# nello stesso turno invece che al prossimo commit.
set -uo pipefail

FILE=$(jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0
[ -f "$FILE" ] || exit 0

command -v uv >/dev/null 2>&1 || exit 0

uv run ruff format "$FILE" >/dev/null 2>&1 || true

PROBLEMI=""
if ! OUT=$(uv run ruff check "$FILE" 2>&1); then
  PROBLEMI="$OUT"
fi

if [ -z "$PROBLEMI" ]; then
  if ! OUT=$(uv run mypy "$FILE" 2>&1); then
    PROBLEMI=$(printf '%s' "$OUT" | head -25)
  fi
fi

if [ -n "$PROBLEMI" ]; then
  printf '%s\n' "$PROBLEMI" >&2
  exit 2
fi

exit 0
