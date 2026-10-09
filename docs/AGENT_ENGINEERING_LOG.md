# Agent Engineering Log

## Week 1 — Arena

**Date:** October 8, 2026  
**Task:** Week 1 Arena document-search repair and verification  
**Tool / model:** ChatGPT coding agent with human review and approval

### What I delegated

I used the coding agent to inspect the Arena starter files, run the supplied tests, summarize failures, propose minimal repairs, create additional verification checks after the reveal, and run the tests again after each change.

### Human decisions

I reviewed the proposed changes before accepting them. One specific decision I made was to use `limit <= 0` instead of checking only `limit == 0`, because negative limits should also return an empty result.

I also chose to keep the repair minimal rather than redesigning the search program.

### What worked

The initial environment check completed successfully. The supplied Arena baseline produced the expected result of 2 passing and 5 failing tests.

Using a specification-first workflow helped define the expected behavior before changing the code. The repair added trimmed, case-insensitive substring matching and correct result-limit behavior. After that change, all 7 supplied tests passed.

After reading the reveal requirements, I used a verification-first workflow by adding new checks before changing the implementation. Those checks exposed a file-lifecycle problem: the library was rereading the source file on every search instead of loading the documents once when constructed.

Updating the `Library` class to load the documents during initialization fixed that problem. A final additional test checked that an existing Library retained its originally loaded data while a newly created Library saw updated data.

Final result: **12 passing tests**.

### What failed or needed correction

The original implementation failed blank-query handling, case-insensitive matching, whitespace trimming, positive result limits, and zero-limit behavior.

The first specification-first repair passed the supplied tests but still failed the reveal requirements because it reread the JSON file during each search.

One temporary-file verification run also encountered a sandbox permission issue. The test was rerun with the required access; this was an environment issue rather than a defect in the search logic.

### How I verified the result

I verified the work by repeatedly running:

`python -m unittest -v`

I also ran:

`python search.py`

The final unit-test run reported 12 passing tests, and `search.py` completed successfully.

I reviewed the final code diff to confirm that the implementation remained small and that the returned document dictionaries preserved their original `text` and `source` fields.

### What is still unknown

The vibe workflow was not separately performed in this session, so I do not claim measured results from that workflow. The workflow comparison records it as not observed rather than inventing evidence.

Mike and I completed some testing together during class. He was unexpectedly unavailable for the later completion session, so I completed the remaining Arena technical work and final verification independently. His scoping review is still pending.

### Improvement for my next agent workflow

I would combine specification-first and verification-first practices: define observable acceptance criteria before implementation, then write or run checks that can expose requirements the initial specification may have missed before accepting the final result.
