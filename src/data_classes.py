from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class User:
    id: str
    is_active: bool = True



class SendMessageInput(BaseModel):
    prompt: str
    model: str
    chat_id: str
    include_collections: list[str]
    include_note_ids: list[str]
    include_notes: list[str]


class OnChatMsgMetadata(BaseModel):
    chat_id: str
