#!/usr/bin/env bash
# Inietta all'avvio lo stato reale della pipeline: senza, Claude
# chiede o peggio inventa.
set -uo pipefail

cd "$(dirname "$0")/../.." || exit 0

ULTIMO_RAW=$(ls -1 data/raw/*.json 2>/dev/null | tail -1 | xargs -r basename)
ULTIMO_OUT=$(ls -1 data/out/*.json 2>/dev/null | tail -1 | xargs -r basename)
ULTIMO_LOG=$(ls -1t logs/*.log 2>/dev/null | head -1)
ESITO="nessun run registrato"
[ -n "$ULTIMO_LOG" ] && ESITO=$(tail -1 "$ULTIMO_LOG" 2>/dev/null | head -c 200)

jq -n \
  --arg raw "${ULTIMO_RAW:-nessuno}" \
  --arg out "${ULTIMO_OUT:-nessuno}" \
  --arg esito "$ESITO" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: ("Stato pipeline — ultimo raw: " + $raw +
                        " · ultimo output: " + $out +
                        " · ultima riga di log: " + $esito)
  }
}'
