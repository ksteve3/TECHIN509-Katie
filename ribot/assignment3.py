"""Reproduce the local Assignment 3 retrieval experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

from .build_index import build_index, load_docs
from .embeddings import fallback_embed
from .evaluate import evaluate_hits, load_golden_set

DATA = Path(__file__).resolve().parent.parent / "data"
CORPUS = DATA / "emergency_preparedness"
GOLDEN = DATA / "golden_set_emergency_preparedness.json"
CONFIGS = ((300, 50), (600, 100), (900, 150))
CALIBRATION = (
    ("What should I use instead of candles in a blackout?", "fema_emergency_lighting.md"),
    ("Which device turns sunlight into electricity?", "doe_solar_pv.md"),
    ("How did traditional papermakers remove water using a screw press?", "gatech_hand_papermaking.md"),
    ("How should I protect a scrape from floodwater?", "cdc_basic_first_aid.md"),
    ("Who wrote Pride and Prejudice?", None),
    ("Where is the nearest generator repair shop?", None),
)


def validate_golden(rows: list[dict]) -> None:
    """Verify supporting passages against the full, saved corpus before scoring."""
    documents = dict(load_docs(CORPUS))
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Golden question IDs must be unique")
    for row in rows:
        source = row["expected_source"]
        snippet = row["expected_snippet"]
        if source is None and snippet is None:
            continue
        if not snippet or source not in documents or snippet not in documents[source]:
            raise ValueError(f"Cannot locate expected evidence for {row['id']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", choices=("calibrate", "golden"))
    parser.add_argument("--min-score", type=float, default=0.0)
    args = parser.parse_args()
    if args.run == "golden":
        golden = load_golden_set(path=GOLDEN)
        validate_golden(golden)

    for size, overlap in CONFIGS:
        print(f"\nsize={size}, overlap={overlap}")
        retriever = build_index(
            CORPUS, size=size, overlap=overlap, embed_fn=fallback_embed
        )

        if args.run == "calibrate":
            for question, source in CALIBRATION:
                hits = retriever.search_hits(question)
                scores = ", ".join(f"{hit.chunk_id} {hit.score:.3f}" for hit in hits)
                print(f"{question} | expected {source} | {scores or 'no positive hits'}")
            continue

        def search(question: str):
            return retriever.search_hits(question, min_score=args.min_score)

        result = evaluate_hits(golden, search)
        total = len(result["supported"])
        for metric in ("hit_at_1", "hit_at_3", "evidence_at_3"):
            print(f"{metric}={result[metric]}/{total}")
        for row in result["supported"]:
            ids = ", ".join(f"{hit.chunk_id} {hit.score:.3f}" for hit in row["hits"])
            print(f"{row['id']} | evidence={row['evidence_at_3']} | {ids}")
        for row in result["unsupported"]:
            top = retriever.search_hits(
                next(item["question"] for item in golden if item["id"] == row["id"]),
                k=1,
            )
            best = f"{top[0].chunk_id} {top[0].score:.3f}" if top else "none"
            print(f"{row['id']} | no result={row['no_result']} | top before cutoff={best}")


if __name__ == "__main__":
    main()
