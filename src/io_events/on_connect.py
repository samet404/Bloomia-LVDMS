import json
import logging
from flask import request
from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient
from configuration import conf
from src.ai_pool import ai_pool
from src.auth import get_auth_session
from src.io_events import send_chat_msg
from src.io_events.create_collection import create_collection
from src.io_events.remove_collection import remove_collection
from src.io_events.req_collection_stats import req_collection_stats
from src.helpers.socketio_helpers import send_io_client_error
from src.io_events.req_collections import req_collections
from src.stores.chat_history_store import ChatHistoryStore, ChatHistory

def on_connect(socketio: SocketIO):
    @socketio.on('connect')
    def handle_connect():
        session_id = request.sid
        if session_id is None:
            raise Exception('No socket.io session ID found')

        try:
            cloudflare_ip = request.headers.get('CF-Connecting-IP')
            logging.info(
                f"CONNECTION ESTABLISHED WITH IP: \n remote_addr: {request.remote_addr} | cloudflare_ip: {cloudflare_ip}")

            # ==============================================================================
            # STATE
            # ==============================================================================
            session = get_auth_session(better_auth_session_token=request.cookies.get("better-auth.session_token"))
            if session is None:
                raise Exception('UNAUTHORIZED')

            auth_session_id = session.session.id
            chat_history_store = ChatHistoryStore()
            logging.info(f"Connecting to Milvus client for user {auth_session_id}")
            milvus_client = MilvusClient(
                uri=conf.milvus_uri,
                db_name="<USER_ID_HERE>",
            )

            # ==============================================================================
            # INITIALIZE EVENTS
            # ==============================================================================

            req_collection_stats(socketio, session_id, milvus_client)
            remove_collection(socketio, session_id, milvus_client)
            create_collection(socketio, session_id, milvus_client)
            req_collections(socketio, session_id, milvus_client)
            send_chat_msg(socketio, session_id, milvus_client)




            # ==============================================================================
            # SEND SUCCESS MESSAGE
            # ==============================================================================
            emit('connect-success')
        except Exception as e:
            logging.error(f"User could not connect to server: {str(e)}")
            send_io_client_error(socketio, f"Could not connect to server.", session_id)
