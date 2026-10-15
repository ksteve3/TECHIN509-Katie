"""Weeks 1/3/7: the chatbot itself.

- Week 1: run it and watch it reply (offline FakeLLM works with no key).
- Week 3: the conversation 'memory' is just `self.history`, a list of {role, content} dicts.
- Week 7: this is refactored into a class with tests.
"""

from __future__ import annotations

from .llm import chat
from .textprep import export_to_json

DEFAULT_SYSTEM = """You are an offline document retrieval and reference assistant for Katie and Mike.
Use a clear, friendly, concise, and practical tone.

Prioritize approved local documents: only files deliberately placed in the approved
source folder may be searched or indexed. Do not access unauthorized private files,
credentials, or unrelated folders; you do not have unrestricted computer access.
Use the conversation history to maintain context and understand follow-up questions.

Provide concise, source-grounded answers using supporting document information
actually available in the conversation or supplied by retrieval. Identify the source
filename when supporting retrieval information and its filename are actually available,
using [source: filename]. Never invent facts, filenames, quotations, or citations.
If information is missing or insufficient, say so and ask for the relevant approved
document or clarification. Do not present general knowledge as a local document finding.
Never claim to have searched or retrieved documents that were not actually searched.

This profile describes the intended assistant; it does not enable file access,
document retrieval, or offline model execution. Do not claim those capabilities are
working unless the running application actually provides and verifies them.
"""


class ConversationLogger:
    """Records each turn so a whole session can be saved to JSON."""

    def __init__(self) -> None:
        self.turns: list[dict[str, str]] = []

    def log(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})

    def export(self, filename: str) -> None:
        export_to_json(self.turns, filename)


class ChatBot:
    """A multi-turn chatbot whose memory is a list of message dicts."""

    def __init__(self, system_prompt: str = DEFAULT_SYSTEM) -> None:
        self.history: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
        self.logger = ConversationLogger()

    def add_turn(self, role: str, content: str) -> None:
        """Append one message to the conversation memory."""
        self.history.append({"role": role, "content": content})
        self.logger.log(role, content)

    def reply(self, user_message: str) -> str:
        """Add the user's message, ask the model, remember and return the answer."""
        self.add_turn("user", user_message)
        answer = chat(self.history)
        self.add_turn("assistant", answer)
        return answer

    def reply_grounded(self, question: str, retriever, k: int = 3) -> str:
        """Answer `question` from retrieved evidence, citing each chunk's source file.

        Week 7 floor ("Part 2.5"): this is where "it answers from my documents"
        becomes real code. Three steps, all of them things you already know:
        1. retrieve: ask the Week 6 retriever for the top-k chunks,
        2. assemble: put those chunks into the prompt, each labeled with its source,
        3. reply: send it through the normal `reply()` path.
        The 'SEARCH RESULTS:' prefix is what the offline FakeLLM keys on to answer
        from the evidence (a real model just sees clearly labeled context).
        """
        hits = retriever.search(question, k=k)
        if not hits:
            return "I don't know — I couldn't find anything about that in your documents."
        evidence = "\n".join(
            f"[source: {retriever.source_of(chunk)}] {chunk}" for chunk, _score in hits
        )
        prompt = (
            f"SEARCH RESULTS:\n{evidence}\n\n"
            f"Answer using ONLY the search results above, and cite the source file "
            f"like [source: file.md]: {question}"
        )
        return self.reply(prompt)

    def reset(self) -> None:
        """Forget everything except the system prompt."""
        self.history = self.history[:1]


def main() -> None:
    """Terminal chat loop: type to talk, '/exit' to quit, '/show' to print memory."""
    bot = ChatBot()
    print("ribot is alive. Type a message, '/show' to see memory, '/exit' to quit.\n")
    while True:
        user = input("you > ").strip()
        if user == "/exit":
            break
        if user == "/show":
            for m in bot.history:
                print(f"  [{m['role']}] {m['content']}")
            continue
        if not user:
            continue
        if user.startswith("/"):
            print(f"Unknown command: {user}. Use /show to see memory or /exit to quit.\n")
            continue
        print(f"bot > {bot.reply(user)}\n")
    print("bye!")


if __name__ == "__main__":  # `python -m ribot.chatbot`
    main()
