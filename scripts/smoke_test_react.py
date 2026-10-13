"""Jedan mali ručni ReAct test; ne pokreće se kroz pytest."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

from src.config import load_settings


def main() -> int:
    settings = load_settings()
    if not settings.api_key or settings.mode == "mock":
        print("FAIL: za ovaj smoke test podesite API ključ i AGENT_MODE=live.")
        return 1
    try:
        from src.agent import run_agent
        result = run_agent("booking_bug", "Find evidence about the booking issue.", settings)
        if not result.root_cause:
            print("FAIL: ReAct nije vratio root cause.")
            return 1
        print(f"SUCCESS: ReAct je završio sa {len(result.events)} javnih tool koraka.")
        return 0
    except Exception as error:
        print(f"FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
