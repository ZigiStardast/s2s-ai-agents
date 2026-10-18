"""Dan 2: Reviewer poredi slab i dobar dokaz."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.config import configure_dspy, load_settings
from src.reviewer import review_finding


CASES = [
    {
        "name": "A — NEPOTKREPLJEN ZAKLJUČAK",
        "issue": "Booking confirmation postoji, ali rezervacija ne može da se pronađe.",
        "root_cause": "Internet veza je nestabilna.",
        "evidence": "Nisu pregledani testovi, logovi ni source kod.",
        "expected": "NEED_MORE_EVIDENCE",
    },
    {
        "name": "B — ZAKLJUČAK SA DOKAZOM",
        "issue": "Booking confirmation postoji, ali rezervacija ne može da se pronađe.",
        "root_cause": "Rezervacija se upisuje u confirmed_bookings, a pretraga je traži u bookings.",
        "evidence": "Odgovarajuće operacije u app/booking.py koriste različite kolekcije.",
        "expected": "SUPPORTED",
    },
]


def print_case(case: dict[str, str], verdict: str, feedback: str) -> None:
    """Prikaži i ulaze i stvarni rezultat Reviewer-a."""

    print("\n" + "=" * 60)
    print(case["name"])
    print("=" * 60)
    print("Issue:", case["issue"])
    print("Root cause:", case["root_cause"])
    print("Evidence:", case["evidence"])
    print("Expected for discussion:", case["expected"])
    print("Actual verdict:", verdict)
    print("Feedback:", feedback)


def main() -> int:
    parser = argparse.ArgumentParser(description="Poređenje DSPy Reviewer nalaza")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="prikaži determinističku simulaciju bez LLM-a",
    )
    args = parser.parse_args()

    if args.offline:
        print("OFFLINE DEMO - Reviewer rezultat je simuliran, bez LLM-a.")
        print_case(CASES[0], "NEED_MORE_EVIDENCE", "Nema proverljivih dokaza.")
        print_case(CASES[1], "SUPPORTED", "Zaključak je povezan sa konkretnim source dokazom.")
        return 0

    settings = load_settings()
    if not settings.api_key:
        print("Nema API ključa. Dodajte ključ u .env ili eksplicitno pokrenite --offline.")
        return 1

    try:
        configure_dspy(settings)
        for case in CASES:
            result = review_finding(case["issue"], case["root_cause"], case["evidence"])
            print_case(case, str(result.verdict), str(result.feedback))
        print("\nNapomena: live model može da se ne složi sa očekivanim rezultatom za diskusiju.")
        return 0
    except Exception as error:
        print(f"Reviewer poziv nije uspeo: {error}")
        print("Pokušajte ponovo, proverite model/limit ili koristite eksplicitni --offline.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
