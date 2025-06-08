import json
from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient
from pydantic import BaseModel, PositiveInt
from google import genaix
from typing import List, Dict
from uuid import uuid4

from src.helpers.GeminiClientPool import GeminiClientPool


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


def ws(socketio: SocketIO, milvus: MilvusClient):
    @socketio.on('connect', namespace='/ws')
    def handle_connect(auth_data):
        auth_input = json.loads(str(auth_data))
        auth_input = AuthData(**auth_input)

        chat_history: List[ChatHistory] = []
        gemini_pool = GeminiClientPool(auth_input.gemini_api_keys)

        emit('connect-success', namespace='/ws')

        @socketio.on('req_collection_stats', namespace='/ws')
        def get_collection_stats(json):
            input = json.loads(str(json))
            input = CollectionStatsReq(**input)

            stats = milvus.get_collection_stats(input.collection_name)

            emit('rec_collection_stats', json.dumps(stats), namespace='/ws')

        @socketio.on('create_collection', namespace='/ws')
        def create_collection(json):
            input = json.loads(str(json))
            input = CreateCollectionData(**input)
            input.model_dump()

            milvus.create_collection(
                collection_name=input.collection_name,
                dimension=1024,
                metric_type="IP",
                id_type='VARCHAR',
            )

        @socketio.on('remove_collection', namespace='/ws')
        def remove_collection(json):
            input = json.loads(str(json))
            input = RemoveCollectionData(**input)
            input.model_dump()

            milvus.drop_collection(input.collection_name)

        @socketio.on('req_collections', namespace='/ws')
        def get_collections():
            collections = milvus.list_collections()
            result = RecCollections(collections=collections)

            emit('rec_collections', json.dumps(result), namespace='/ws')

        @socketio.on('req_chat_response')
        def get_chat_response(json):
            id = uuid4()
            input = json.loads(str(json))
            input = ReqChatResponse(**input)

            full_response = ""
            for chunk in gemini_pool.getResponse(input.model, """
                SYSTEM INSTRUCTIONS:
                You are an AI assistant. You are able to find answers to the questions from provided context. If you don't know the answer, just say that you don't know. If question is not clear, ask for clarification.
                
                CONTEXT:
                {input.prompt}
                
                QUESTION:
                {input.prompt}
            """):
                response = RecChatResponse(id=str(id), text=chunk.text)
                emit('rec_chat_response',response.model_dump()  , namespace='/ws')
                full_response += chunk.text

            chat_history.append(ChatHistory(text=input.prompt, role="user"))
            chat_history.append(ChatHistory(text=full_response, role="assistant"))
