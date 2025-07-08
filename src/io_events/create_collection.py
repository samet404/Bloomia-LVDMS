import logging
from flask import session
from flask_socketio import SocketIO
from src.data_classes import CreateCollectionInput
from src.db.milvus import milvus_clients
from src.helpers.notify_about_milvus import send_list_collections, send_collection_stats
from src.helpers.socketio_helpers import send_io_client_error

def create_collection(socketio: SocketIO):
    @socketio.on('create_collection')
    def run(json):
       try:
           session_id = session["auth_session"]
           input = json.loads(str(json))
           input = CreateCollectionInput(**input)
           input.model_dump()

           milvus_clients[session_id].create_collection(
               collection_name=input.collection_name,
               dimension=1024,
               metric_type="IP",
               id_type='VARCHAR',
           )

           send_list_collections(session_id, socketio)
           send_collection_stats(input.collection_name, session_id, socketio)
       except Exception as e:
            logging.error(f"Error creating collection: {str(e)}")
            send_io_client_error(socketio, f"Error creating collection: {str(e)}")
