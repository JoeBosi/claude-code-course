"""Adattatore DocumentSource che legge dal filesystem locale."""

import pathlib
from collections.abc import Sequence
from dataclasses import dataclass

from ...domain.models import Document

ESTENSIONI = {".md", ".txt", ".rst"}


@dataclass
class FilesystemSource:
    def load(self, uri: str) -> Sequence[Document]:
        radice = pathlib.Path(uri)
        if radice.is_file():
            file = [radice]
        else:
            file = [p for p in sorted(radice.rglob("*")) if p.suffix in ESTENSIONI]

        return [
            Document(uri=str(p), text=p.read_text(encoding="utf-8", errors="replace"))
            for p in file
        ]
