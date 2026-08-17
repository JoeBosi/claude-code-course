#!/usr/bin/env bash
# Orchestratore. Chiama gli stadi in ordine, si ferma al primo che fallisce.
set -euo pipefail

# BASH_SOURCE[0] = il percorso di QUESTO script, comunque lo si invochi
# (./bin/run.sh, bash bin/run.sh, da cron...): risalendo di una cartella
# troviamo la radice del progetto, e ci spostiamo lì.
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
# exec 9> apre il file di lock sul "canale" numero 9 e lo tiene aperto per
# tutta la vita dello script; flock -n prova a mettere un lucchetto esclusivo
# su quel canale senza aspettare (-n = non bloccare: se è già preso, fallisci
# subito). Il lucchetto si libera da solo quando lo script termina, comunque
# termini: è il modo robusto di dire "un'istanza sola".
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
  # Esegui lo stadio e cattura il suo exit code SENZA negazioni di mezzo:
  # dentro un "if ! cmd", $? vale l'esito del costrutto negato (sempre 0),
  # non quello di cmd — un bug classico che qui farebbe uscire l'orchestratore
  # con successo anche a stadio fallito. Il "|| codice=$?" evita anche che
  # set -e uccida lo script prima di poter loggare.
  local codice=0
  "bin/$script" "$DATA" >> "$LOG" 2>&1 || codice=$?
  if [ "$codice" -ne 0 ]; then
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
