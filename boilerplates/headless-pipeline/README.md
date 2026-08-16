# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Boilerplate agentico per pipeline dati headless: Bash + `claude -p` + cron.

## L'idea in una riga

**Quattro stadi, e solo uno usa l'LLM.** Raccolta, formattazione e pubblicazione sono
comandi deterministici; Claude interviene dove serve giudizio, e restituisce dati
strutturati validati contro uno schema.

## Struttura

| File | Cosa fa | Usa l'LLM? |
| --- | --- | --- |
| `bin/run.sh` | Orchestratore, con lock e log | no |
| `bin/01-fetch.sh` | Raccolta → `data/raw/<data>.json` | no |
| `bin/02-analyze.sh` | Analisi → `data/out/<data>.json` | **sì** |
| `bin/03-render.sh` | JSON → markdown, con `jq` | no |
| `bin/04-publish.sh` | Pubblicazione | no |
| `schemas/analisi.json` | Il contratto dell'output | — |
| `.claude/skills/analizza/` | Il prompt di analisi, versionato | — |

## Avvio

```bash
./init.sh "nome-pipeline" "Cosa produce"
cp .env.example .env       # e riempilo: CLAUDE_BIN va assoluto
bin/run.sh --dry-run
```

Serve `jq`. `shellcheck` è consigliato: c'è un hook che lo usa.

## Da personalizzare

1. `bin/01-fetch.sh` — le tue fonti, tra i due commenti `Personalizza da qui`
2. `schemas/analisi.json` — la forma dell'output
3. `.claude/skills/analizza/SKILL.md` — il prompt
4. `bin/04-publish.sh` — i canali

`03-render.sh` va aggiornato **insieme** allo schema: sono un contratto solo.

## Da lasciare com'è

- **Un solo stadio chiama Claude.** È il vincolo che rende la pipeline riproducibile
- `--bare`, `--json-schema` e `--max-turns` nell'invocazione
- La scrittura su file temporaneo seguita da `mv`: evita output parziali che il run
  successivo scambierebbe per validi
- `data/raw/` immutabile

## Programmarla

- **cron**: vedi `crontab.example`
- **CI**: vedi `.github-workflow.example.yml`

## Exit code

```
0  ok
1  la pipeline ha fallito (dati mancanti, stadio in errore)
2  errore dello strumento: Claude non ha girato
```

Distinguerli permette al monitoraggio di svegliare la persona giusta.
