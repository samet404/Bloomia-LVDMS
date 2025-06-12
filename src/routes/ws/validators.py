from pydantic import BaseModel


class CollectionStatsReq(BaseModel):
    collection_name: str = 'John Doe'


class AuthData(BaseModel):
    gemini_api_keys: list[str] = []


class CreateCollectionData(BaseModel):
    collection_name: str


class RemoveCollectionData(BaseModel):
    collection_name: str


class RecCollections(BaseModel):
    collections: list[str] = []


class ReqChatResponse(BaseModel):
    prompt: str
    model: str

class RecChatResponse(BaseModel):
    id: str
    text: str

class ChatHistory(BaseModel):
    text: str
    role: str

