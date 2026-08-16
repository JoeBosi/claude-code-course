#!/usr/bin/env bash
# Dopo ogni modifica a TypeScript: formatta, poi riporta a Claude cosa non va.
set -uo pipefail

FILE=$(jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0
[ -f "$FILE" ] || exit 0

npx --no-install prettier --write "$FILE" >/dev/null 2>&1 || true

PROBLEMI=""

if ! OUT=$(npx --no-install eslint "$FILE" 2>&1); then
  PROBLEMI="$OUT"
fi

# Il typecheck è di progetto, non per file: lo lanciamo solo se il lint è pulito,
# per non sommare due muri di output nello stesso turno.
if [ -z "$PROBLEMI" ]; then
  if ! OUT=$(npx --no-install tsc --noEmit 2>&1); then
    PROBLEMI=$(printf '%s' "$OUT" | head -30)
  fi
fi

if [ -n "$PROBLEMI" ]; then
  printf '%s\n' "$PROBLEMI" >&2
  exit 2
fi

exit 0
