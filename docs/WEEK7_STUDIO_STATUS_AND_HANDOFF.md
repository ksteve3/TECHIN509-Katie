# Week 7 Studio — Owner Status and Partner Handoff

**Repository submitted to Canvas:** https://github.com/ksteve3/TECHIN509-Katie  
**As of:** November 15, 2026  
**Status:** Owner preparation complete; partner collaboration **not yet verified or complete**.

This file deliberately documents unfinished steps as placeholders. It is **not** evidence that a partner implemented, reviewed, approved, or merged code.

## Completed project-owner preparation (Katie)

- [x] Chose one small feature: search saved conversation messages without deleting memory.
- [x] Committed synthetic data to `main`: [conversation_search_sample.json](../tests/data/conversation_search_sample.json).
- [x] Committed 3 exact-result acceptance tests to `main` before any implementation: [test_conversation_search.py](../tests/test_conversation_search.py).
- [x] Opened [Issue #2](https://github.com/ksteve3/TECHIN509-Katie/issues/2) with signature, inputs, outputs, test command, and out-of-scope work.
- [x] Previously verified baseline on GitHub `main`: **101 passed** excluding the intentionally failing Week 7 test module; 3 Week 7 tests failed at missing import as expected. These are results of an earlier independent checkout, not a new run.
- [x] Local `main` was reported fast-forwarded to the tests-first commit `6e96b00` with existing untracked files preserved.

## Pending: partner-delivered feature in Katie's repository

- [ ] **Partner:** [name / GitHub username not yet confirmed for this feature].
- [ ] **Access workflow:** [collaborator write permission OR fork-and-PR confirmed].
- [ ] **Issue walkthrough:** partner restates the function signature and edge-case behavior in Issue #2 before implementation.
- [ ] **Partner feature branch:** [branch URL to be added after partner creates it].
- [ ] **Partner pull request:** [PR URL to be added after partner opens it].
- [ ] **Partner PR description:** `Closes #2`, one-sentence change, verification commands and actual results.
- [ ] **Owner review:** Katie reruns the acceptance suite and full suite on the partner's branch.
- [ ] **Extra owner review input:** `search_saved_turns("48v batt", SAMPLE)` should return only `{"role": "user", "content": "The project needs a 48V battery."}`. Verify behavior with the actual implementation, not just by reading the code.
- [ ] **Review comments:** [real observed test commands / results / extra input / reasoning].
- [ ] **Outcome:** [approved / changes requested / merged / issue closed / branch preserved].

### Read-only check commands (from repo root)

```powershell
git status
git branch --show-current
git fetch origin
git rev-parse HEAD origin/main
python -m pytest tests/test_conversation_search.py -v
python -m pytest --ignore=tests/test_conversation_search.py -v
```

*Before implementation*, the focused tests should fail at the missing `ribot.conversation_search` import. *After partner implementation*, rerun `python -m pytest` and confirm all tests pass on the appropriate branch. **Do not mark a check as done until actually verified.**

## Pending: Katie's developer contribution to partner's repository

- [ ] **Partner repository:** [URL].
- [ ] **Partner's GitHub issue:** [URL and issue number].
- [ ] **Agreed feature / function contract:** [from the partner's issue].
- [ ] **Acceptance tests and sample data present in partner default branch before Katie starts:** [verified commit].
- [ ] **Katie's feature branch:** [URL].
- [ ] **Katie's PR:** [URL; must include `Closes #n`, change summary, actual test results].
- [ ] **Partner review:** [real review feedback and any revisions].
- [ ] **Merge:** [merged / issue closed / branch preserved].

## Separate contingency — NOT partner work

[Draft PR #3](https://github.com/ksteve3/TECHIN509-Katie/pull/3) is an **independent owner-authored fallback** on `week7-solo-fallback-conversation-search`. It does **not** satisfy the partner contribution or review requirements; do not represent it as Mike's work. The draft PR is not merged into `main`.

## Professor's requirements and limitations

The Week 7 studio instructions require **one actual feature delivered in the owner's repo and one PR contributed to the partner's repo**, real code review, merging, and passing tests on the default branch after merge. This document is a truthful readiness checklist, not a substitute for those actions.

Course source: https://github.com/GIX-Luyao/H-TECHIN509-2026/tree/main/week-7/studio
