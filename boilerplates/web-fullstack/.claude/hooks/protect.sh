#!/usr/bin/env bash
# Blocca le modifiche a file che non devono essere toccati da un agente.
set -uo pipefail

FILE=$(jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0

nega() {
  jq -n --arg m "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $m
    }
  }'
  exit 0
}

case "$FILE" in
  */src/db/migrations/*)
    nega "Le migrazioni applicate non si modificano. Modifica src/db/schema.ts e lancia \`npm run db:generate\` per creare una migrazione nuova." ;;
  *.env|*.env.local|*.env.production)
    nega "I file di ambiente non si modificano da qui. Aggiungi la variabile a .env.example e a src/lib/env.ts, e chiedi all'utente di impostarla." ;;
  */package-lock.json)
    nega "Il lockfile si aggiorna solo con npm. Non modificarlo a mano." ;;
esac

exit 0
