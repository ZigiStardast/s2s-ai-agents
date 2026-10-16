"""Jedan mali ručni DSPy poziv; ne pokreće se kroz pytest."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.config import configure_dspy, load_settings


def main() -> int:
    settings = load_settings()
    if settings.provider != "openrouter" or not settings.api_key:
        print("FAIL: OPENROUTER_API_KEY nije podešen za OpenRouter smoke test.")
        return 1
    try:
        import dspy
        from src.signatures import SummarizeIssue

        configure_dspy(settings)
        result = dspy.Predict(SummarizeIssue)(issue="Smoke test: booking is missing.")
        print("SUCCESS: DSPy + OpenRouter odgovor je stigao.")
        print(result.summary)
        return 0
    except Exception as error:
        print(f"FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
