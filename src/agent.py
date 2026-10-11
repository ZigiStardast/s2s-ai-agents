"""Jednostavan ReAct agent i transparentna mock simulacija za offline nastavu."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import tools
from .config import Settings, configure_dspy
from .trace import ToolEvent, events_from_trajectory


@dataclass
class InvestigationResult:
    """Rezultat koji CLI može da prikaže i u live i u mock režimu."""

    root_cause: str
    evidence: str
    recommendation: str
    events: list[ToolEvent]
    raw: Any = None


def _mock_investigation(scenario: str, issue: str) -> InvestigationResult:
    """Deterministička simulacija iste ideje; nije LLM i to jasno naglašava."""

    events = [
        ToolEvent(1, "run_tests", {}, tools.run_tests()),
        ToolEvent(2, "read_file", {"path": "app/booking.py"}, tools.read_file("app/booking.py")),
        ToolEvent(3, "search_logs", {"query": "booking"}, tools.search_logs("booking")),
    ]
    if scenario == "booking_bug":
        root_cause = (
            "Potvrda se upisuje u jednu kolekciju, dok pretraga bookings traži u drugoj kolekciji; "
            "zato uspešna potvrda kasnije nije vidljiva u pretrazi."
        )
    else:
        root_cause = (
            "Provera duplikata očekuje ključ event_id, ali se novi zapis čuva pod ključem event; "
            "provera zato ne prepoznaje drugo isto zakazivanje."
        )
    return InvestigationResult(
        root_cause=root_cause,
        evidence="Testovi reprodukuju prijavljeni problem, a app/booking.py i log sadrže odgovarajuće tragove.",
        recommendation="Ispraviti neslaganje u podacima, dodati regresioni test i ponovo pokrenuti testove.",
        events=events,
    )


def investigate(scenario: str, issue: str, settings: Settings) -> InvestigationResult:
    """Pokreni mock simulaciju ili pravi DSPy ReAct agent."""

    tools.set_scenario(scenario)
    if settings.mode == "mock":
        return _mock_investigation(scenario, issue)

    configure_dspy(settings)
    import dspy
    from .signatures import InvestigateIssue

    agent = dspy.ReAct(
        InvestigateIssue,
        tools=[tools.list_files, tools.read_file, tools.run_tests, tools.search_logs],
        max_iters=settings.max_iters,
    )
    result = agent(issue=issue)
    trajectory = getattr(result, "trajectory", None)
    events = events_from_trajectory(trajectory)
    return InvestigationResult(
        root_cause=str(getattr(result, "root_cause", "")),
        evidence=str(getattr(result, "evidence", "")),
        recommendation=str(getattr(result, "recommendation", "")),
        events=events,
        raw=result,
    )
