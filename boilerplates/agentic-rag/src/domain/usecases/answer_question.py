"""Caso d'uso: rispondere a una domanda sui documenti indicizzati.

Riceve le porte, non le implementazioni. È il motivo per cui questo file si testa
offline in millisecondi.
"""

from dataclasses import dataclass

from ..models import Answer, Query
from ..ports import LLMGateway, VectorStore


@dataclass(frozen=True)
class AnswerQuestion:
    store: VectorStore
    llm: LLMGateway
    limit: int = 8

    def __call__(self, question: str) -> Answer:
        query = Query(text=question.strip())
        if not query.text:
            raise ValueError("la domanda non può essere vuota")

        chunks = self.store.search(query, limit=self.limit)
        if not chunks:
            # Nessun contesto: non chiamiamo il modello per farci inventare
            # una risposta. Costa meno ed è più onesto.
            return Answer(text="Non ho trovato nulla di pertinente nei documenti indicizzati.")

        return self.llm.answer(query, chunks)
