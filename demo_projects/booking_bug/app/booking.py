"""Minimalni deo CampusHub-a za kreiranje i pronalaženje rezervacija."""

confirmed_bookings: list[dict[str, str]] = []
bookings: list[dict[str, str]] = []


def create_booking(student_id: str, event_id: str) -> str:
    """Kreiraj rezervaciju i vrati tekst potvrde."""

    confirmed_bookings.append({"student_id": student_id, "event_id": event_id})
    return "Booking confirmed"


def find_booking(student_id: str, event_id: str) -> list[dict[str, str]]:
    """Pronađi rezervacije za studenta i događaj."""

    return [
        booking
        for booking in bookings
        if booking["student_id"] == student_id and booking["event_id"] == event_id
    ]
