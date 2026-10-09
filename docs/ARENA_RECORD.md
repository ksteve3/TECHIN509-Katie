# Week 1 — Arena record

Name/team: Katie. Collaborator Mike was assigned but became unexpectedly unavailable, so the technical work was completed independently.

Workflows before and after rotation: Specification-first before the planned rotation; Verification-first after the planned rotation.

Roles before / after rotation: Katie retained human decisions and review, with Codex providing the requested specifications, edits, and test execution. Normal role rotation could not occur because Mike was unavailable. No partner participation is claimed.

## Task and checks

Repair `Library.search(query, limit=3)` to match substrings without case sensitivity, trim surrounding query whitespace, return `[]` for blank queries or no matches, respect positive limits, return `[]` for zero limits, and preserve each result's original `source` and `text`. Keep supplied tests, data, and instructions unchanged; use no model/API dependency or hard-coded answers.

The initial acceptance checklist was written after the starting checks and before implementation edits, in the same response as the agent's proposed minimal repair. Katie approved the plan with one change: use `limit <= 0` instead of `limit == 0`. Some proposed initial checklist cases (partial substrings, tab/newline whitespace, oversized limits, and explicit field preservation) were not added as separate initial tests; the initial run verified the seven supplied tests.

After reading the reveal, extend the specification: read documents once during construction, search cached data even if the source file becomes unavailable, preserve input-file order, and return `[]` for negative limits. A new `Library` must load updated file contents. Reveal checks were added and run before changing the implementation.

All commands below were run from `exercises/week1-arena/`. Python bytecode writing was disabled to avoid cache files.

| Input or condition | Expected result | Command or steps | Actual result |
|---|---|---|---|
| `vacation` | First result has source `leave.md` | Supplied `test_normal_query`; `python -m unittest -v` | Passed initially and in final run |
| `spaceship` | `[]` | Supplied `test_unknown_query` | Passed initially and in final run |
| `PASSWORD` | Two matches, ignoring case | Supplied `test_case_insensitive` | Initially zero matches; passed after initial repair |
| ` password  ` | Two matches after trimming | Supplied `test_trim_query` | Initially zero matches; passed after initial repair |
| Empty or whitespace-only query | `[]` | Supplied `test_blank_query` | Initially empty query returned three documents; passed after initial repair |
| `password`, limit 1 | One matching document | Supplied `test_result_limit`; `python search.py` | Initially two results; one after repair |
| `password`, limit 0 | `[]` | Supplied `test_zero_limit` | Initially one result; passed after initial repair |
| Library construction and two searches | One read during construction, no additional reads | `test_loads_once_at_construction` in `test_reveal.py` | Before reveal fix: constructor performed zero reads; after fix: passed |
| Temporary fixture deleted after construction | Both subsequent searches succeed | Copy supplied JSON into a temporary directory, construct library, delete only the copy, search for `password` and `vacation` | Before reveal fix: both searches raised `FileNotFoundError`; after fix: passed |
| Multiple matches in deliberately nonalphabetical source order | Results equal the original document list in input order | `test_matches_preserve_input_file_order`, using temporary synthetic JSON | Passed before and after reveal fix |
| Limits -1, -2, and -10 | `[]` | `test_negative_limits_return_empty` | Passed before and after reveal fix |
| File updated after constructing an existing library | Existing library returns original documents; new library returns updated documents | Extra test `test_new_library_loads_updated_file_existing_library_keeps_cache`, using temporary synthetic JSON | Passed; final total 12/12 |

## Evidence

