#!/usr/bin/env bash
# Stadio 1 — raccolta. NESSUN LLM: solo comandi deterministici.
# Scrive data/raw/<data>.json e non tocca nient'altro.
set -euo pipefail

DATA="${1:-$(date +%F)}"
DEST="data/raw/${DATA}.json"
mkdir -p "$(dirname "$DEST")"   # ogni stadio è eseguibile da solo, anche senza run.sh

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

# git log con "separatore di unità": %x1f è un carattere di controllo che non
# può comparire in un messaggio di commit, quindi è un separatore sicuro tra
# i campi (sha, messaggio, autore). jq poi ricostruisce il JSON da quelle
# righe, così virgolette e caratteri speciali nei messaggi non rompono nulla.
# NOTA i due fallback "|| COMMIT='[]'" sotto: se git o jq falliscono (es. non
# siamo in un repository), la raccolta prosegue con una lista vuota invece di
# fermarsi. Il fallback sta FUORI dalla command substitution di proposito:
# un "|| echo '[]'" dentro le parentesi, con pipefail, può sommarsi all'output
# già stampato da jq e produrre JSON invalido ("[]" due volte). Comodo per il
# template, ma un fallback così MASCHERA gli errori: con le tue fonti reali
# valuta se un fallimento debba invece far uscire lo stadio con exit 1.
COMMIT=$(git log --since="$DATA 00:00" --until="$DATA 23:59" \
           --pretty=format:'%h%x1f%s%x1f%an' 2>/dev/null \
         | jq -R -s 'split("\n") | map(select(length > 0) | split("\u001f")
             | {sha: .[0], msg: .[1], autore: .[2]})' 2>/dev/null) || COMMIT='[]'
[ -n "$COMMIT" ] || COMMIT='[]'
# ── a qui ─────────────────────────────────────────────────────────────

# Scrivi su temporaneo e sposta solo a comando riuscito: una redirezione
# diretta lascerebbe un file vuoto se jq fallisce, e il run successivo lo
# scambierebbe per dati già raccolti.
#   mktemp        = crea un file temporaneo vuoto e ne stampa il percorso
#   trap ... EXIT = "quando lo script esce, COMUNQUE esca, cancella il
#                   temporaneo": così un errore a metà non lascia residui
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
