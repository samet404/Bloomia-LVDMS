from dataclasses import dataclass
from typing import List, Literal

@dataclass
class ChatHistory:
    id: str
    text: str
    role: Literal["user", "assistant", "system-error", "system-info", "system-warn"]

class ChatHistoryStore:
    def __init__(self):
        self.chat_history: List[ChatHistory] = []

    def add_chat_history(self, text: str, role: Literal["user", "assistant", "system-error", "system-info", "system-warn"]):
        self.chat_history.append(ChatHistory(text=text, role=role))

    def remove_chat_history(self, index: int):
        del self.chat_history[index]