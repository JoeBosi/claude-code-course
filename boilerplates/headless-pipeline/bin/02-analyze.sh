#!/usr/bin/env bash
# Stadio 2 — analisi. L'UNICO stadio che chiama Claude.
# Legge data/raw/<data>.json, scrive data/out/<data>.json validato dallo schema.
set -euo pipefail

DATA="${1:-$(date +%F)}"
SRC="data/raw/${DATA}.json"
DEST="data/out/${DATA}.json"
CLAUDE="${CLAUDE_BIN:-$(command -v claude || true)}"

[ -f "$SRC" ]     || { echo "manca $SRC: esegui prima 01-fetch.sh" >&2; exit 1; }
[ -n "$CLAUDE" ]  || { echo "claude non trovato: imposta CLAUDE_BIN in .env" >&2; exit 2; }

# --bare      → risultato identico su ogni macchina
# --json-schema → l'output è dato, non prosa
# --max-turns → nessuno sta guardando
RISPOSTA=$("$CLAUDE" --bare -p "/analizza" \
  --output-format json \
  --json-schema "$(cat schemas/analisi.json)" \
  --max-turns 8 \
  < "$SRC") || { echo "claude non ha completato il run" >&2; exit 2; }

if ! printf '%s' "$RISPOSTA" | jq -e '.is_error == false' > /dev/null; then
  echo "run in errore:" >&2
  printf '%s' "$RISPOSTA" | jq -r '.result // "nessun dettaglio"' >&2
  exit 2
fi

NEGATI=$(printf '%s' "$RISPOSTA" | jq '.permission_denials | length')
[ "$NEGATI" -gt 0 ] && echo "attenzione: $NEGATI azioni negate dai permessi" >&2

# Come nello stadio 01: temporaneo, poi mv, per non lasciare output parziale.
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
printf '%s' "$RISPOSTA" | jq -e '.structured_output' > "$TMP"
mv "$TMP" "$DEST"
trap - EXIT
COSTO=$(printf '%s' "$RISPOSTA" | jq -r '.total_cost_usd')

echo "scritto $DEST · costo stimato ${COSTO} USD"
