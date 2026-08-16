"""La regola architetturale di questo progetto, resa eseguibile.

`src/domain/` non importa nulla che non sia standard library o dominio stesso.
Se questo test fallisce, il problema è il design: NON aggiungere eccezioni a CONSENTITI.
La strada giusta è definire un Protocol in `domain/ports.py` e implementarlo in
`src/adapters/`.
"""

import ast
import pathlib
import sys

DOMINIO = pathlib.Path(__file__).resolve().parents[2] / "src" / "domain"

# Solo standard library. Non aggiungere pacchetti di terze parti qui.
CONSENTITI = set(sys.stdlib_module_names) | {"src"}


def _moduli_importati(file: pathlib.Path) -> set[str]:
    albero = ast.parse(file.read_text(encoding="utf-8"))
    moduli: set[str] = set()

    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Import):
            moduli.update(alias.name.split(".")[0] for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom):
            # `from .models import X` ha level > 0: è interno al dominio.
            if nodo.level == 0 and nodo.module:
                moduli.add(nodo.module.split(".")[0])

    return moduli


def test_il_dominio_non_importa_dipendenze_esterne() -> None:
    violazioni: list[str] = []

    for file in sorted(DOMINIO.rglob("*.py")):
        for modulo in sorted(_moduli_importati(file) - CONSENTITI):
            violazioni.append(f"{file.relative_to(DOMINIO.parents[1])}: import '{modulo}'")

    assert not violazioni, (
        "src/domain/ deve restare libero da dipendenze esterne.\n"
        + "\n".join(violazioni)
        + "\n\nDefinisci un Protocol in domain/ports.py e implementalo in src/adapters/."
    )
