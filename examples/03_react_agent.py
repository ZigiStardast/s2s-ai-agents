"""Treći korak: direktno pokretanje ReAct agenta."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.agent import run_agent
from src.config import load_settings
from src.trace import format_trace


def main() -> int:
    settings = load_settings()
    try:
        result = run_agent(
            "booking_bug",
            "Neki studenti dobiju potvrdu, ali kasnije ne mogu da pronađu rezervaciju.",
            settings,
        )
        print(format_trace(result.events))
        print("\nRoot cause:", result.root_cause)
        return 0
    except Exception as error:
        print(f"OpenRouter nije dostupan: {error}")
        print("Podesite AGENT_MODE=mock ili OPENROUTER_API_KEY.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
