from __future__ import annotations

import hmac


def is_valid_public_demo_code(supplied_code: str, configured_code: str | None) -> bool:
    """Compare a submitted demo code, failing closed when no code is configured."""
    if not isinstance(supplied_code, str) or not isinstance(configured_code, str):
        return False
    if not configured_code:
        return False
    return hmac.compare_digest(supplied_code, configured_code)


def user_facing_error(error: Exception, *, public_mode: bool) -> str:
    """Hide provider and infrastructure details from public demo visitors."""
    if public_mode:
        return "Không thể xử lý yêu cầu. Vui lòng thử lại sau."
    return f"Không thể xử lý: {error}"
