"""Četvrti korak: ReAct agent pa kontrolisani DSPy Reviewer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.agent import run_agent
from src.config import load_settings
from src.reviewer import review_finding
from src.trace import format_trace


def main() -> int:
    issue = "Neki studenti dobiju potvrdu, ali kasnije ne mogu da pronađu rezervaciju."
    settings = load_settings()
    try:
        result = run_agent("booking_bug", issue, settings)

        print(format_trace(result.events))
        print("\nRoot cause:", result.root_cause)

        if settings.mode == "mock":
            print("\nReviewer verdict: SUPPORTED")
            print("Reviewer feedback: Mock reviewer koristi unapred pripremljene tragove.")
        else:
            review = review_finding(issue, result.root_cause, result.evidence)
            print("\nReviewer verdict:", review.verdict)
            print("Reviewer feedback:", review.feedback)
        return 0
    except Exception as error:
        print(f"OpenRouter nije dostupan: {error}")
        print("Podesite AGENT_MODE=mock ili API ključ u .env.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
