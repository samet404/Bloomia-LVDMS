import json
from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient
from typing import List, Dict
from uuid import uuid4
from src.routes.ws.validators import *


def ws(socketio: SocketIO, milvus: MilvusClient):
    @socketio.on('connect', namespace='/ws')
    def handle_connect(auth_data):
        auth_input = json.loads(str(auth_data))
        auth_input = AuthData(**auth_input)

        chat_history: List[ChatHistory] = []

        emit('connect-success', namespace='/ws')

        @socketio.on('req_collection_stats', namespace='/ws')
        def get_collection_stats(json):
            input = json.loads(str(json))
            input = CollectionStatsReq(**input)

            stats = milvus.get_collection_stats(input.collection_name)

            emit('rec_collection_stats', str(json.dumps(stats, mode='json')), namespace='/ws')

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

            emit('rec_collections', json.dumps(result, mode='json'), namespace='/ws')

        @socketio.on('req_chat_response')
        def get_chat_response(json):
            id = uuid4()
            input = json.loads(str(json))
            input = ReqChatResponse(**input)

            full_response = ""


            chat_history.append(ChatHistory(text=input.prompt, role="user"))
            chat_history.append(ChatHistory(text=full_response, role="assistant"))

