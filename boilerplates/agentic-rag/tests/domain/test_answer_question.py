"""Test del dominio: offline, in millisecondi, con adattatori finti."""

from dataclasses import dataclass
from typing import Sequence

import pytest

from src.domain.models import Answer, Chunk, Citation, Query
from src.domain.usecases.answer_question import AnswerQuestion


@dataclass
class StoreFinto:
    risultati: Sequence[Chunk] = ()
    ultima_query: Query | None = None

    def upsert(self, chunks: Sequence[Chunk]) -> None:  # pragma: no cover
        raise NotImplementedError

    def search(self, query: Query, limit: int) -> Sequence[Chunk]:
        self.ultima_query = query
        return self.risultati[:limit]


@dataclass
class LLMFinto:
    chiamato: bool = False

    def answer(self, query: Query, context: Sequence[Chunk]) -> Answer:
        self.chiamato = True
        return Answer(
            text=f"risposta a: {query.text}",
            citations=tuple(Citation(c.document_uri, c.index) for c in context),
        )


def test_senza_contesto_non_chiama_il_modello() -> None:
    llm = LLMFinto()
    caso = AnswerQuestion(store=StoreFinto(risultati=()), llm=llm)

    risposta = caso("Come funziona il retry?")

    assert not llm.chiamato, "senza contesto non si spende una chiamata al modello"
    assert not risposta.is_grounded


def test_con_contesto_cita_le_fonti() -> None:
    chunks = (
        Chunk(document_uri="docs/retry.md", text="…", index=0),
        Chunk(document_uri="docs/retry.md", text="…", index=1),
    )
    caso = AnswerQuestion(store=StoreFinto(risultati=chunks), llm=LLMFinto())

    risposta = caso("Come funziona il retry?")

    assert risposta.is_grounded
    assert len(risposta.citations) == 2


def test_la_domanda_vuota_e_un_errore() -> None:
    caso = AnswerQuestion(store=StoreFinto(), llm=LLMFinto())

    with pytest.raises(ValueError):
        caso("   ")
