"""Assignment: reusable chatbot components and conversation persistence."""

import json

import pytest

from ribot.chatbot import ChatBot, load_conversation, validate_turn


def test_validate_turn_preserves_original_text():
    assert validate_turn("user", "  Hello, Katie!  ") == {
        "role": "user", "content": "  Hello, Katie!  "
    }


@pytest.mark.parametrize("role,content", [
    ("system", "not permitted"),
    ("other", "hello"),
    ("user", None),
    ("assistant", 123),
])
def test_invalid_turn_rejected(role, content):
    with pytest.raises(ValueError):
        validate_turn(role, content)


def test_add_turn_rejects_invalid_input_without_changing_memory():
    bot = ChatBot(system_prompt="Test assistant")
    before_history = [item.copy() for item in bot.history]
    before_log = list(bot.logger.turns)
    with pytest.raises(ValueError):
        bot.add_turn("user", None)
    assert bot.history == before_history
    assert bot.logger.turns == before_log


def test_json_round_trip_preserves_messages(tmp_path):
    first = ChatBot(system_prompt="Assistant A")
    first.add_turn("user", "  Please remember my project.  ")
    first.add_turn("assistant", "I will remember it.")
    filename = tmp_path / "conversation.json"
    first.save(str(filename))
    saved_data = json.loads(filename.read_text(encoding="utf-8"))
    assert saved_data == first.logger.turns

    second = ChatBot(system_prompt="Assistant B")
    second.resume(str(filename))
    assert second.history[0] == {"role": "system", "content": "Assistant B"}
    assert second.history[1:] == first.history[1:]
    assert second.logger.turns == first.logger.turns


def test_malformed_json_does_not_change_existing_memory(tmp_path):
    bot = ChatBot(system_prompt="Original")
    bot.add_turn("user", "Keep this message.")
    history_before = [item.copy() for item in bot.history]
    log_before = [item.copy() for item in bot.logger.turns]
    filename = tmp_path / "broken.json"
    filename.write_text("{not valid JSON", encoding="utf-8")
    with pytest.raises(ValueError, match="Unable to load"):
        bot.resume(str(filename))
    assert bot.history == history_before
    assert bot.logger.turns == log_before


def test_invalid_saved_turn_does_not_partially_restore(tmp_path):
    bot = ChatBot(system_prompt="Original")
    bot.add_turn("user", "Keep this message.")
    before = [item.copy() for item in bot.history]
    filename = tmp_path / "bad_turn.json"
    filename.write_text(json.dumps([
        {"role": "user", "content": "valid"},
        {"role": "system", "content": "not allowed"},
    ]), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid turn 1"):
        bot.resume(str(filename))
    assert bot.history == before


def test_file_must_contain_list(tmp_path):
    filename = tmp_path / "wrong_shape.json"
    filename.write_text('{"role": "user"}', encoding="utf-8")
    with pytest.raises(ValueError, match="JSON list"):
        load_conversation(str(filename))


def test_missing_conversation_file_reports_error(tmp_path):
    with pytest.raises(ValueError, match="Unable to load"):
        load_conversation(str(tmp_path / "missing.json"))