- Starting failures: `python -m unittest -v` ran seven tests: 2 passing / 5 failing, exit code 1. Normal and unknown queries passed. Blank queries, case-insensitive matching, positive limits, trimming, and zero limits failed. `python search.py` exited 0 but printed two password results despite `limit=1`.
- Agent request and proposed approach: Katie requested a specification-first plan based only on the initial requirements, with no edits until approval. Codex proposed normalizing the query, guarding blank queries and zero limits, comparing normalized text, and correcting the slice. Katie approved with `limit <= 0`.
- Changes made and why: Inside `search()`, use `query.strip().casefold()`, return `[]` for blank queries or `limit <= 0`, compare against `doc["text"].casefold()`, and use `matches[:limit]`. This corrects normalization and the off-by-one limit while returning the original dictionaries. The initial repair produced 7/7 supplied tests passing, exit code 0.
- Diff review findings: The initial diff was shown before the test run and changed only `search()`. The reveal implementation diff added the JSON load to `Library.__init__` and replaced file reading in `search()` with iteration over `self.documents`. The extra-test diff added only one test method. Supplied tests, fixture, README, and REVEAL were not edited. No separate partner diff review is claimed.
- Additional requirement and how you checked it: In the verification-first stage, added four checks in separate `test_reveal.py` before modifying implementation. The first run had sandbox permission errors creating temporary files; an approved rerun outside the sandbox established the implementation failures: constructor read count 0 rather than 1, and two `FileNotFoundError` subtests after deleting the temporary fixture. Order and negative-limit checks already passed, as did all seven supplied tests. The reveal fix loads JSON once into `self.documents` in `Library.__init__`; `search()` uses that cached list. Result: 11/11 tests passing, exit code 0. `python search.py` then printed only `[it.md] To reset your password, use the synthetic IT portal.` and exited 0.
- Your extra test case and result: Change only temporary JSON after constructing a library, construct a new library, then assert the existing library returns original data and the new one returns updated data. The added test passed without any further `search.py` change.
- Final test results: `python -m unittest -v` ran 12 tests in 0.033s: 12/12 passing, `OK`, exit code 0. This consists of seven supplied tests and five added reveal/extra tests. No implementation edits followed the final run.
- Code/commit link, or remaining failure and next check: Local code: `exercises/week1-arena/search.py`; supplied checks: `exercises/week1-arena/test_search.py`; added checks: `exercises/week1-arena/test_reveal.py`. No Arena commit or push has been made in this session, so a commit link is not yet available. No known failure remains in the tested requirements. Next submission step: review this record and the other required documents, then commit and push when authorized.

Data flow: JSON → `Library.__init__` → cached documents → query normalization → substring matching → preserved `source` and `text`. Positive limits truncate the matching list without reordering it; blank queries and nonpositive limits return `[]`.

## Compare workflows

Evidence below is limited to this session's observed specifications, diffs, and command results. Other teams' results were not observed / not yet available. No timing or effort ranking between workflows is supported.

| Workflow | Evidence source | Speed / human effort | Correctness | Code clarity | Remaining uncertainty |
|---|---|---|---|---|---|
| Vibe | Not performed in this session; direct evidence unavailable. Other teams: not observed / not yet available | Not observed / not yet available | Not observed / not yet available | Not observed / not yet available | No direct evidence for comparison |
| Specification-first | Observed in this session: initial specification and acceptance checklist, Katie's approval, minimal diff, supplied test output. Other teams: not observed / not yet available | Specification and approval preceded edits; Katie refined the limit guard. Duration and comparable effort measurements not recorded | Supplied tests improved from 2/7 to 7/7 passing; additional initial checklist cases were not separately tested at this stage | Repair stayed within `search()` and made normalization, guard, and limit explicit; no independent clarity rating | One task only; no partner review or other-team comparison; seven initial tests did not establish reveal behavior |
| Verification-first | Observed in this session: reveal tests before implementation, failing output, cache-loading diff, passing rerun, extra update/cache test. Other teams: not observed / not yet available | Tests preceded implementation; a sandbox permission issue required an approved rerun. Duration and comparable effort measurements not recorded | Tests exposed missing construction-time loading and file dependence; fix passed 11/11; extra test passed for final 12/12 | Fix moved JSON loading to construction and made searches use `self.documents`; no independent clarity rating | One task only; normal role rotation unavailable; no other-team evidence or measured speed comparison |

Which approach would you use for your chatbot, and why?

Based on this session, I would use a **specification-first approach followed by verification-first testing** for my chatbot. Writing the requirements and acceptance criteria first helped keep the initial repair small and focused. Adding tests before the reveal change then exposed file-lifecycle problems that the original checks did not catch. Combining the two approaches gave me clearer requirements, stronger verification, and a more maintainable implementation while keeping human review and approval in the loop.
