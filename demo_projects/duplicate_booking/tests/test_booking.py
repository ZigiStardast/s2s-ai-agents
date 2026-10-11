from app.booking import create_booking


def test_first_booking_is_confirmed():
    assert create_booking("ana", "python-day")["status"] == "confirmed"


def test_same_student_and_event_is_rejected():
    create_booking("marko", "agents-day")
    assert create_booking("marko", "agents-day")["status"] == "duplicate"


def test_different_event_is_allowed():
    assert create_booking("jelena", "testing-day")["status"] == "confirmed"
    assert create_booking("jelena", "debug-day")["status"] == "confirmed"


def test_different_student_is_allowed():
    assert create_booking("nikola", "python-day")["status"] == "confirmed"
