"""Mali formatter za javno vidljivu agentovu execution trajectory."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolEvent:
    """Jedan vidljivi korak: alat, argumenti i opažanje."""

    step: int
    tool: str
    arguments: Any
    observation: str


def _argument_text(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def events_from_trajectory(trajectory: Any) -> list[ToolEvent]:
    """Najbolje-effort čitanje javnog DSPy trajectory formata."""

    if not isinstance(trajectory, dict):
        return []
    events: list[ToolEvent] = []
    names = {}
    for key, value in trajectory.items():
        match = re.match(r"tool_name_(\d+)$", str(key))
        if match:
            names[int(match.group(1))] = value
    for number in sorted(names):
        arguments = trajectory.get(f"tool_args_{number}", trajectory.get(f"tool_arguments_{number}", {}))
        observation = trajectory.get(f"observation_{number}", "")
        events.append(ToolEvent(number, str(names[number]), _argument_text(arguments), str(observation)))
    return events


def format_trace(events: list[ToolEvent]) -> str:
    """Formatiraj kratku trace poruku za početnike."""

    lines = ["=== AGENT EXECUTION TRACE ===", ""]
    if not events:
        lines.append("Javna trajectory nije dostupna za ovaj rezultat.")
    for event in events:
        lines.extend(
            [
                f"Step {event.step}",
                f"Tool: {event.tool}",
                f"Arguments: {json.dumps(event.arguments, ensure_ascii=False)}",
                "Observation:",
                event.observation[:2_000],
                "",
            ]
        )
    return "\n".join(lines).rstrip()
