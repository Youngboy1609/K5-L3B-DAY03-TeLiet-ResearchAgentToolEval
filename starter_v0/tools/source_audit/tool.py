from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from tools._shared import err


def audit_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Audits source metadata to ensure URLs have valid HTTP/HTTPS schemes

    and required source metadata. Only checks metadata; does not verify
    factuality.
    """
    if not isinstance(items, list):
        return err("source_audit", TypeError("items must be a list of dictionaries"))

    issues: list[dict[str, Any]] = []
    valid_count = 0

    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            issues.append({"index": idx, "issue": "Item is not a dictionary"})
            continue

        url = item.get("url")
        if not url or not isinstance(url, str) or not url.strip():
            issues.append({"index": idx, "issue": "Missing or empty URL"})
            continue

        try:
            parsed = urlparse(url.strip())
            if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
                issues.append({"index": idx, "url": url, "issue": "Invalid URL scheme: must be http or https"})
                continue
        except Exception as exc:
            issues.append({"index": idx, "url": url, "issue": f"Malformed URL: {exc}"})
            continue

        valid_count += 1

    return {
        "ok": len(issues) == 0,
        "checked_count": len(items),
        "valid_count": valid_count,
        "issues": issues,
    }
