import logging

from flask_socketio import SocketIO, emit
from src.helpers.notify_about_milvus import send_collection_stats
from src.helpers.socketio_helpers import send_io_client_error
from src.validators import CollectionStatsReq

def req_collection_stats(socketio: SocketIO, session_id: str):
    @socketio.on('req_collection_stats')
    def run(json):
        try:
            input = json.loads(str(json))
            input = CollectionStatsReq(**input)

            send_collection_stats(input.collection_name, session_id, socketio)
        except Exception as e:
            logging.error(f"Error getting collection stats: {str(e)}")
            send_io_client_error(socketio, "Error getting collection stats.", session_id)