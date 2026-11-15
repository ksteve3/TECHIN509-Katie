"""Week 7: Search saved conversation turns without truncating conversation history."""

from __future__ import annotations

from pathlib import Path

from .chatbot import load_conversation


def search_saved_turns(query: str, json_path: str | Path) -> list[dict[str, str]]:
    """Return saved turns whose content contains query, ignoring case.

    Uses the existing conversation loader to validate the JSON file.
    Results preserve message order and original role/content text.
    """
    if not isinstance(query, str):
        raise ValueError("Query must be text")
    if not query.strip():
        return []

    needle = query.casefold()
    turns = load_conversation(str(json_path))
    return [turn for turn in turns if needle in turn["content"].casefold()]
