"""Test di contratto: ogni adattatore di una porta supera ESATTAMENTE questi test.

Aggiungendo un adattatore nuovo, aggiungilo a `adattatori()` qui sotto e non
scrivere test separati: se un adattatore ha bisogno di test diversi, non sta
rispettando la porta.
"""

from typing import Callable, Sequence

import pytest

from src.domain.models import Chunk, Query
from src.domain.ports import VectorStore


class StoreInMemoria:
    """Implementazione di riferimento, usata anche nei test del dominio."""

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []

    def upsert(self, chunks: Sequence[Chunk]) -> None:
        self._chunks.extend(chunks)

    def search(self, query: Query, limit: int) -> Sequence[Chunk]:
        termini = query.text.lower().split()
        punteggiati = [
            (sum(t in c.text.lower() for t in termini), c) for c in self._chunks
        ]
        punteggiati.sort(key=lambda coppia: coppia[0], reverse=True)
        return [c for punteggio, c in punteggiati if punteggio > 0][:limit]


def adattatori() -> list[Callable[[], VectorStore]]:
    # Aggiungi qui le factory degli altri adattatori, per esempio ChromaStore
    # con una directory temporanea. Nessuno di essi deve richiedere la rete.
    return [StoreInMemoria]


@pytest.fixture(params=adattatori(), ids=lambda f: f.__name__)
def store(request: pytest.FixtureRequest) -> VectorStore:
    return request.param()


def test_uno_store_vuoto_non_restituisce_nulla(store: VectorStore) -> None:
    assert list(store.search(Query("qualsiasi cosa"), limit=5)) == []


def test_ritrova_quello_che_ha_inserito(store: VectorStore) -> None:
    store.upsert([Chunk(document_uri="a.md", text="il retry usa backoff esponenziale", index=0)])

    risultati = list(store.search(Query("backoff"), limit=5))

    assert len(risultati) == 1
    assert risultati[0].document_uri == "a.md"


def test_rispetta_il_limite(store: VectorStore) -> None:
    store.upsert(
        [Chunk(document_uri="a.md", text=f"retry numero {i}", index=i) for i in range(10)]
    )

    assert len(list(store.search(Query("retry"), limit=3))) == 3
