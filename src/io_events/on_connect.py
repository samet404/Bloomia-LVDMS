import json
import logging

from flask import request
from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient
from typing import List
from src.io_events.create_collection import create_collection
from src.io_events.remove_collection import remove_collection
from src.io_events.req_collection_stats import req_collection_stats
from src.helpers.socketio_helpers import send_io_client_error
from src.stores.chat_history_store import ChatHistoryStore
from src.validators import *


def on_connect(socketio: SocketIO):
    @socketio.on('connect')
    def handle_connect(auth_data):
        try:
            session_id = request.sid
            if session_id is None:
                raise Exception('No session ID found')

            chat_history_store = ChatHistoryStore()

            auth_input = json.loads(str(auth_data))
            auth_input = AuthData(**auth_input)
            chat_history: List[ChatHistory] = []
            emit('connect-success')

            req_collection_stats(socketio, session_id)
            remove_collection(socketio, session_id)
            create_collection(socketio, session_id)
            chat_req_response(socketio)
        except Exception as e:
            logging.error(f"User could not connect to server: {str(e)}")
            send_io_client_error(socketio, f"Could not connect to server.", session_id)
