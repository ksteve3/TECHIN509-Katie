"""Week 7: search saved conversation turns without changing the saved history.

The chatbot saves conversations as a JSON list of {role, content} dicts.
`search_saved_turns` reads that file and returns the turns whose content
contains the query, ignoring case. The file is only read, never written.
"""

from __future__ import annotations

import json


def search_saved_turns(query: str, json_path) -> list[dict[str, str]]:
    """Return every saved turn whose content contains `query` (case-insensitive).

    Matching turns come back as the original dicts, in their saved order.
    Returns [] when nothing matches. An empty query matches every turn,
    because an empty string is a substring of every string.
    Turns that are not dicts, or whose content is not text, are skipped.
    """
    with open(json_path, encoding="utf-8") as handle:
        turns = json.load(handle)

    needle = query.lower()
    matches = []
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        content = turn.get("content")
        if isinstance(content, str) and needle in content.lower():
            matches.append(turn)
    return matches
