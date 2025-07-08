import json
import logging

from flask_socketio import SocketIO

from src.db.milvus import milvus_clients
from src.helpers.socketio_helpers import send_io_client_error

def send_collection_stats(collection_name: str, session_id: str, socketio: SocketIO):
    try:
        if id not in milvus_clients:
            raise Exception(f"Milvus client for user {id} not found")
        stats = milvus_clients[session_id].get_collection_stats(collection_name)
        socketio.emit('rec_collection_stats', str(json.dumps(stats, mode='json')), to=session_id)
    except Exception as e:
        logging.error(f"Error getting collection stats: {str(e)}")
        send_io_client_error(socketio, "Error getting collection stats.", session_id)

def send_list_collections(session_id: str, socketio: SocketIO):
    try:
        collections = milvus_clients[session_id].list_collections()
        socketio.emit('rec_collections', json.dumps(collections, mode='json'), to=session_id)
    except Exception as e:
        logging.error(f"Error getting list of collections: {str(e)}")
        send_io_client_error(socketio, "Error getting list of collections.", session_id)

