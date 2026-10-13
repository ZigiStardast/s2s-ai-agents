"""Mali izolovani formatter za javno vidljivu execution trajectory."""

from __future__ import annotations

import json
import re


def trajectory_events(trajectory: object) -> list[dict[str, object]]:
    """Pretvori DSPy javnu trajectory u jednostavne korake za prikaz."""

    if not isinstance(trajectory, dict):
        return []

    events: list[dict[str, object]] = []
    tool_numbers = []
    for key in trajectory:
        match = re.match(r"tool_name_(\d+)$", str(key))
        if match:
            tool_numbers.append(int(match.group(1)))

    for number in sorted(tool_numbers):
        arguments = trajectory.get(
            f"tool_args_{number}", trajectory.get(f"tool_arguments_{number}", {})
        )
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                pass
        events.append(
            {
                "step": number,
                "tool": str(trajectory[f"tool_name_{number}"]),
                "arguments": arguments,
                "observation": str(trajectory.get(f"observation_{number}", "")),
            }
        )
    return events


def format_trace(events: list[dict[str, object]]) -> str:
    """Formatiraj samo ono što studenti treba da vide: alat i observation."""

    lines = ["=== AGENT EXECUTION TRACE ===", ""]
    if not events:
        lines.append("Javna trajectory nije dostupna za ovaj rezultat.")
    for event in events:
        lines.extend(
            [
                f"Step {event['step']}",
                f"Tool: {event['tool']}",
                f"Arguments: {json.dumps(event['arguments'], ensure_ascii=False)}",
                "Observation:",
                str(event["observation"])[:2_000],
                "",
            ]
        )
    return "\n".join(lines).rstrip()
