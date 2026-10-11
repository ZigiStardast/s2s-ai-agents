from app.booking import create_booking, find_booking


def test_confirmation_text():
    assert create_booking("ana", "python-day") == "Booking confirmed"


def test_booking_can_be_found_after_creation():
    create_booking("marko", "agents-day")
    assert find_booking("marko", "agents-day")


def test_different_student_is_not_returned():
    create_booking("jelena", "testing-day")
    assert not find_booking("nikola", "testing-day")


def test_different_event_is_not_returned():
    create_booking("ana-2", "python-day")
    assert not find_booking("ana-2", "agents-day")


def test_module_exposes_booking_functions():
    assert callable(create_booking)
    assert callable(find_booking)


def test_confirmation_is_repeatable():
    assert create_booking("pera", "debug-day") == "Booking confirmed"
