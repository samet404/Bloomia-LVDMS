import logging
from flask import session
from flask_socketio import SocketIO
from src.data_classes import CollectionStatsInput
from src.helpers.notify_about_milvus import send_collection_stats
from src.helpers.socketio_helpers import send_io_client_error

def req_collection_stats(socketio: SocketIO):
    @socketio.on('req_collection_stats')
    def run(json):
        try:
            session_id = session["auth_session"]
            input = json.loads(str(json))
            input = CollectionStatsInput(**input)

            send_collection_stats(input.collection_name, session_id)
        except Exception as e:
            logging.error(f"Error getting collection stats: {str(e)}")
            send_io_client_error(socketio, "Error getting collection stats.", session_id)