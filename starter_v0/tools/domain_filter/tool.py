from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from tools._shared import err


def filter_by_domain(
    items: list[dict[str, Any]] | None = None,
    allowed_domains: list[str] | None = None,
) -> dict[str, Any]:
    """Filters a list of items to keep only those matching the allowed domains.

    Supports exact domain matching and valid subdomains (e.g. news.example.com
    matches example.com). Safely rejects deceptive domains (e.g.
    example.com.evil.org). Returns an error dict if arguments have invalid
    types.
    """
    if not isinstance(items, list):
        return err("domain_filter", TypeError("items must be a list of dictionaries"))
    if not isinstance(allowed_domains, list):
        return err("domain_filter", TypeError("allowed_domains must be a list of domain strings"))

    # Normalize allowed domains
    clean_domains: list[str] = []
    for entry in allowed_domains:
        if not isinstance(entry, str):
            continue
        dom = entry.strip().lower()
        if dom.startswith("http://") or dom.startswith("https://"):
            dom = urlparse(dom).netloc
        dom = dom.replace("www.", "")
        dom = dom.split("/")[0].split(":")[0].strip()
        if dom:
            clean_domains.append(dom)

    matched_items: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        if not isinstance(url, str) or not url.strip():
            continue

        try:
            parsed = urlparse(url.strip())
            netloc = (parsed.netloc or "").lower().replace("www.", "")
            netloc = netloc.split(":")[0].strip()
        except Exception:
            continue

        if not netloc:
            continue

        # Check match against clean_domains
        is_matched = False
        for allowed in clean_domains:
            if netloc == allowed or netloc.endswith("." + allowed):
                is_matched = True
                break

        if is_matched:
            matched_items.append(item)

    return {
        "items": matched_items,
        "matched_count": len(matched_items),
        "filtered_out_count": len(items) - len(matched_items),
    }
