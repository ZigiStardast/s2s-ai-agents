"""Dan 2: deterministička simulacija human-in-the-loop odobrenja."""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    print("=" * 60)
    print("SIMULACIJA: HUMAN-IN-THE-LOOP WORKFLOW")
    print("=" * 60)
    print("\n[1] Korisnik šalje zahtev u fiktivni Slack kanal.")
    print("Korisnik: Objavi kratko saopštenje o CampusHub radionici.")
    print("\n[2] AI asistent potvrđuje prijem zahteva.")
    print("AI asistent: 👀 Video sam zahtev i pripremam predlog.")
    print("\n[3] AI asistent priprema predlog u chatu.")
    print("Predlog: CampusHub radionica počinje u 10:00 u sali 204.")
    print("\n[4] Korisnik pregleda predlog.")
    answer = input("Odobriti objavu u fiktivni Confluence? [y/N] ").strip().lower()

    print("\n[5] Rezultat:")
    if answer == "y":
        print("Odobreno. Objavljivanje bi sada bilo dozvoljeno.")
        print("SIMULACIJA: ništa stvarno nije poslato niti upisano.")
    else:
        print("Nije odobreno. Ništa ne bi bilo objavljeno.")


if __name__ == "__main__":
    main()
