# PLAN

Il piano corrente. Lo scrive Claude in Plan Mode, lo correggi tu, poi si esegue.
Quando è completato, riassumilo in `STATE.md` e svuota questo file.

---

## Obiettivo

_Una frase._

## Fuori scope

_Cosa esplicitamente non tocchiamo._

## Porte coinvolte

_Quali porte esistenti bastano. Se ne serve una nuova, motivalo qui prima di scriverla._

## Passi

1. …

## Verifica

- [ ] `uv run pytest` verde, inclusi i test di contratto
- [ ] `uv run mypy src` verde
- [ ] `tests/domain/test_no_external_imports.py` verde
