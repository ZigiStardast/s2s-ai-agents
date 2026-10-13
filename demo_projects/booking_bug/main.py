"""Mali uvodni demo simptoma CampusHub problema."""

import sys

from app.booking import create_booking, find_booking


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    """Prikaži šta korisnik vidi pre istrage problema."""

    student_id = "marko"
    event_id = "agents-day"

    print("==================================================")
    print("           CAMPUSHUB - BOOKING DEMO")
    print("==================================================")
    print()
    print(f"Student: {student_id}")
    print(f"Event: {event_id}")
    print()
    print("[1] Student kreira rezervaciju...")
    print()
    print("CampusHub:")
    print(create_booking(student_id, event_id))
    print()
    print("[2] Student kasnije traži istu rezervaciju...")
    print()
    print("CampusHub:")
    print(find_booking(student_id, event_id))
    print()
    print("Nešto nije u redu:")
    print("rezervacija je potvrđena, ali ne može da se pronađe.")
    print()
    print("Pitanje:")
    print("Zašto se ovo dešava?")


if __name__ == "__main__":
    main()
