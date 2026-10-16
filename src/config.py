"""Podešavanja radionice i bezbedan izbor CampusHub scenarija."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # omogućava mock režim i u minimalnom okruženju
    def load_dotenv(_: Path) -> bool:
        return False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_ROOT = PROJECT_ROOT / "demo_projects"


@dataclass(frozen=True)
class Settings:
    """Podešavanja koja su potrebna za pokretanje jednog primera."""

    mode: str
    model: str
    api_key: str
    max_iters: int = 3
    provider: str = "openrouter"


def load_settings(mode_override: str | None = None) -> Settings:
    """Učitaj `.env` i vrati mala, čitljiva podešavanja."""

    load_dotenv(PROJECT_ROOT / ".env")
    mode = (mode_override or os.getenv("AGENT_MODE", "live")).strip().lower()
    if mode not in {"live", "mock"}:
        mode = "live"
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        return Settings(
            mode=mode,
            model=os.getenv("OPENAI_MODEL", "gpt-5.5").strip(),
            api_key=openai_key,
            provider="openai",
        )
    return Settings(
        mode=mode,
        model=os.getenv("OPENROUTER_MODEL", "openrouter/free").strip(),
        api_key=os.getenv("OPENROUTER_API_KEY", "").strip(),
        provider="openrouter",
    )


def scenario_path(scenario: str) -> Path:
    """Vrati scenario putanju samo ako je jedan od dozvoljenih scenarija."""

    if scenario not in {"booking_bug", "duplicate_booking"}:
        raise ValueError("Nepoznat scenario. Izaberite booking_bug ili duplicate_booking.")
    path = (SCENARIOS_ROOT / scenario).resolve()
    if path.parent != SCENARIOS_ROOT.resolve():
        raise ValueError("Nevažeća scenario putanja.")
    return path


def configure_dspy(settings: Settings) -> None:
    """Konfiguriši DSPy za OpenAI ili OpenRouter."""

    if not settings.api_key:
        raise RuntimeError(
            "API ključ nedostaje. Dodajte OPENAI_API_KEY ili OPENROUTER_API_KEY u .env, "
            "ili koristite AGENT_MODE=mock."
        )

    import dspy

    if settings.provider == "openai":
        model_name = settings.model
        if not model_name.startswith("openai/"):
            model_name = f"openai/{model_name}"
        lm = dspy.LM(
            model_name,
            api_key=settings.api_key,
            temperature=1.0,
            max_tokens=16000,
        )
    else:
        model_name = settings.model
        if not model_name.startswith("openai/"):
            model_name = f"openai/{model_name}"
        lm = dspy.LM(
            model_name,
            api_base="https://openrouter.ai/api/v1",
            api_key=settings.api_key,
            temperature=0.2,
            max_tokens=4000,
        )
    dspy.configure(lm=lm)
