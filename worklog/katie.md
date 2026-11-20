# Katie's work log

## 2026-11-05 | Katie directing | Codex

- I verified assignment-conversation-persistence at 5cfc597. No implementation, documentation, or test corrections were needed. The only file I changed during verification was worklog/katie.md; I made no commit.
- With the existing .venv and FakeLLM: python -m pytest tests/test_conversation_persistence.py tests/test_chatbot.py -q returned 29 passed, 0 failed; python -m pytest -q returned 101 passed, 0 failed.
- git diff --check, git diff --cached --check, and git diff --check origin/main...HEAD all passed. A synthetic JSON round trip restored prior turns and name recall, and FakeLLM received the new chatbot system prompt.
- The branch matched its upstream. My two pre-existing untracked notebooks were preserved. Open item: I still need to submit the assignment.


## 2026-11-19 — Assignment 3 retrieval

- Directing partner: Katie. Agent: Codex.
- I added a seven-document corpus, provenance-bearing retrieval, a 12-question golden set, and offline evaluation and tests. See docs/ASSIGNMENT_3_RETRIEVAL.md for the scope, file and run details.
- Files changed: ribot/build_index.py, ribot/chunking.py, ribot/evaluate.py, ribot/retriever.py, ribot/vectorstore.py, ribot/assignment3.py, data/emergency_preparedness/*.md, data/golden_set_emergency_preparedness.json, docs/ASSIGNMENT_3_RETRIEVAL.md, tests/test_assignment3_retrieval.py, and this entry.
- Starting commit: 5209bafb189e146e1012982ec5fbb72966828cf3. Implementation remains uncommitted on codex/assignment-3-retrieval.
- Verification: python -B -m ribot.assignment3 calibrate and python -B -m ribot.assignment3 golden --min-score 0.09 with network blocked. Selected 600/100 with 10/10 Evidence@3. python -B -m pytest -q -p no:cacheprovider under the offline wrapper returned 122 passed and zero network attempts.
- Open questions: both unsupported golden prompts still returned irrelevant hits. The optional transcript is deferred. Results await review.


## 2026-11-19 — Assignment 3 finalization

- I directed this session with Codex. I added the CDC free-access statement to docs/ASSIGNMENT_3_RETRIEVAL.md and added the Assignment 3 execution commands to README.md.
- I committed the approved Assignment 3 implementation and documentation as b73a1e6bab5712caabd4ab0ebf9351fa27512fcb. This worklog entry is tracked separately.
- I ran the existing virtual environment's pytest with `-q -p no:cacheprovider`, fake backends, dotenv disabled, and sockets and DNS blocked. All 122 tests passed with zero network attempts. The working and staged Git whitespace checks passed, and both notebook hashes matched.
- Both unsupported questions still return irrelevant candidates. Weak-match rejection remains future work.
