"""Četvrti korak: agent pa kontrolisani DSPy Reviewer."""

import os
import subprocess
import sys


if __name__ == "__main__":
    command = [sys.executable, "-m", "src.main", "--scenario", "booking_bug", "--review"]
    if os.getenv("AGENT_MODE", "").lower() == "mock":
        command.append("--mock")
    raise SystemExit(subprocess.call(command))
