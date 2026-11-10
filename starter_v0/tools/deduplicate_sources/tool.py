from __future__ import annotations

from typing import Any

from tools._shared import err


def deduplicate_sources(
    items: list[dict[str, Any]] | None = None,
    keep_no_url: bool = True,
) -> dict[str, Any]:
    """Removes duplicate items with identical URLs, preserving the first occurrence

    and original order.
    """
    if not isinstance(items, list):
        return err("deduplicate_sources", TypeError("items must be a list of dictionaries"))

    seen_urls: set[str] = set()
    unique_items: list[dict[str, Any]] = []
    removed_count = 0

    for item in items:
        if not isinstance(item, dict):
            continue
        raw_url = item.get("url")
        if not raw_url or not isinstance(raw_url, str) or not raw_url.strip():
            if keep_no_url:
                unique_items.append(item)
            else:
                removed_count += 1
            continue

        norm_url = raw_url.strip().lower().rstrip("/")
        if norm_url in seen_urls:
            removed_count += 1
        else:
            seen_urls.add(norm_url)
            unique_items.append(item)

    return {
        "items": unique_items,
        "original_count": len(items),
        "deduped_count": len(unique_items),
        "removed_count": removed_count,
    }
