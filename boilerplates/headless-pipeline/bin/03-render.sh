#!/usr/bin/env bash
# Stadio 3 — resa in markdown. NESSUN LLM: formattare non richiede giudizio.
set -euo pipefail

DATA="${1:-$(date +%F)}"
SRC="data/out/${DATA}.json"
DEST="data/out/${DATA}.md"
mkdir -p "$(dirname "$DEST")"   # ogni stadio è eseguibile da solo, anche senza run.sh

[ -f "$SRC" ] || { echo "manca $SRC: esegui prima 02-analyze.sh" >&2; exit 1; }

# I campi letti qui sotto (.titolo, .sintesi, .temi[], .rilievi[]...) sono
# ESATTAMENTE quelli garantiti da schemas/analisi.json: lo schema è il
# contratto tra lo stadio 02 e questo. Se cambi lo schema, cambia il renderer.
jq -r '
  "# \(.titolo)\n",
  "\(.sintesi)\n",
  (if (.temi | length) > 0 then
    "## Temi\n" +
    ([.temi[] | "### \(.tema)\n\n\(.cosa)\n\nRiferimenti: \(.riferimenti | join(", "))\n"] | join("\n"))
   else "" end),
  (if (.rilievi | length) > 0 then
    "## Rilievi\n" +
    ([.rilievi[] |
      "- **[\(.gravita)]** \(.rilievo)\n  - prova: \(.prova)\n  - azione: \(.azione)"
     ] | join("\n"))
   else "## Rilievi\n\nNessuno." end)
' "$SRC" > "$DEST"

echo "scritto $DEST"
