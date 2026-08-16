#!/usr/bin/env bash
# La regola architetturale di questo progetto è che src/domain/ non dipende da nulla.
# Un test la verifica dopo; questo hook la difende prima, con un messaggio che dice
# a Claude cosa fare invece.
set -uo pipefail

# stdin si legge UNA volta sola: due `jq` in pipeline sullo stesso stdin
# leggerebbero il secondo a vuoto.
IN=$(cat)

FILE=$(printf '%s' "$IN" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0

case "$FILE" in
  */src/domain/*.py) ;;
  *) exit 0 ;;
esac

CONTENUTO=$(printf '%s' "$IN" | jq -r '.tool_input.content // .tool_input.new_string // empty')
[ -z "$CONTENUTO" ] && exit 0

VIETATI="httpx|requests|anthropic|openai|chromadb|sqlalchemy|psycopg|fastapi|pydantic_settings|boto3"

if TROVATO=$(printf '%s' "$CONTENUTO" | grep -nE "^\s*(import|from)\s+($VIETATI)\b" | head -3); then
  jq -n --arg t "$TROVATO" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: ("src/domain/ non puo importare dipendenze esterne. Trovato:\n" + $t +
        "\n\nSe serve parlare con un servizio esterno: definisci un Protocol in src/domain/ports.py, " +
        "implementalo in src/adapters/, e registralo in src/config.py. Il dominio riceve la porta, mai la sua implementazione.")
    }
  }'
fi

exit 0
