#!/usr/bin/env bash
# Stadio 4 — pubblicazione. NESSUN LLM.
set -euo pipefail

DATA="${1:-$(date +%F)}"
SRC="data/out/${DATA}.md"

[ -f "$SRC" ] || { echo "manca $SRC: esegui prima 03-render.sh" >&2; exit 1; }

# ── Personalizza da qui ────────────────────────────────────────────────
# Scegli uno o più canali e cancella gli altri.

# Issue su GitHub
if command -v gh >/dev/null 2>&1 && [ -n "${PUBBLICA_SU_GITHUB:-}" ]; then
  gh issue create --title "Report $DATA" --body-file "$SRC"
fi

# Slack
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  jq -Rs '{text: .}' < "$SRC" \
    | curl -sf -X POST -H 'Content-Type: application/json' \
        -d @- "$SLACK_WEBHOOK_URL" > /dev/null
fi
# ── a qui ─────────────────────────────────────────────────────────────

echo "pubblicato $SRC"
