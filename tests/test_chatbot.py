"""Week 7: example tests for the ChatBot class (runs offline via FakeLLM)."""

import pytest

from ribot.chatbot import DEFAULT_SYSTEM, ChatBot, ConversationLogger, main


@pytest.fixture(autouse=True)
def use_fake_llm(monkeypatch):
    # Override configured backends so this module cannot make real model calls.
    monkeypatch.setenv("OPENAI_API_KEY", " ")
    monkeypatch.setenv("RIBOT_LLM", "fake")
    monkeypatch.setenv("RIBOT_EMBED", "fake")


def _run_terminal(monkeypatch, inputs):
    bot = ChatBot()
    entries = iter(inputs)
    monkeypatch.setattr("ribot.chatbot.ChatBot", lambda: bot)
    monkeypatch.setattr("builtins.input", lambda prompt: next(entries))
    main()
    return bot


def test_terminal_two_turns_and_show_history(monkeypatch, capsys):
    bot = _run_terminal(
        monkeypatch, ["  My name is Katie.  ", "What's my name?", "/show", "/exit"]
    )
    output = capsys.readouterr().out
    assert [m["role"] for m in bot.history] == [
        "system", "user", "assistant", "user", "assistant"
    ]
    assert bot.history[1]["content"] == "My name is Katie."
    assert bot.history[3]["content"] == "What's my name?"
    assert "You told me earlier — your name is Katie." in bot.history[4]["content"]
    assert bot.logger.turns == bot.history[1:]
    assert output.count("bot > ") == 2
    for message in bot.history:
        assert f"[{message['role']}] {message['content']}" in output
    assert output.endswith("bye!\n")


def test_terminal_exit_stops_without_recording_or_calling_model(monkeypatch, capsys):
    def unexpected_call(messages):
        pytest.fail("Exit must not call the model")

    monkeypatch.setattr("ribot.chatbot.chat", unexpected_call)
    bot = _run_terminal(monkeypatch, ["  /exit  ", "must not be read"])
    assert bot.history == [{"role": "system", "content": DEFAULT_SYSTEM}]
    assert bot.logger.turns == []
    assert capsys.readouterr().out.endswith("bye!\n")


@pytest.mark.parametrize("empty", ["", "   ", "\t  "])
def test_terminal_skips_empty_input_and_continues(monkeypatch, capsys, empty):
    bot = _run_terminal(monkeypatch, [empty, "My name is Mike.", "/exit"])
    assert len(bot.history) == 3
    assert bot.history[1] == {"role": "user", "content": "My name is Mike."}
    assert len(bot.logger.turns) == 2
    assert capsys.readouterr().out.count("bot > ") == 1


def test_terminal_unknown_command_reports_help_and_continues(monkeypatch, capsys):
    bot = _run_terminal(monkeypatch, ["/unknown", "My name is Mike.", "/exit"])
    output = capsys.readouterr().out
    assert "Unknown command: /unknown" in output
    assert "Use /show to see memory or /exit to quit." in output
    assert len(bot.history) == 3
    assert bot.history[1]["content"] == "My name is Mike."
    assert len(bot.logger.turns) == 2
    assert output.count("bot > ") == 1


def test_default_profile_defines_role_users_and_tone():
    bot = ChatBot()
    assert bot.history[0] == {"role": "system", "content": DEFAULT_SYSTEM}
    assert "offline document retrieval and reference assistant" in DEFAULT_SYSTEM
    assert "Katie and Mike" in DEFAULT_SYSTEM
    assert "clear, friendly, concise, and practical" in DEFAULT_SYSTEM


def test_default_profile_requires_grounding_and_honest_limits():
    for rule in (
        "only files deliberately placed in the approved",
        "Do not access unauthorized private files",
        "you do not have unrestricted computer access",
        "concise, source-grounded answers",
        "when supporting retrieval information and its filename are actually available",
        "Never invent facts, filenames, quotations, or citations",
        "If information is missing or insufficient, say so",
        "Never claim to have searched or retrieved documents that were not actually searched",
        "it does not enable file access",
        "document retrieval, or offline model execution",
    ):
        assert rule in DEFAULT_SYSTEM


