"""Arena starter: deliberately buggy. Repair using the task and checks."""
import json
from pathlib import Path


class Library:
    def __init__(self, path):
        self.path = Path(path)
        self.documents = json.loads(self.path.read_text(encoding="utf-8"))

    def search(self, query, limit=3):
        query = query.strip().casefold()
        if not query or limit <= 0:
            return []

        matches = [doc for doc in self.documents if query in doc["text"].casefold()]
        return matches[:limit]


if __name__ == "__main__":
    library = Library(Path(__file__).parent / "data" / "documents.json")
    for hit in library.search("password", limit=1):
        print(f"[{hit['source']}] {hit['text']}")
