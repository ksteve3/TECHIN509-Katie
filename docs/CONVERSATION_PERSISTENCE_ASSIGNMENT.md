# Assignment: Reusable Chatbot Components and Conversation Persistence

## Goal
I extended my existing TECHIN 509 chatbot so it can validate messages, save a conversation, and read it back. I reused the existing `ConversationLogger`, `ChatBot`, and `export_to_json` rather than creating a separate chat application.

## Component contracts
| Function or method | Input | Output / responsibility |
| --- | --- | --- |
| `validate_turn(role, content)` | Role string and message text | Returns a `{"role": ..., "content": ...}` dict, or raises `ValueError` |
| `ChatBot.add_turn(role, content)` | One conversation turn | Validates and adds the same turn to active history and the full log |
| `ConversationLogger.log(role, content)` | One conversation turn | Reuses the validator and records the turn |
| `ChatBot.save(filename)` | JSON file path | Writes the entire conversation log using the existing JSON export helper |
| `load_conversation(filename)` | JSON file path | Returns fully validated turns or raises `ValueError` |
| `ChatBot.resume(filename)` | JSON file path | Replaces conversation turns and log only *after* all saved data passes validation |

## Design choice
I extracted shared validation into `validate_turn` so live chat turns and saved turns follow one contract. I preserve the exact text (including spaces and punctuation) rather than calling `clean_message`, because changing a message would change the context sent to the model. When resuming, I keep the new chatbot's system prompt rather than importing one from a JSON file. Loading validates every turn before changing session state, avoiding a partially restored conversation.

I deliberately preserved the current chatbot's unlimited in-session history: this assignment does not introduce trimming or change its memory window. `reset()` retains its original behavior of clearing active history only; the logger still contains earlier turns until a new session is loaded.

## Error handling
Malformed JSON, missing/unreadable files, invalid JSON structure, unsupported roles, and non-string messages raise a readable `ValueError`. A bad saved session does not partially overwrite active history.

## Serialization demonstration
```python
from ribot.chatbot import ChatBot

first = ChatBot()
first.add_turn("user", "Remember my project.")
first.add_turn("assistant", "I will remember it.")
first.save("conversation.json")

restored = ChatBot()
restored.resume("conversation.json")
assert restored.history[1:] == first.history[1:]
assert restored.logger.turns == first.logger.turns
print("Conversation saved and restored.")
```

The JSON contains only user and assistant turns; the configured system prompt stays in the application.

## Tests
New focused tests are in `tests/test_conversation_persistence.py`. They cover message validation, invalid-input atomicity, JSON round trips, malformed files, invalid saved turns, missing files, and invalid top-level JSON structures.

From the project root (Windows PowerShell), run:

```powershell
$env:OPENAI_API_KEY = ' '
$env:RIBOT_LLM = 'fake'
$env:RIBOT_EMBED = 'fake'
python -m pytest tests/test_conversation_persistence.py tests/test_chatbot.py -q
python -m pytest -q
git diff --check
```

These commands need to be run on the checked-out branch before submission. The tests do not require a paid model API.

## Limitation
Conversation files are plain JSON and are not encrypted. They should only contain synthetic or otherwise approved non-sensitive content. There is also no automatic persistence between runs: someone must call `save()` and `resume()`, and the current design keeps the full conversation in memory. The offline FakeLLM is deterministic test scaffolding, not a genuine local reasoning model.
