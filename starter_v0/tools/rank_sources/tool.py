from __future__ import annotations

from typing import Any

from tools._shared import err, terms


def rank_sources(
    items: list[dict[str, Any]] | None = None,
    query: str = "",
    limit: int | None = None,
) -> dict[str, Any]:
    """Ranks items by keyword overlap with the query.

    Heuristic only; does not evaluate factual accuracy or authority.
    """
    if not isinstance(items, list):
        return err("rank_sources", TypeError("items must be a list of dictionaries"))
    if not isinstance(query, str):
        return err("rank_sources", TypeError("query must be a string"))

    q_terms = terms(query)
    scored: list[tuple[int, dict[str, Any]]] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        it_terms = terms(text)
        overlap = len(q_terms & it_terms) if q_terms else 0
        scored.append((overlap, item))

    # Stable descending sort by keyword overlap score
    scored.sort(key=lambda x: x[0], reverse=True)
    ranked = [it for _, it in scored]

    if limit is not None and isinstance(limit, int) and limit > 0:
        ranked = ranked[:limit]

    return {
        "items": ranked,
        "ranked_count": len(ranked),
        "query_terms": sorted(list(q_terms)),
    }
