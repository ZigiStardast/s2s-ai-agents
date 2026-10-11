"""Komandni ulaz za CampusHub radionicu."""

from __future__ import annotations

import argparse
import sys
import traceback

from .agent import investigate
from .config import load_settings
from .reviewer import review_finding
from .trace import format_trace


ISSUES = {
    "booking_bug": "Neki studenti dobiju uspešnu potvrdu rezervacije, ali kasnije ne mogu da pronađu rezervaciju.",
    "duplicate_booking": "Isti student ponekad može da rezerviše isti događaj više puta.",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CampusHub DSPy agent radionica")
    parser.add_argument("--scenario", choices=sorted(ISSUES), default="booking_bug")
    parser.add_argument("--mock", action="store_true", help="koristi determinističku simulaciju bez LLM-a")
    parser.add_argument("--review", action="store_true", help="pošalji nalaz kroz DSPy Reviewer")
    parser.add_argument("--propose", action="store_true", help="prikaži human-in-the-loop predlog bez izmene fajla")
    parser.add_argument("--debug", action="store_true", help="prikaži traceback za instruktora")
    return parser


def main() -> int:
    # Windows konzola ponekad koristi cp1252; zamena je bolja od rušenja trace-a.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = build_parser().parse_args()
    settings = load_settings()
    if args.mock:
        settings = settings.__class__(mode="mock", model=settings.model, api_key=settings.api_key)
    print(f"[1] Loading scenario: {args.scenario}")
    print(f"[2] Mode: {settings.mode}")
    if settings.mode == "mock":
        print("MOCK MODE - no real LLM is being used.")
    else:
        print("[3] Configuring DSPy...")
    print("[4] Starting ReAct agent...")
    try:
        result = investigate(args.scenario, ISSUES[args.scenario], settings)
        print(format_trace(result.events))
        print("\n=== FINAL RESULT ===")
        print(f"\nRoot cause:\n{result.root_cause}")
        print(f"\nEvidence:\n{result.evidence}")
        print(f"\nRecommendation:\n{result.recommendation}")
        if args.review:
            if settings.mode == "mock":
                print("\n=== REVIEWER ===\nSUPPORTED\nMock reviewer: nalaz ima unapred pripremljene tragove.")
            else:
                review = review_finding(ISSUES[args.scenario], result.root_cause, result.evidence)
                print(f"\n=== REVIEWER ===\nVerdict: {review.verdict}\nFeedback: {review.feedback}")
        if args.propose:
            print("\n=== HUMAN APPROVAL ===")
            print("Proposed action: modify app/booking.py")
            try:
                answer = input("Approve proposed action? [y/N] ").strip().lower()
            except EOFError:
                answer = ""
            if answer == "y":
                print("Approved. In a production system, the authorized action would run here.")
            else:
                print("Not approved. No files were changed.")
        print("\n[5] Agent finished.")
        return 0
    except Exception as error:
        print(f"\nOpenRouter request failed or was rate-limited: {error}")
        print("Try again later, choose another free model, or set AGENT_MODE=mock.")
        if args.debug:
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
