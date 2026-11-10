"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_my_new_tool_happy_path() -> None:
    """1. Happy path: exact domain & subdomain matching."""
    test_domain_filter_exact_and_subdomain_matches()


def test_my_new_tool_bad_input_from_model() -> None:
    """2. Bad/dirty input from model: dirty allowed domains & malformed URLs."""
    test_domain_filter_normalizes_dirty_allowed_domains()
    test_domain_filter_handles_malformed_urls_and_items()


def test_my_new_tool_failure_returns_error_dict() -> None:
    """3. Failure path: invalid types return error dict without raising."""
    test_domain_filter_invalid_input_types_return_error_dict()


def test_domain_filter_exact_and_subdomain_matches() -> None:
    """Verifies that exact domains, valid subdomains, and deeply nested subdomains match."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]
    items = [
        {"url": "https://example.com/page1", "title": "Exact match"},
        {"url": "http://news.example.com/article", "title": "Subdomain match"},
        {"url": "https://deep.sub.news.example.com/story", "title": "Deep subdomain"},
        {"url": "https://unrelated.org/test", "title": "Unrelated domain"},
    ]
    res = filter_func(items=items, allowed_domains=["example.com"])
    assert res["matched_count"] == 3
    assert res["filtered_out_count"] == 1
    assert [it["title"] for it in res["items"]] == [
        "Exact match",
        "Subdomain match",
        "Deep subdomain",
    ]


def test_domain_filter_rejects_deceptive_and_spoofed_domains() -> None:
    """Critical security test: rejects phishing, deceptive suffixes, and prefix-spoofed domains."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]
    items = [
        {"url": "https://example.com.evil.org/phish", "title": "Deceptive suffix"},
        {"url": "https://fakeexample.com/login", "title": "Missing dot separator"},
        {"url": "https://example.com-attacker.net/", "title": "Hyphenated attack"},
        {"url": "https://not-example.com/fake", "title": "Prefixed domain"},
        {"url": "https://example.com:8080/legit", "title": "Legit with port"},
    ]
    res = filter_func(items=items, allowed_domains=["example.com"])
    assert res["matched_count"] == 1
    assert res["items"][0]["title"] == "Legit with port"
    assert res["filtered_out_count"] == 4


def test_domain_filter_normalizes_dirty_allowed_domains() -> None:
    """LLMs often pass domains with protocol, www prefix, uppercase, or trailing slash."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]
    dirty_domains = [
        "https://example.com/",
        "  WWW.TECHCRUNCH.COM  ",
        "vinuni.edu.vn/admissions",
        "arxiv.org:443",
    ]
    items = [
        {"url": "https://example.com/ai", "title": "Example AI"},
        {"url": "https://techcrunch.com/funding", "title": "TechCrunch"},
        {"url": "https://sub.vinuni.edu.vn/research", "title": "VinUni Sub"},
        {"url": "http://arxiv.org/abs/2401.0001", "title": "arXiv Paper"},
        {"url": "https://unallowed.com/news", "title": "Unallowed"},
    ]
    res = filter_func(items=items, allowed_domains=dirty_domains)
    assert res["matched_count"] == 4
    assert res["filtered_out_count"] == 1


def test_domain_filter_handles_malformed_urls_and_items() -> None:
    """Items with missing, empty, non-string, or malformed URLs should not crash."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]
    items = [
        {"url": "https://example.com/ok", "title": "Valid"},
        {"url": "", "title": "Empty URL"},
        {"url": "   ", "title": "Whitespace URL"},
        {"url": None, "title": "None URL"},
        {"title": "Missing URL key"},
        {"url": 9999, "title": "Int URL"},
        {"url": "javascript:alert(1)", "title": "JS Scheme"},
        "not a dictionary",
    ]
    res = filter_func(items=items, allowed_domains=["example.com"])
    assert res["matched_count"] == 1
    assert res["items"][0]["title"] == "Valid"
    assert res["filtered_out_count"] == len(items) - 1


def test_domain_filter_preserves_item_order_across_multiple_domains() -> None:
    """Order of matched items in the output list must strictly preserve input order."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]
    items = [
        {"url": "https://b.com/1", "order": 1},
        {"url": "https://a.com/2", "order": 2},
        {"url": "https://c.com/3", "order": 3},
        {"url": "https://b.com/4", "order": 4},
        {"url": "https://a.com/5", "order": 5},
    ]
    res = filter_func(items=items, allowed_domains=["a.com", "b.com"])
    assert res["matched_count"] == 4
    assert [it["order"] for it in res["items"]] == [1, 2, 4, 5]


def test_domain_filter_case_insensitive_matching() -> None:
    """Matching should be case-insensitive for both uppercase URLs and domains."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]
    items = [
        {"url": "HTTPS://NEWS.EXAMPLE.COM/Page", "title": "Upper URL"},
        {"url": "https://example.com/path", "title": "Lower URL"},
    ]
    res = filter_func(items=items, allowed_domains=["EXAMPLE.COM"])
    assert res["matched_count"] == 2
    assert res["filtered_out_count"] == 0


def test_domain_filter_invalid_input_types_return_error_dict() -> None:
    """When model passes wrong types for items or allowed_domains, return error dict without raising."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]

    # items is not list
    res1 = filter_func(items="https://example.com", allowed_domains=["example.com"])
    assert res1.get("tool") == "domain_filter"
    assert res1.get("error") == "TypeError"
    assert "items must be a list" in res1.get("message", "")

    # allowed_domains is not list
    res2 = filter_func(items=[{"url": "https://example.com"}], allowed_domains="example.com")
    assert res2.get("tool") == "domain_filter"
    assert res2.get("error") == "TypeError"
    assert "allowed_domains must be a list" in res2.get("message", "")

    # both are None
    res3 = filter_func(items=None, allowed_domains=None)
    assert res3.get("tool") == "domain_filter"
    assert res3.get("error") == "TypeError"


def test_domain_filter_empty_inputs() -> None:
    """Empty list inputs are valid and should return zero matches without error."""
    filter_func = TOOL_FUNCTIONS["domain_filter"]

    res_empty_items = filter_func(items=[], allowed_domains=["example.com"])
    assert res_empty_items["matched_count"] == 0
    assert res_empty_items["filtered_out_count"] == 0
    assert res_empty_items["items"] == []

    res_empty_domains = filter_func(items=[{"url": "https://example.com"}], allowed_domains=[])
    assert res_empty_domains["matched_count"] == 0
    assert res_empty_domains["filtered_out_count"] == 1
