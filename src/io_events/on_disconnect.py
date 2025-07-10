import logging

from flask import request, session
from flask_socketio import SocketIO
from src.db.milvus import delete_milvus_client
from src.db.postgresql import remove_main_postgresql_cursor

def on_disconnect(socketio: SocketIO):
    @socketio.on('disconnect')
    def handle_disconnect(reason):
        logging.info(f'USER DISCONNECTED CLEANING UP \n session_id: {request.sid} | auth_session_id: {session.get("auth_session", None)} | reason: {reason}')
        auth_session = session.get("auth_session", None)
        user_id = session.get("user_id", None)

        if auth_session is None or user_id is None:
            logging.error("AUTH SESSION NOT FOUND ON DISCONNECT")
            return

        remove_main_postgresql_cursor(auth_session, request.sid)
        delete_milvus_client(user_id, request.sid)
