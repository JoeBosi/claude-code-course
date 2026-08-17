"""I modelli del dominio.

Solo standard library. Nessun import da fuori: la regola è verificata da
`tests/domain/test_no_external_imports.py`.
"""

from dataclasses import dataclass, field

# Tutti i modelli sono @dataclass(frozen=True): "frozen" = immutabile, una
# volta creato l'oggetto i suoi campi non si possono più cambiare. Un dato che
# non può cambiare sotto i piedi è un dato di cui ci si può fidare ovunque
# venga passato — e Python solleva un errore a chi ci prova.


@dataclass(frozen=True)
class Document:
    uri: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Chunk:
    document_uri: str
    text: str
    index: int
    score: float | None = None


@dataclass(frozen=True)
class Query:
    text: str


@dataclass(frozen=True)
class Citation:
    document_uri: str
    chunk_index: int


@dataclass(frozen=True)
class Answer:
    text: str
    citations: tuple[Citation, ...] = ()

    @property
    def is_grounded(self) -> bool:
        """Una risposta senza citazioni non è ancorata alle fonti.

        Chi consuma la risposta decide cosa farne: mostrarla con un avviso, o
        rifiutarla. Il dominio non decide la politica, espone il fatto.
        """
        return len(self.citations) > 0
