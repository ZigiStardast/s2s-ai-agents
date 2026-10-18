"""Dan 2: tri kratke, potpuno izmišljene agent trajectory priče."""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def print_agent(name: str, steps: list[str], conclusion: str, evidence: str) -> None:
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)
    for number, step in enumerate(steps, start=1):
        print(f"Step {number}: {step}")
    print("Zaključak:", conclusion)
    print("Dokaz:", evidence)


def main() -> None:
    print("FICTIONAL EXAMPLES - ovo nisu snimljene live ReAct trajectory.")
    print_agent(
        "AGENT A — KRATAK I TAČAN",
        ["run_tests()", "read_file('app/booking.py')"],
        "Potvrda i pretraga koriste različite kolekcije.",
        "Neuspešan test i konkretan source kod.",
    )
    print_agent(
        "AGENT B — DUŽI, ALI TAČAN",
        [
            "list_files()",
            "search_logs('booking')",
            "search_logs('booking') — isto pitanje i isti rezultat, nepotrebno ponavljanje",
            "read_file('app/booking.py')",
            "run_tests()",
        ],
        "Potvrda i pretraga koriste različite kolekcije.",
        "Log, source kod i testovi.",
    )
    print_agent(
        "AGENT C — BRZ, ALI NETAČAN",
        ["search_logs('booking')"],
        "Problem je nestabilna mreža.",
        "Nema proverljivog dokaza.",
    )
    print("\nPitanja za studente:")
    print("- Koji agent je dao tačan odgovor?")
    print("- Koji agent je pružio proverljiv dokaz?")
    print("- Koji agent je imao nepotrebne pozive alata?")
    print("- Da li je najjeftiniji agent nužno najbolji?")


if __name__ == "__main__":
    main()
