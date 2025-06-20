import json
import logging
from flask_socketio import SocketIO
from pymilvus import MilvusClient

from src.helpers.socketio_helpers import send_io_client_error

def send_collection_stats(collection_name: str,session_id: str, socketio: SocketIO,  milvus_client: MilvusClient):
    try:
        stats = milvus_client.get_collection_stats(collection_name)
        socketio.emit('rec_collection_stats', str(json.dumps(stats, mode='json')), to=session_id)
    except Exception as e:
        logging.error(f"Error getting collection stats: {str(e)}")
        send_io_client_error(socketio, "Error getting collection stats.", session_id)

def send_list_collections(socketio: SocketIO, session_id: str, milvus_client: MilvusClient):
    try:
        collections = milvus_client.list_collections()
        socketio.emit('rec_collections', json.dumps(collections, mode='json'), to=session_id)
    except Exception as e:
        logging.error(f"Error getting list of collections: {str(e)}")
        send_io_client_error(socketio, "Error getting list of collections.", session_id)