def test_default_profile_and_context_are_sent_on_follow_up(monkeypatch):
    calls = []

    def capture_chat(messages):
        calls.append([message.copy() for message in messages])
        return "Please provide the approved document."

    monkeypatch.setattr("ribot.chatbot.chat", capture_chat)
    bot = ChatBot()
    first_answer = bot.reply("Help me find generator instructions.")
    bot.reply("What are the startup steps?")
    assert "Use the conversation history to maintain context" in DEFAULT_SYSTEM
    assert calls[1] == [
        {"role": "system", "content": DEFAULT_SYSTEM},
        {"role": "user", "content": "Help me find generator instructions."},
        {"role": "assistant", "content": first_answer},
        {"role": "user", "content": "What are the startup steps?"},
    ]
    bot.reset()
    assert bot.history == [{"role": "system", "content": DEFAULT_SYSTEM}]


def test_history_starts_with_system_message():
    bot = ChatBot(system_prompt="You are a test bot.")
    assert bot.history[0] == {"role": "system", "content": "You are a test bot."}


def test_add_turn_appends_to_history():
    bot = ChatBot()
    before = len(bot.history)
    bot.add_turn("user", "hi")
    assert len(bot.history) == before + 1
    assert bot.history[-1] == {"role": "user", "content": "hi"}


def test_reply_records_user_and_assistant():
    bot = ChatBot()
    answer = bot.reply("hello")
    assert isinstance(answer, str) and answer
    assert bot.history[-2]["role"] == "user"
    assert bot.history[-1]["role"] == "assistant"


def test_reset_keeps_only_system():
    bot = ChatBot()
    bot.reply("hello")
    bot.reset()
    assert len(bot.history) == 1


def test_logger_records_turns():
    logger = ConversationLogger()
    logger.log("user", "hi")
    assert logger.turns == [{"role": "user", "content": "hi"}]


def test_memory_recalls_name_when_history_is_kept():
    # The Week 1/3 memory demo: with history kept, the bot recalls your name.
    bot = ChatBot()
    bot.reply("My name is Sam.")
    answer = bot.reply("What's my name?")
    assert "Sam" in answer


def _tiny_retriever():
    # A two-chunk index, built the same way Week 6's build_index does it.
    from ribot.embeddings import fallback_embed
    from ribot.retriever import Retriever
    from ribot.vectorstore import InMemoryStore

    store = InMemoryStore()
    chunks = [
        "Vacation policy: full-time employees receive 15 vacation days per year.",
        "To reset your password, open the IT portal and choose 'Forgot password'.",
    ]
    store.add(
        ids=["policy.md:0", "it_faq.md:0"],
        documents=chunks,
        embeddings=[fallback_embed(c) for c in chunks],
    )
    return Retriever(store, embed_fn=fallback_embed)


def test_reply_grounded_cites_a_source():
    # Week 7 floor: the grounded reply must carry a [source: ...] citation.
    bot = ChatBot()
    answer = bot.reply_grounded("How many vacation days do employees get?", _tiny_retriever())
    assert "[source:" in answer


def test_reply_grounded_refuses_on_empty_index():
    # No documents indexed -> the honest answer is "I don't know", not an invention.
    from ribot.embeddings import fallback_embed
    from ribot.retriever import Retriever
    from ribot.vectorstore import InMemoryStore

    bot = ChatBot()
    empty = Retriever(InMemoryStore(), embed_fn=fallback_embed)
    answer = bot.reply_grounded("What is the vacation policy?", empty)
    assert "don't know" in answer.lower()


def test_memory_forgets_without_history():
    # The "goldfish" case: if earlier turns are NOT in messages, the bot can't know.
    from ribot.llm import chat

    answer = chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is my name?"},
        ]
    )
    assert "don't know" in answer.lower()
