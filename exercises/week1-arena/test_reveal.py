"""Checks for the Arena reveal requirements only."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from search import Library


FIXTURE = Path(__file__).parent / "data" / "documents.json"


class RevealChecks(unittest.TestCase):
    def test_loads_once_at_construction(self):
        contents = FIXTURE.read_text(encoding="utf-8")
        with patch.object(Path, "read_text", return_value=contents) as read_text:
            library = Library(FIXTURE)
            self.assertEqual(read_text.call_count, 1)
            library.search("password")
            library.search("vacation")
            self.assertEqual(read_text.call_count, 1)

    def test_two_searches_after_temporary_file_deleted(self):
        documents = json.loads(FIXTURE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as folder:
            temporary_fixture = Path(folder) / "documents.json"
            shutil.copyfile(FIXTURE, temporary_fixture)
            library = Library(temporary_fixture)
            temporary_fixture.unlink()
            for query in ("password", "vacation"):
                with self.subTest(query=query):
                    expected = [doc for doc in documents if query in doc["text"]]
                    self.assertEqual(library.search(query), expected)

    def test_matches_preserve_input_file_order(self):
        documents = [
            {"source": "z.md", "text": "shared third alphabetically"},
            {"source": "a.md", "text": "shared first alphabetically"},
            {"source": "m.md", "text": "shared second alphabetically"},
        ]
        with tempfile.TemporaryDirectory() as folder:
            temporary_fixture = Path(folder) / "documents.json"
            temporary_fixture.write_text(json.dumps(documents), encoding="utf-8")
            library = Library(temporary_fixture)
            self.assertEqual(library.search("shared"), documents)

    def test_new_library_loads_updated_file_existing_library_keeps_cache(self):
        original = [{"source": "original.md", "text": "shared original content"}]
        updated = [{"source": "updated.md", "text": "shared updated content"}]
        with tempfile.TemporaryDirectory() as folder:
            temporary_fixture = Path(folder) / "documents.json"
            temporary_fixture.write_text(json.dumps(original), encoding="utf-8")
            existing_library = Library(temporary_fixture)

            temporary_fixture.write_text(json.dumps(updated), encoding="utf-8")
            new_library = Library(temporary_fixture)

            self.assertEqual(existing_library.search("shared"), original)
            self.assertEqual(new_library.search("shared"), updated)

    def test_negative_limits_return_empty(self):
        library = Library(FIXTURE)
        for limit in (-1, -2, -10):
            with self.subTest(limit=limit):
                self.assertEqual(library.search("password", limit=limit), [])


if __name__ == "__main__":
    unittest.main()
