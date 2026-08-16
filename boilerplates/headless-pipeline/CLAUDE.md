# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Pipeline dati headless: Bash + `claude -p` + cron. Nessun server, nessun database: file su disco.

## Come si esegue

- `bin/run.sh [YYYY-MM-DD]` — pipeline completa. Senza argomento, oggi
- `bin/run.sh --dry-run` — tutto tranne la pubblicazione
- Ogni stadio è eseguibile da solo: `bin/02-analyze.sh 2026-08-16`

## Il contratto

- Ogni stadio **legge da disco e scrive su disco**. Nessuno stato in memoria tra stadi
- `data/raw/` è **immutabile**: si aggiunge, non si modifica. È la prova di cosa è
  successo quel giorno
- L'output di `02-analyze.sh` è validato contro `schemas/analisi.json`.
  **Se lo schema cambia, cambia anche `03-render.sh`**
- Exit code: `0` ok · `1` fallimento della pipeline · `2` errore dello strumento
  (Claude non ha girato). Il monitoraggio li distingue

## Regola non negoziabile

**Solo `02-analyze.sh` chiama Claude.**

Raccolta, formattazione e pubblicazione sono comandi deterministici. Se ti viene voglia di
chiedere a Claude di fare un `curl`, di ordinare una lista o di formattare del markdown, la
risposta è no: costa di più, è meno affidabile e non è riproducibile.

## Come si invoca Claude

Sempre con `--bare`, `--max-turns` e `--json-schema`. Mai senza.

- `--bare` perché il risultato deve essere identico su ogni macchina: niente hook,
  skill o `CLAUDE.md` dell'host
- `--json-schema` perché l'output è dato, non prosa
- `--max-turns` perché nessuno sta guardando

Il prompt vive in `.claude/skills/analizza/SKILL.md`, **non inline negli script**: così è
versionato e si rivede in diff.

## Struttura

| File | Cosa fa | Usa l'LLM? |
| --- | --- | --- |
| `bin/run.sh` | Orchestratore | no |
| `bin/01-fetch.sh` | Raccolta dati | no |
| `bin/02-analyze.sh` | Analisi e giudizio | **sì** |
| `bin/03-render.sh` | JSON → markdown, con `jq` | no |
| `bin/04-publish.sh` | Pubblicazione | no |

## Cosa NON fare senza discuterne

- Aggiungere un secondo stadio che chiama Claude
- Introdurre un framework di orchestrazione: per una pipeline lineare, `run.sh` basta
- Scrivere in `data/raw/` da uno stadio diverso da `01-fetch.sh`

## Trappole

- `cron` ha un `PATH` minimo: `bin/run.sh` fa il source di `.env` ed esporta il PATH pieno
- `claude` non è nel PATH di cron: usa il percorso assoluto, che `run.sh` risolve con
  `command -v claude` e salva in `.env`
- Se l'API è lenta, `02` può superare la finestra dello slot: c'è un lock in `logs/.lock`
