# Week 7 Studio — Owner Delivery and Developer Handoff

**Submission repository:** https://github.com/ksteve3/TECHIN509-Katie  
**Updated:** November 15, 2026  
**Owner delivery:** Mike's feature merged; post-merge `main` verification complete (113 passed, 0 failed, 0 errors)  
**Developer delivery:** Katie's ReceiptBot implementation submitted as PR #5; Mike's review and merge pending

## Katie's project-owner work

- [x] Defined a small feature: search saved conversation messages without deleting memory.
- [x] Committed synthetic fixture [conversation_search_sample.json](../tests/data/conversation_search_sample.json) before implementation.
- [x] Committed three exact-result acceptance tests [test_conversation_search.py](../tests/test_conversation_search.py) before implementation.
- [x] Opened [Issue #2](https://github.com/ksteve3/TECHIN509-Katie/issues/2) with behavior, function signature, tests, and scope.
- [x] Partner **LBXMike** restated the contract; Katie clarified blank queries and malformed turn handling in the issue comments.
- [x] Mike contributed independently via his fork: [PR #4](https://github.com/ksteve3/TECHIN509-Katie/pull/4), implementing `ribot/conversation_search.py` and nine additional edge-case tests.
- [x] Owner review evidence: DT Chat tested exact head `bd8c4087fcfce8658547401a5125c68b70232bb5` in a separate checkout. Acceptance: **3 passed**; edge-case: **9 passed**; full suite: **113 passed**. Extra input `"48v batt"` returned exactly one matching user turn about the 48V battery. The sample file was unchanged and `git diff --check` passed.
- [x] Formal GitHub approval review posted on PR #4.
- [x] PR #4 merged into `main`, merge commit `a4da6df057eb92c5d44a6774f9858d64a1d3141a`; Issue #2 closed automatically.
- [x] Owner-authored contingency [draft PR #3](https://github.com/ksteve3/TECHIN509-Katie/pull/3) closed without merging or deleting its branch. It was not counted as partner work.
- [x] Post-merge validation on local `main` at `5209bafb189e146e1012982ec5fbb72966828cf3`: `python -m pytest` → **113 passed, 0 failed, 0 errors** (exit code 0). Local `main` matched `origin/main`; untracked notebooks and `worklog/katie.md` were preserved and hash-checked.
- [ ] Confirm instructor has access if explicit access is required.

## Katie's developer work for Mike's ReceiptBot

**Partner repository:** https://github.com/LBXMike/Techin509  
**Owner's issue:** [Issue #4 — Add item price lookup to ReceiptBot](https://github.com/LBXMike/Techin509/issues/4)

**Required implementation:** `find_item(query: str, receipts: list[dict]) -> list[dict]` in `project2/item_lookup.py`. Return results for matching item names (case-insensitive substring search) in receipt and item order. Each result must have the exact keys `receipt`, `store`, `date`, `item`, `price`. Blank or unknown queries return `[]`. Do not mutate input receipts or change existing code/tests; no chat-loop integration.

Mike's test-first setup:
- [project2/tests/test_p2_item_lookup.py](https://github.com/LBXMike/Techin509/blob/main/project2/tests/test_p2_item_lookup.py) — 5 acceptance tests
- [project2/tests/data/item_lookup_sample.json](https://github.com/LBXMike/Techin509/blob/main/project2/tests/data/item_lookup_sample.json) — synthetic receipt data
- Pre-implementation baseline independently verified by DT Chat: **75 passed**, plus **5 expected missing-import failures** for the new acceptance tests.

**Completed developer work:**
- [x] Katie restated the feature contract in [Issue #4](https://github.com/LBXMike/Techin509/issues/4) before implementation.
- [x] DT Chat cloned and verified Mike's `main` at `0dc230f76b21e0c450b3fbcdaff4b43bc6e357dc`, and ran the pre-implementation checks: 75 passed, five acceptance tests failed at the expected missing import.
- [x] Created the independent branch `week7-katie-item-lookup` and added only `project2/item_lookup.py`. No existing code, sample data, or tests changed.
- [x] DT Chat post-implementation verification: **5 acceptance tests passed**, **80 Project 2 tests passed**; diff whitespace checks passed.
- [x] Committed as `14ff6aec415a75259468ef0f02e3a335c7e6ea0e`; direct push failed with HTTP 403, so branch was pushed to [Katie's fork](https://github.com/ksteve3/Techin509/tree/week7-katie-item-lookup).
- [x] Opened [PR #5](https://github.com/LBXMike/Techin509/pull/5) into Mike's `main`, including `Closes #4`, a one-sentence summary, and actual test results. Requested Mike's review in a [PR comment](https://github.com/LBXMike/Techin509/pull/5#issuecomment-6905258443) after a formal reviewer-request attempt returned 404.
- [x] ChatGPT independently inspected the GitHub diff: one new file, matches the agreed behavior; PR was open and mergeable as of November 15, 2026.

**Pending owner actions (Mike):**
- [ ] Mike reviews PR #5 and approves or requests changes.
- [ ] If needed, Katie revises the same branch and reports new tests.
- [ ] Mike merges PR #5, closes Issue #4, retains the branch, and reruns `python -m pytest project2/tests` on his updated default branch.

## Validation commands

For Katie's repository (now that PR #4 is merged):

```powershell
git status
git fetch origin
git pull --ff-only origin main
python -m pytest
```

For Mike's repository, from the repository root:

```powershell
python -m pytest project2/tests/test_p2_item_lookup.py -v
python -m pytest project2/tests
```

## Source and integrity notes

The Week 7 studio instructions explicitly require collaboration: each person owns one feature, develops one feature for the partner, provides real review evidence, and keeps branches undeleted. This document reports completed and pending actions accurately; do not mark pending steps as done without performing them.

Instructor instructions: https://github.com/GIX-Luyao/H-TECHIN509-2026/tree/main/week-7/studio
