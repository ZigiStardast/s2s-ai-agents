from src.tools import list_files, read_file, run_tests, search_logs, set_scenario


def setup_function():
    set_scenario("booking_bug")


def test_list_files_works():
    files = list_files()
    assert "app/booking.py" in files
    assert ".env" not in files


def test_read_file_allowed_file():
    assert "def create_booking" in read_file("app/booking.py")


def test_run_tests_only_selected_scenario():
    output = run_tests()
    assert "failed" in output or "passed" in output
    assert "booking_bug" not in output


def test_search_logs_returns_expected_match():
    output = search_logs("result_count")
    assert "result_count=0" in output
