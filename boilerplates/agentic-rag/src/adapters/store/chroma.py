"""Adattatore VectorStore su ChromaDB."""

from dataclasses import dataclass
from typing import Sequence

from ...domain.models import Chunk, Query


@dataclass
class ChromaStore:
    path: str = "./chroma"

    def upsert(self, chunks: Sequence[Chunk]) -> None:
        raise NotImplementedError("Implementa l'upsert su Chroma.")

    def search(self, query: Query, limit: int) -> Sequence[Chunk]:
        raise NotImplementedError("Implementa la ricerca su Chroma.")
