# memory/chat_memory.py

class ChatMemory:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.messages: list[dict] = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get(self) -> list[dict]:
        return self.messages.copy()