import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_booking_bug_is_reproducible():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT / "demo_projects" / "booking_bug",
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "failed" in result.stdout


def test_duplicate_booking_is_reproducible():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT / "demo_projects" / "duplicate_booking",
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "failed" in result.stdout


def test_mock_mode_without_api_key():
    environment = {"PATH": str(Path(sys.executable).parent), "AGENT_MODE": "mock"}
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "--scenario", "booking_bug"],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "MOCK MODE - no real LLM is being used." in result.stdout
    assert "=== FINAL RESULT ===" in result.stdout
