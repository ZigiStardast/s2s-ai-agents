"""Mala pomoćna funkcija koja predstavlja slanje potvrde."""


def confirmation_message(student_id: str, event_id: str) -> str:
    """Vrati poruku kakva bi otišla studentu."""

    return f"Confirmation sent to {student_id} for {event_id}"
