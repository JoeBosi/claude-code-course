"""Composition root: l'unico posto dove si sceglie quale adattatore usare.

Se stai importando un adattatore da qualche altra parte, quella parte va rifattorizzata.
"""

import os
from dataclasses import dataclass

from .domain.ports import DocumentSource, LLMGateway, VectorStore


@dataclass(frozen=True)
class Dipendenze:
    llm: LLMGateway
    store: VectorStore
    source: DocumentSource


def costruisci() -> Dipendenze:
    """Sceglie gli adattatori in base all'ambiente.

    Gli import sono locali di proposito: così importare `config` per leggerne il tipo
    non tira dentro chromadb e il client HTTP.
    """
    from .adapters.llm.claude import ClaudeGateway
    from .adapters.source.filesystem import FilesystemSource
    from .adapters.store.chroma import ChromaStore

    return Dipendenze(
        llm=ClaudeGateway(model=os.environ.get("LLM_MODEL", "claude-sonnet-5")),
        store=ChromaStore(path=os.environ.get("CHROMA_PATH", "./chroma")),
        source=FilesystemSource(),
    )
