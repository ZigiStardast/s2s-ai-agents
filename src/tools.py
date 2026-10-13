"""Četiri read-only Python funkcije koje agent sme da koristi."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .config import scenario_path

_selected_scenario: Path | None = None
_ALLOWED_EXTENSIONS = {".py", ".txt", ".md", ".log", ".json", ".yml", ".yaml"}
_MAX_OUTPUT = 4_000


def set_scenario(scenario: str) -> None:
    """Izaberi jedan poznati demo scenario za naredne pozive alata."""

    global _selected_scenario
    _selected_scenario = scenario_path(scenario)


# ----- ALATI KOJE AGENT SME DA KORISTI -----

def list_files() -> str:
    """Listaj dozvoljene tekstualne fajlove izabranog demo scenarija."""

    root = _scenario()
    files = [
        path.relative_to(root).as_posix()
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path.suffix.lower() in _ALLOWED_EXTENSIONS
        and ".env" not in path.parts
    ]
    return "\n".join(files)[:_MAX_OUTPUT] or "Nema dozvoljenih fajlova."


def read_file(path: str) -> str:
    """Pročitaj jedan mali tekstualni fajl unutar izabranog scenarija."""

    safe_path = _safe_relative_path(path)
    if not safe_path.is_file():
        return f"Fajl ne postoji: {path}"
    return safe_path.read_text(encoding="utf-8")[:_MAX_OUTPUT]


def run_tests() -> str:
    """Pokreni samo pytest testove iz izabranog scenarija."""

    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=_scenario(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=15,
        check=False,
    )
    output = (completed.stdout + "\n" + completed.stderr).strip()
    return output[-_MAX_OUTPUT:] if output else f"pytest exit code: {completed.returncode}"


def search_logs(query: str) -> str:
    """Pronađi najviše 20 linija koje sadrže upit u log fajlovima."""

    query = str(query).strip().lower()
    if not query:
        return "Upit za log pretragu ne sme biti prazan."
    matches: list[str] = []
    for log_path in sorted(_scenario().rglob("*.log")):
        for line_number, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
            if query in line.lower():
                relative = log_path.relative_to(_scenario()).as_posix()
                matches.append(f"{relative}:{line_number}: {line}")
                if len(matches) >= 20:
                    return "\n".join(matches)
    return "\n".join(matches) or "Nema pronađenih log linija."


# Bezbednosni detalji su ispod četiri funkcije koje se objašnjavaju na času.
def _scenario() -> Path:
    if _selected_scenario is None:
        raise RuntimeError("Scenario nije izabran. Prvo pozovite set_scenario().")
    return _selected_scenario


def _safe_relative_path(path: str) -> Path:
    """Validiraj relativnu tekstualnu putanju unutar scenarija."""

    candidate_text = str(path).strip()
    candidate = Path(candidate_text)
    if not candidate_text or candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("Dozvoljene su samo relativne putanje bez '..'.")
    if candidate.name == ".env" or ".env" in candidate.parts:
        raise ValueError(".env nije dozvoljen za čitanje.")
    if candidate.suffix.lower() not in _ALLOWED_EXTENSIONS:
        raise ValueError("Dozvoljen je samo poznat tekstualni tip fajla.")
    root = _scenario().resolve()
    resolved = (root / candidate).resolve()
    if root != resolved and root not in resolved.parents:
        raise ValueError("Putanja mora ostati unutar izabranog scenarija.")
    return resolved
