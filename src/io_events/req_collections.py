from flask import session
from flask_socketio import SocketIO
from src.helpers.notify_about_milvus import send_list_collections

def req_collections(socketio: SocketIO):
    @socketio.on('req_collections')
    def req_collections():
        session_id = session["auth_session"]
        send_list_collections(session_id)