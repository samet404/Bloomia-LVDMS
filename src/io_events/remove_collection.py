import logging

from flask import session
from flask_socketio import SocketIO

from src.data_classes import RemoveCollectionInput
from src.db.milvus import milvus_clients
from src.helpers.socketio_helpers import send_io_client_error

def remove_collection(socketio: SocketIO):
    @socketio.on('remove_collection')
    def run(json):
       try:
           input = json.loads(str(json))
           input = RemoveCollectionInput(**input)
           input = input.model_dump()

           milvus_client = milvus_clients[session["auth_session"]]


           milvus_client.drop_collection(input.collection_name)
       except Exception as e:
            logging.error(f"Error removing collection: {str(e)}")
            send_io_client_error(socketio, "Error removing collection.", session_id)