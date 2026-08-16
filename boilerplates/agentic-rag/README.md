# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Boilerplate agentico per sistemi agentic/RAG: Python 3.12 · FastAPI · architettura
esagonale · Claude Agent SDK.

## L'idea in una riga

**Il dominio non conosce nessuna implementazione.** Dichiara tre porte —
`LLMGateway`, `VectorStore`, `DocumentSource` — e riceve gli adattatori da
`config.py`. Cambiare Claude con un modello locale, o Chroma con pgvector, non tocca
una riga di logica.

## La regola, resa eseguibile

`tests/domain/test_no_external_imports.py` verifica che `src/domain/` non importi
nulla di esterno. Non è documentazione: è un test che fallisce.

Un hook `PreToolUse` la difende **prima** che la violazione venga scritta, con un
messaggio che dice a Claude cosa fare invece.

## Struttura

```
src/
├── domain/          zero import esterni
│   ├── models.py
│   ├── ports.py     le tre porte, come Protocol
│   └── usecases/
├── adapters/        qui le dipendenze esterne sono benvenute
│   ├── llm/  store/  source/
├── api/             solo traduzione HTTP ↔ dominio
├── cli/
└── config.py        composition root: l'UNICO posto che sceglie gli adattatori
tests/
├── domain/          offline, millisecondi
└── adapters/        contratto: ogni adattatore supera gli stessi test
```

## Avvio

```bash
./init.sh "nome-progetto" "Cosa fa"
uv sync
cp .env.example .env
uv run pytest          # 7 test passano già, senza rete
```

Serve `jq` per gli hook.

## Cosa è già scritto e cosa no

**Già scritto e testato:** modelli, porte, i due casi d'uso, i test del dominio e
l'infrastruttura dei test di contratto.

**Da implementare:** i tre adattatori. Sono `NotImplementedError` di proposito — il
messaggio di ciascuno dice cosa deve restituire. Aggiungendo un adattatore, aggiungilo
anche a `adattatori()` in `tests/adapters/test_contratto_vector_store.py`.

## Da personalizzare

- I tre adattatori
- `chunk_size` e `overlap` in `IngestDocument`, in base ai tuoi documenti
- `.mcp.json` — le sorgenti reali

## Da lasciare com'è

- **Il confine di `src/domain/`**, e il test che lo verifica
- Il fatto che `config.py` sia l'unico posto che sceglie gli adattatori
- I test di contratto condivisi: sono ciò che rende le porte reali invece che decorative
