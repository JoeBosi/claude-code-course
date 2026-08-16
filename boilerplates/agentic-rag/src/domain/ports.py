"""Le porte del dominio.

Ogni porta è un Protocol: il dominio dichiara cosa gli serve, gli adattatori in
`src/adapters/` dichiarano come si fa. Il dominio non conosce nessuna implementazione.

Aggiungere una porta è una decisione architetturale: prima di farlo, verifica che il
caso non sia coperto da un adattatore nuovo di una porta esistente.
"""

from typing import Protocol, Sequence

from .models import Answer, Chunk, Document, Query


class LLMGateway(Protocol):
    """Genera una risposta a partire da una domanda e dai chunk recuperati."""

    def answer(self, query: Query, context: Sequence[Chunk]) -> Answer: ...


class VectorStore(Protocol):
    """Conserva i chunk e li recupera per similarità."""

    def upsert(self, chunks: Sequence[Chunk]) -> None: ...

    def search(self, query: Query, limit: int) -> Sequence[Chunk]: ...


class DocumentSource(Protocol):
    """Fornisce i documenti da indicizzare."""

    def load(self, uri: str) -> Sequence[Document]: ...
