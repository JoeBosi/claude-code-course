#!/usr/bin/env bash
# Orchestratore. Chiama gli stadi in ordine, si ferma al primo che fallisce.
set -euo pipefail

RADICE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RADICE"

# cron ha un PATH minimo: .env riporta quello vero e il percorso di claude.
# shellcheck disable=SC1091
[ -f .env ] && . ./.env

DRY_RUN=0
DATA=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *)         DATA="$arg" ;;
  esac
done
[ -z "$DATA" ] && DATA=$(date +%F)

mkdir -p data/raw data/out logs
LOG="logs/${DATA}.log"

# Un solo run alla volta: se il precedente è ancora in corso, questo esce pulito.
LOCK="logs/.lock"
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date -u +%FT%TZ)  saltato: un altro run è in corso" >> "$LOG"
  exit 0
fi

log() { printf '%s  %s\n' "$(date -u +%FT%TZ)" "$1" | tee -a "$LOG"; }

stadio() {
  local script="$1"
  log "→ $script"
  if ! "bin/$script" "$DATA" >> "$LOG" 2>&1; then
    local codice=$?
    log "✘ $script fallito (exit $codice)"
    exit "$codice"
  fi
}

log "=== run $DATA ==="
stadio 01-fetch.sh
stadio 02-analyze.sh
stadio 03-render.sh

if [ "$DRY_RUN" -eq 1 ]; then
  log "dry-run: pubblicazione saltata"
else
  stadio 04-publish.sh
fi

log "✔ completato"
