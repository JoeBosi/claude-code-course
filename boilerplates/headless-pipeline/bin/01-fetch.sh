#!/usr/bin/env bash
# Stadio 1 — raccolta. NESSUN LLM: solo comandi deterministici.
# Scrive data/raw/<data>.json e non tocca nient'altro.
set -euo pipefail

DATA="${1:-$(date +%F)}"
DEST="data/raw/${DATA}.json"

if [ -f "$DEST" ]; then
  echo "raw già presente per $DATA, non lo sovrascrivo (data/raw è immutabile)"
  exit 0
fi

# ── Personalizza da qui ────────────────────────────────────────────────
# Sostituisci con le tue fonti reali. Ogni fonte diventa una chiave del JSON.
# Esempi:
#   curl -sf "$API_URL/metrics?date=$DATA"
#   gh issue list --state open --json number,title,createdAt
#   psql "$DATABASE_URL_RO" -Atc "select ..." | jq -R -s 'split("\n")'

# git log con separatore di unità: jq costruisce il JSON, così i caratteri
# speciali nei messaggi di commit non rompono nulla.
COMMIT=$(git log --since="$DATA 00:00" --until="$DATA 23:59" \
           --pretty=format:'%h%x1f%s%x1f%an' 2>/dev/null \
         | jq -R -s 'split("\n") | map(select(length > 0) | split("\u001f")
             | {sha: .[0], msg: .[1], autore: .[2]})' 2>/dev/null || echo '[]')
# ── a qui ─────────────────────────────────────────────────────────────

# Scrivi su temporaneo e sposta solo a comando riuscito: una redirezione
# diretta lascerebbe un file vuoto se jq fallisce, e il run successivo lo
# scambierebbe per dati già raccolti.
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

jq -n --arg data "$DATA" --argjson commit "$COMMIT" '{
  data: $data,
  raccolto_il: (now | todate),
  commit: $commit
}' > "$TMP"

[ -s "$TMP" ] || { echo "raccolta vuota, non scrivo $DEST" >&2; exit 1; }
mv "$TMP" "$DEST"
trap - EXIT

echo "scritto $DEST ($(wc -c < "$DEST") byte)"
