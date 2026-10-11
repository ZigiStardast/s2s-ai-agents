"""Provere koje se koriste pre kreiranja CampusHub rezervacije."""


def is_duplicate(bookings: list[dict[str, str]], student_id: str, event_id: str) -> bool:
    """Vrati True ako student već ima rezervaciju za isti događaj."""

    return any(
        booking.get("student_id") == student_id and booking.get("event_id") == event_id
        for booking in bookings
    )
