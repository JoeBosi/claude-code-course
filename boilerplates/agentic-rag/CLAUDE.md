# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Python 3.12 · FastAPI · architettura esagonale · Claude Agent SDK.

## Comandi

- `uv run pytest` — tutti i test
- `uv run pytest tests/domain` — solo il dominio: veloci, **offline**
- `uv run ruff check --fix` e `uv run mypy src` — **entrambi verdi prima di ogni commit**
- `uv run uvicorn src.api.main:app --reload` — API in locale
- `uv run python -m src.cli ingest ./docs` — ingest da CLI

## La regola che tiene in piedi tutto

**`src/domain/` non importa niente da fuori di sé.** Niente `httpx`, niente `chromadb`,
niente `anthropic`, niente `fastapi`. Solo la standard library e i modelli del dominio.

È verificata da `tests/domain/test_no_external_imports.py`. Se quel test fallisce, il
problema è il design, non il test: **non aggiungere eccezioni alla lista consentita**.

## Convenzione linguistica

Codice, nomi e docstring di API pubbliche in **inglese**; commenti didattici, messaggi
di errore rivolti all'utente e documentazione in **italiano**. È la convenzione di
questo template: mantienila in ciò che aggiungi.

## Dove va cosa

| Se stai scrivendo… | Va in |
| --- | --- |
| Logica che dipende dal *problema* | `src/domain/usecases/` |
| Codice che parla con un servizio esterno | `src/adapters/<categoria>/` |
| Traduzione HTTP ↔ dominio | `src/api/` |
| La scelta di quale adattatore usare | `src/config.py` — **l'unico posto** |

## Aggiungere un adattatore

1. Implementa il `Protocol` in `src/domain/ports.py`. **Non inventare un'interfaccia nuova**
2. Aggiungilo ai test di contratto in `tests/adapters/`: ogni adattatore della stessa porta
   supera **esattamente gli stessi test**
3. Registralo in `src/config.py`
4. Non toccare `src/domain/`. Se ti serve, la porta è sbagliata: discutine prima

## Subagent

| Agente | A cosa serve |
| --- | --- |
| `researcher` | Sola lettura. Esplora e riporta con riferimenti `file:riga` |
| `coder` | Implementa, seguendo le convenzioni |
| `reviewer` | Sola lettura, Opus. Verifica la diff contro i requisiti |

Il flusso su un task non banale: `researcher` → implementazione → `reviewer`.

## Cosa NON fare senza discuterne

- Introdurre LangChain o LlamaIndex: le astrazioni le abbiamo già, e sono le nostre porte
- Aggiungere una porta nuova: prima verifica che non sia un adattatore di una esistente
- Chiamare un servizio esterno da `usecases/`

## Trappole

- Chroma persiste su disco: i test che scrivono usano una directory temporanea, mai `./chroma`
- Il rate limit del gateway LLM è per chiave, non per processo: l'ingest parallelo va limitato
- I chunk di documenti scansionati arrivano senza punteggiatura: il chunker non può
  assumere che esistano frasi
