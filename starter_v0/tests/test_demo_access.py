try:
    from demo_access import is_valid_public_demo_code
except ModuleNotFoundError:
    is_valid_public_demo_code = None

try:
    from demo_access import user_facing_error
except ImportError:
    user_facing_error = None


def test_public_demo_code_accepts_the_configured_code() -> None:
    assert callable(is_valid_public_demo_code), "demo_access.py is not implemented"
    assert is_valid_public_demo_code("group-code", "group-code") is True


def test_public_demo_code_rejects_a_wrong_code() -> None:
    assert callable(is_valid_public_demo_code), "demo_access.py is not implemented"
    assert is_valid_public_demo_code("wrong-code", "group-code") is False


def test_public_demo_code_fails_closed_when_no_code_is_configured() -> None:
    assert callable(is_valid_public_demo_code), "demo_access.py is not implemented"
    assert is_valid_public_demo_code("anything", None) is False
    assert is_valid_public_demo_code("", "") is False


def test_public_demo_hides_internal_exception_details() -> None:
    assert callable(user_facing_error), "public error handling is not implemented"
    message = user_facing_error(RuntimeError("provider token or URL detail"), public_mode=True)
    assert message == "Không thể xử lý yêu cầu. Vui lòng thử lại sau."
    assert "provider token" not in message


def test_local_mode_keeps_the_existing_error_detail_for_debugging() -> None:
    assert callable(user_facing_error), "public error handling is not implemented"
    assert user_facing_error(RuntimeError("local detail"), public_mode=False) == "Không thể xử lý: local detail"
