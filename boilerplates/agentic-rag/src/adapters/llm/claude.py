"""Adattatore per il gateway LLM basato sul Claude Agent SDK.

Qui dentro le dipendenze esterne sono benvenute: è il punto del progetto in cui
si parla col mondo. Il dominio non sa che questo file esiste.
"""

from dataclasses import dataclass
from typing import Sequence

from ...domain.models import Answer, Chunk, Citation, Query


@dataclass
class ClaudeGateway:
    model: str = "claude-sonnet-5"

    def answer(self, query: Query, context: Sequence[Chunk]) -> Answer:
        # TODO: sostituire con la chiamata reale al Claude Agent SDK.
        # La forma del ritorno è ciò che conta per il resto del sistema: una risposta
        # con le citazioni dei chunk effettivamente usati.
        raise NotImplementedError(
            "Implementa la chiamata al modello. Restituisci un Answer con le Citation "
            "dei chunk che hai davvero usato: is_grounded dipende da quelle."
        )

    @staticmethod
    def _citazioni(context: Sequence[Chunk]) -> tuple[Citation, ...]:
        return tuple(Citation(c.document_uri, c.index) for c in context)
