"""Jasan put od Signature-a i alata do jednog DSPy ReAct agenta."""

from __future__ import annotations

from dataclasses import dataclass

from . import tools
from .config import Settings, configure_dspy
from .trace import trajectory_events


@dataclass
class InvestigationResult:
    """Zajednički mali format za live i mock rezultat."""

    root_cause: str
    evidence: str
    recommendation: str
    events: list[dict[str, object]]


def run_mock_agent(scenario: str) -> InvestigationResult:
    """Vrati scripted fallback kada pravi LLM nije dostupan."""

    events = [
        {
            "step": 1,
            "tool": "run_tests",
            "arguments": {},
            "observation": tools.run_tests(),
        },
        {
            "step": 2,
            "tool": "read_file",
            "arguments": {"path": "app/booking.py"},
            "observation": tools.read_file("app/booking.py"),
        },
        {
            "step": 3,
            "tool": "search_logs",
            "arguments": {"query": "booking"},
            "observation": tools.search_logs("booking"),
        },
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


def run_agent(scenario: str, issue: str, settings: Settings) -> InvestigationResult:
    """Pokreni mock fallback ili pravi DSPy ReAct agent."""

    tools.set_scenario(scenario)
    if settings.mode == "mock":
        return run_mock_agent(scenario)
    
    configure_dspy(settings)
    
    import dspy
    from .signatures import InvestigateIssue
    
    agent = dspy.ReAct(
        InvestigateIssue,
        tools = [
            tools.list_files,
            tools.read_file,
            tools.run_tests,
            tools.search_logs,
        ],
        max_iters=3
    )
    
    prediction = agent(issue=issue)
    
    return InvestigationResult(
        root_cause=str(getattr(prediction, "root_cause", "")),
        evidence=str(getattr(prediction, "evidence", "")),
        recommendation=str(getattr(prediction, "recommendation", "")),
        events=trajectory_events(getattr(prediction, "trajectory", None)),
    )
