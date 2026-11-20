"""Observable Assignment 3 behavior with local, deterministic embeddings."""

import pytest

from ribot.assignment3 import CORPUS, GOLDEN, validate_golden
from ribot.build_index import build_index
from ribot.embeddings import fallback_embed
from ribot.evaluate import evaluate_hits, load_golden_set
from ribot.retriever import Retriever
from ribot.vectorstore import InMemoryStore, RetrievalHit


def test_duplicate_passages_preserve_filename_and_chunk_id(tmp_path):
    passage = "portable generator outdoors"
    for name in ("a.md", "b.txt"):
        (tmp_path / name).write_text(passage, encoding="utf-8")
    retriever = build_index(tmp_path, embed_fn=fallback_embed, quiet=True)
    hits = retriever.search_hits(passage)
    assert [hit.source_filename for hit in hits] == ["a.md", "b.txt"]
    assert [hit.chunk_id for hit in hits] == ["a.md:0", "b.txt:0"]
    assert [hit.text for hit in hits] == [passage, passage]
    assert [hit.score for hit in hits] == pytest.approx([1, 1])
    assert retriever.search(passage) == [(passage, hit.score) for hit in hits]
    assert retriever.search_text(passage) == f"{passage}\n---\n{passage}"
    assert retriever.sources() == ["a.md", "b.txt"]


def test_scores_rank_results_and_filter_weak_hits():
    store = InMemoryStore()
    store.add(
        ["topic.md:0", "topic.md:1", "other.md:0"],
        ["weak", "strong", "unrelated"],
        [[1, 3], [1, 0], [0, 1]],
    )
    retriever = Retriever(store, lambda _: [1, 0])
    hits = retriever.search_hits("topic")
    assert [hit.chunk_id for hit in hits] == ["topic.md:1", "topic.md:0"]
    assert [hit.score for hit in hits] == pytest.approx([1, 1 / 10**0.5])
    assert retriever.search_hits("topic", min_score=0.4) == hits[:1]
    assert retriever.search_hits("topic", k=1) == hits[:1]
    assert retriever.search("topic")[-1] == ("unrelated", 0)


@pytest.mark.parametrize("size,overlap", [(0, 0), (5, -1), (5, 5), (5, 6)])
def test_invalid_chunk_configuration_rejected_even_on_empty_folder(
    tmp_path, size, overlap
):
    with pytest.raises(ValueError):
        build_index(tmp_path, size=size, overlap=overlap, embed_fn=fallback_embed)


def test_empty_index_and_blank_query_do_not_embed():
    def unexpected_embed(_):
        pytest.fail("A blank query or empty index should not invoke the embedder")

    store = InMemoryStore()
    retriever = Retriever(store, unexpected_embed)
    assert retriever.search_hits("water") == []
    store.add(["a.md:0"], ["water"], [[1]])
    assert retriever.search_hits(" \t") == []


def test_evidence_requires_source_and_passage_on_same_hit():
    rows = [
        dict(id="supported", question="q", expected_source="a.md", expected_snippet="evidence"),
        dict(id="unsupported", question="q2", expected_source=None, expected_snippet=None),
    ]
    hits = [
        RetrievalHit("a.md", "a.md:0", "unrelated", 0.7),
        RetrievalHit("b.md", "b.md:0", "evidence", 0.6),
    ]
    result = evaluate_hits(rows, lambda _: hits)
    assert result["hit_at_1"] == result["hit_at_3"] == 1
    assert result["evidence_at_3"] == 0
    assert not result["unsupported"][0]["no_result"]
    assert evaluate_hits(rows, lambda _: [])["unsupported"][0]["no_result"]


def test_offline_corpus_meets_evidence_target():
    rows = load_golden_set(path=GOLDEN)
    validate_golden(rows)
    retriever = build_index(
        CORPUS, size=600, overlap=100, quiet=True, embed_fn=fallback_embed
    )
    assert retriever.search_hits("the and") == []
    result = evaluate_hits(rows, lambda query: retriever.search_hits(query, min_score=0.09))
    assert len(result["supported"]) >= 10
    assert result["evidence_at_3"] / len(result["supported"]) >= 0.8
    assert {row["id"] for row in result["unsupported"]} == {"weather", "generator-startup"}
