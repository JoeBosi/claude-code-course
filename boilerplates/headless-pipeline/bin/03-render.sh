#!/usr/bin/env bash
# Stadio 3 — resa in markdown. NESSUN LLM: formattare non richiede giudizio.
set -euo pipefail

DATA="${1:-$(date +%F)}"
SRC="data/out/${DATA}.json"
DEST="data/out/${DATA}.md"

[ -f "$SRC" ] || { echo "manca $SRC: esegui prima 02-analyze.sh" >&2; exit 1; }

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
