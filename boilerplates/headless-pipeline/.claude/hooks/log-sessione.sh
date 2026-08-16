#!/usr/bin/env bash
# Traccia le sessioni su questa pipeline: quando qualcosa si rompe in
# produzione, sapere chi ha toccato cosa e quando vale il costo di due righe.
set -uo pipefail

cd "$(dirname "$0")/../.." || exit 0
mkdir -p logs

IN=$(cat)
SID=$(printf '%s' "$IN" | jq -r '.session_id // "sconosciuta"')
MOTIVO=$(printf '%s' "$IN" | jq -r '.end_reason // "sconosciuto"')

printf '%s  sessione=%s  fine=%s\n' \
  "$(date -u +%FT%TZ)" "$SID" "$MOTIVO" >> logs/sessioni.log
