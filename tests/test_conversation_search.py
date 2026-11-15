"""Week 7 owner acceptance tests: search saved conversation turns.

Run from repository root:
    python -m pytest tests/test_conversation_search.py -v

Synthetic sample data: tests/data/conversation_search_sample.json
The developer implements ribot.conversation_search.search_saved_turns().
These tests intentionally precede the implementation (test-first workflow).
"""

from pathlib import Path

SAMPLE = Path(__file__).parent / "data" / "conversation_search_sample.json"


def test_search_finds_all_matching_turns_case_insensitively_in_order():
    from ribot.conversation_search import search_saved_turns

    assert search_saved_turns("BATTERY", SAMPLE) == [
        {"role": "user", "content": "The project needs a 48V battery."},
        {"role": "assistant", "content": "I noted the battery requirement."},
    ]


def test_search_unknown_term_returns_empty_list():
    from ribot.conversation_search import search_saved_turns

    assert search_saved_turns("motor", SAMPLE) == []


def test_search_matches_another_term_from_sample_not_just_battery():
    from ribot.conversation_search import search_saved_turns

    assert search_saved_turns("cardboard", SAMPLE) == [
        {"role": "user", "content": "The prototype enclosure is cardboard."},
        {"role": "assistant", "content": "I will remember the cardboard enclosure."},
    ]
