from dataclasses import dataclass
from typing import List, Literal

@dataclass
class OpenedEvent:
    event_name: str

class OpenedAIPoolEventsStore:
    def __init__(self, session_id: str):
        self.events: List[OpenedEvent] = []
        self.session_id = session_id

    def add(self, event_name: str):
        self.events.append(OpenedEvent(event_name=event_name))
