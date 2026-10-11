"""Prvi korak: Signature + Predict. Zahteva live OpenRouter podešavanje."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.config import configure_dspy, load_settings


def main() -> None:
    settings = load_settings()
    if settings.mode == "mock" or not settings.api_key:
        print("Preskačem live DSPy poziv: podesite OPENROUTER_API_KEY i AGENT_MODE=live.")
        return
    import dspy
    from src.signatures import SummarizeIssue

    configure_dspy(settings)
    summarize = dspy.Predict(SummarizeIssue)
    result = summarize(issue="Rezervacija je potvrđena, ali se kasnije ne vidi.")
    print("Summary:", result.summary)


if __name__ == "__main__":
    main()
