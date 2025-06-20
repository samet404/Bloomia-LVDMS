import logging

from flask_socketio import SocketIO, emit
from pymilvus import MilvusClient
from src.data_classes import CreateCollectionInput
from src.helpers.notify_about_milvus import send_list_collections, send_collection_stats
from src.helpers.socketio_helpers import send_io_client_error

def create_collection(socketio: SocketIO, session_id: str, milvus_client: MilvusClient):
    @socketio.on('create_collection')
    def run(json):
       try:
           input = json.loads(str(json))
           input = CreateCollectionInput(**input)
           input.model_dump()

           milvus_client.create_collection(
               collection_name=input.collection_name,
               dimension=1024,
               metric_type="IP",
               id_type='VARCHAR',
           )

           send_list_collections(socketio, session_id)
           send_collection_stats(input.collection_name, session_id, socketio)
       except Exception as e:
            logging.error(f"Error creating collection: {str(e)}")
            send_io_client_error(socketio, f"Error creating collection: {str(e)}")
