"""Developer edge-case tests for ribot.conversation_search (issue #2).

Katie's acceptance tests live in tests/test_conversation_search.py; these add
coverage for the edge cases agreed in the issue's repeat-back comment.
"""

import json

import pytest

from ribot.conversation_search import search_saved_turns


def write_turns(tmp_path, turns):
    path = tmp_path / "saved.json"
    path.write_text(json.dumps(turns, ensure_ascii=False), encoding="utf-8")
    return path


@pytest.mark.parametrize("query", ["", " ", "   \t\n"])
def test_empty_or_whitespace_query_returns_empty_list(tmp_path, query):
    turns = [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "second"},
    ]
    assert search_saved_turns(query, write_turns(tmp_path, turns)) == []


def test_query_with_surrounding_spaces_still_matches_as_substring(tmp_path):
    turns = [
        {"role": "user", "content": "a 48V battery pack"},
        {"role": "user", "content": "battery"},
    ]
    assert search_saved_turns(" battery ", write_turns(tmp_path, turns)) == [
        {"role": "user", "content": "a 48V battery pack"},
    ]


def test_original_dicts_preserved_including_extra_keys(tmp_path):
    turns = [{"role": "user", "content": "Battery check", "timestamp": "2026-11-14"}]
    assert search_saved_turns("battery", write_turns(tmp_path, turns)) == turns


def test_turns_without_text_content_are_skipped(tmp_path):
    turns = [
        {"role": "user"},
        {"role": "user", "content": None},
        "not a dict",
        {"role": "assistant", "content": "the battery is fine"},
    ]
    assert search_saved_turns("battery", write_turns(tmp_path, turns)) == [
        {"role": "assistant", "content": "the battery is fine"},
    ]


def test_utf8_content_is_searchable(tmp_path):
    turns = [{"role": "user", "content": "Café enclosure — résumé attached"}]
    assert search_saved_turns("CAFÉ", write_turns(tmp_path, turns)) == turns


def test_search_does_not_modify_saved_file(tmp_path):
    path = write_turns(tmp_path, [{"role": "user", "content": "battery"}])
    before = path.read_bytes()
    search_saved_turns("battery", path)
    assert path.read_bytes() == before


def test_accepts_string_path(tmp_path):
    path = write_turns(tmp_path, [{"role": "user", "content": "battery"}])
    assert len(search_saved_turns("battery", str(path))) == 1
