# Assignment 3 — Offline document retrieval

## Goal

I extended my offline assistant so I can search a small collection of local references and verify the filename and passage behind each hit. I reused the instructor's loader, character chunker, deterministic hash embeddings, cosine similarity, in-memory store, and retriever. The existing tuple-based search and chatbot workflows retain their interfaces. For this assignment I evaluated retrieval results directly.

## Corpus and source reuse

I placed seven attributed summaries in [the corpus folder](../data/emergency_preparedness). Each file records its publisher, source title, URL, capture date, and relevant headings. The collection covers emergency drinking water, generator safety, food during outages, emergency lighting, wound care, photovoltaic electricity, and traditional hand papermaking. I checked the summaries against the linked source passages, including the elevation condition for boiling water, closed-door conditions for cold food, and outdoor generator clearance.

I used original prose to summarize facts. The collection includes no copied images, logos, tables, or video. CDC's terms describe how to attribute agency material and distinguish it from third-party content. The original CDC materials are available free of charge on the agency's website. Inclusion of the CDC references implies no endorsement by CDC, ATSDR, HHS, or the U.S. government. DOE and federal guidance also identify exceptions for third-party content. I summarized the Georgia Tech museum's factual description without reproducing its text or images or assuming a republication license. [CDC reuse policy](https://www.cdc.gov/other/agencymaterials.html) · [DOE web policies](https://www.energy.gov/web-policies) · [U.S. Copyright Office guidance on protected material](https://www.copyright.gov/help/faq/faq-protect.html)

I deferred the optional video example because I did not verify a suitable timestamped transcript and its reuse terms. The seven documents contain public reference information and are indexed as local UTF-8 Markdown.

## Retrieval contract

`Retriever.search_hits(question, k=3, min_score=0.0)` returns ranked records with `source_filename`, `chunk_id`, `text`, and `score`. A result carries the ID of the indexed record that produced the score. Two files with identical text therefore still return their own filenames and IDs. IDs use `filename:ordinal` within a single index and can change when the file or chunk settings change.

Blank questions and empty indexes return an empty list. Scores at or below the cutoff are discarded. For the experiment I explicitly injected `fallback_embed` into the index builder and used the in-memory store. These scores are cosine similarities between hashed word vectors. The optional Chroma adapter preserves result IDs on the structured path, and its existing distance-derived scores are outside this experiment.

## Golden questions and scoring

I labeled [12 questions](../data/golden_set_emergency_preparedness.json) before scoring. Ten cite passages checked against the saved files, including paraphrases and questions that need a qualifier. The two unsupported questions ask for tomorrow's forecast and the exact startup steps for a portable generator model. I checked the seven summaries for both answers and found neither. The related generator safety passage covers placement and carbon monoxide detection.

Hits@1 and Hits@3 require the expected filename among the first one or three results. Evidence@3 requires the expected filename and the full labeled passage in the **same** hit. The target was at least 8 of 10 supported questions at Evidence@3. The runner reports unsupported queries separately, including whether they received any hits after filtering.

## Calibration

I ran four supported and two unsupported probes before running the golden questions. With 600/100, the unrelated book question scored 0.081 at rank one, the supported scrape question scored 0.107, and the adjacent repair-shop question scored 0.190. I froze a strict cutoff of 0.09 for all three configurations. That retained the scrape passage at 600/100 and removed the unrelated calibration hits across configurations. It still admitted the repair-shop query. The lighting paraphrase about candles and a blackout missed the correct source in the top three at all three sizes. This small probe showed how lexical mismatch and hash collisions affect the fallback.

## Final results

| Characters / overlap | Chunks | Characters embedded | Hits@1 | Hits@3 | Evidence@3 | Supported queries with repeated source in results |
|---|---:|---:|---:|---:|---:|---:|
| 300 / 50 | 24 | 5,581 | 10/10 | 10/10 | 10/10 | 10/10 |
| 600 / 100 | 14 | 5,385 | 10/10 | 10/10 | 10/10 | 8/10 |
| 900 / 150 | 10 | 4,901 | 9/10 | 10/10 | 10/10 | 3/10 |

I selected **600/100**. It kept the same top-rank and evidence scores as 300/50 with 10 fewer embedded vectors and fewer queries that returned several passages from one source. The 900/150 windows gave more surrounding context and the smallest index, but the elevation question ranked first aid ahead of the water guide. The water guide still returned the complete evidence at rank two. The smaller windows can isolate a topic more closely, but character boundaries can split instructions from qualifiers. Larger overlaps help preserve phrases near those boundaries and can also repeat passages and consume top-three slots. The starter can emit a trailing overlap window even when the preceding window already reaches the end. The counts above include these windows and measure indexing work without relying on timings for this small corpus.

| Unsupported question | 300 / 50 top score | 600 / 100 top score | 900 / 150 top score | Outcome |
|---|---:|---:|---:|---|
| Tomorrow's weather forecast | 0.298 | 0.121 | 0.298 | Hits at all sizes, with no forecast evidence |
| Exact generator startup steps | 0.350 | 0.280 | 0.280 | Hits at all sizes, with no startup evidence |

At 600/100, the top weather result was a food-storage passage and the top generator-startup result was a water passage. The cutoff did not reject either golden unsupported query. The supported retrieval target passed on this small set, and the unsupported results show why a similarity score alone is insufficient to decide whether a passage answers a question.

## Reproduction and repository record

From the repository root in PowerShell:

```powershell
$env:PYTHON_DOTENV_DISABLED = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:OPENAI_API_KEY = ' '
$env:RIBOT_LLM = 'fake'
$env:RIBOT_EMBED = 'fake'
.\.venv\Scripts\python.exe -B -m ribot.assignment3 calibrate
.\.venv\Scripts\python.exe -B -m ribot.assignment3 golden --min-score 0.09
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
git diff --check
```

For the recorded runs I also patched `dotenv.load_dotenv` to return without reading a file and blocked Python socket creation, connection, and DNS lookup inside the test process. The full suite passed **122 tests** with **zero network attempts**. Calibration and the golden run also recorded zero attempts.

The starting commit was `5209bafb189e146e1012982ec5fbb72966828cf3` on local `main`, with no tracked changes. GitHub's `main` was one commit ahead, touching only `docs/WEEK7_STUDIO_STATUS_AND_HANDOFF.md`. The local branch `codex/assignment-3-retrieval` starts at the local commit. The remote change remains on GitHub and was outside this implementation.

| Existing untracked file | Starting SHA-256 |
|---|---|
| `HMSTI_509_M1_Lesson.ipynb` | `472174BD51BC45E23784CD37A86AA585B3A3379017017EC8C340C62E19E2A869` |
| `density_relevance.ipynb` | `E73815693D21EC74B49D47D41905369553C81A45F1FF505717A94FD28A14CB22` |
| `worklog/katie.md` | `D106880809E3384270473219CDFF7DF02CACE4EC5C268A3FAEE9E055FB79FB22` |
