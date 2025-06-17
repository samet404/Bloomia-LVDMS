from pydantic import BaseModel


class AuthData(BaseModel):
    gemini_api_keys: list[str] = []

class CollectionStatsReq(BaseModel):
    collection_name: str = 'John Doe'

class ReqChatResponse(BaseModel):
    prompt: str
    model: str

class RecChatResponse(BaseModel):
    id: str
    text: str

class ChatHistory(BaseModel):
    text: str
    role: str

