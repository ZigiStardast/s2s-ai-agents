"""Drugi korak: alati su obične Python funkcije, čak i bez AI-ja."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.tools import list_files, read_file, run_tests, search_logs, set_scenario


def main() -> None:
    set_scenario("booking_bug")
    print("FILES\n", list_files())
    print("\nBOOKING SOURCE\n", read_file("app/booking.py"))
    print("\nTESTS\n", run_tests())
    print("\nLOG SEARCH\n", search_logs("confirmed"))


if __name__ == "__main__":
    main()
