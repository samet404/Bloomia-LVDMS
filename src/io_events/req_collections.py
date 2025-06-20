from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient

from src.helpers.notify_about_milvus import send_list_collections

def req_collections(socketio: SocketIO, session_id: str, milvus: MilvusClient):
    @socketio.on('req_collections')
    def req_collections():
        send_list_collections(socketio, session_id, milvus)