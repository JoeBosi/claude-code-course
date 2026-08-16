"""Caso d'uso: indicizzare documenti da una sorgente."""

from dataclasses import dataclass

from ..models import Chunk
from ..ports import DocumentSource, VectorStore


@dataclass(frozen=True)
class IngestDocument:
    source: DocumentSource
    store: VectorStore
    chunk_size: int = 1200
    overlap: int = 150

    def __call__(self, uri: str) -> int:
        documents = self.source.load(uri)
        chunks: list[Chunk] = []

        for doc in documents:
            chunks.extend(self._split(doc.uri, doc.text))

        if chunks:
            self.store.upsert(chunks)
        return len(chunks)

    def _split(self, uri: str, text: str) -> list[Chunk]:
        # Split per finestra scorrevole sui caratteri, non per frasi: i documenti
        # scansionati arrivano senza punteggiatura affidabile.
        if self.chunk_size <= self.overlap:
            raise ValueError("chunk_size deve essere maggiore di overlap")

        passo = self.chunk_size - self.overlap
        return [
            Chunk(document_uri=uri, text=text[i : i + self.chunk_size], index=n)
            for n, i in enumerate(range(0, max(len(text), 1), passo))
            if text[i : i + self.chunk_size].strip()
        ]
