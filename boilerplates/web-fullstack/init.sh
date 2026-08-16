#!/usr/bin/env bash
# Personalizza il boilerplate: sostituisce i segnaposto e rimuove sé stesso.
set -euo pipefail

NOME="${1:-}"
DESCR="${2:-}"

if [ -z "$NOME" ]; then
  echo "Uso: ./init.sh <nome-progetto> [descrizione]" >&2
  exit 1
fi
[ -z "$DESCR" ] && DESCR="$NOME"

mapfile -t FILE < <(grep -rl '{{PROJECT_NAME}}\|{{PROJECT_DESCRIPTION}}' . \
  --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null || true)

for f in "${FILE[@]}"; do
  sed -i.bak \
    -e "s|{{PROJECT_NAME}}|$NOME|g" \
    -e "s|{{PROJECT_DESCRIPTION}}|$DESCR|g" "$f"
  rm -f "$f.bak"
  echo "  aggiornato  $f"
done

sed -i.bak "s|^Ultimo aggiornamento: —|Ultimo aggiornamento: $(date +%F)|" STATE.md && rm -f STATE.md.bak

if [ ! -d .git ]; then
  git init -q
  echo "  git init"
fi

echo
echo "✔ Progetto '$NOME' inizializzato."
echo
echo "Prossimi passi:"
echo "  1. npm install"
echo "  2. cp .env.example .env.local  e riempilo"
echo "  3. rivedi CLAUDE.md — soprattutto 'Regole non negoziabili'"
echo "  4. npm run dev"
echo
rm -- "$0"
