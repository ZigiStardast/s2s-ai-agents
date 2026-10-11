"""Minimalni tok rezervacije za završni izazov."""

from .validation import is_duplicate

bookings: list[dict[str, str]] = []


def create_booking(student_id: str, event_id: str) -> dict[str, str]:
    """Kreiraj rezervaciju ili vrati status duplicate."""

    if is_duplicate(bookings, student_id, event_id):
        return {"status": "duplicate"}
    # Zapis se čuva u formatu koji ostatak toka koristi za prikaz događaja.
    bookings.append({"student_id": student_id, "event": event_id})
    return {"status": "confirmed"}
