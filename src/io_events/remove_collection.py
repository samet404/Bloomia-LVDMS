import logging

from flask_socketio import SocketIO, emit
from pydantic import BaseModel
from pymilvus import MilvusClient
from src.helpers.socketio_helpers import send_io_client_error

class RemoveCollectionData(BaseModel):
    collection_name: str

def remove_collection(socketio: SocketIO, session_id: str, milvus: MilvusClient):
    @socketio.on('remove_collection')
    def run(json):
       try:
           input = json.loads(str(json))
           input = RemoveCollectionData(**input)
           input.model_dump()

           milvus.drop_collection(input.collection_name)
       except Exception as e:
            logging.error(f"Error removing collection: {str(e)}")
            send_io_client_error(socketio, "Error removing collection.", session_id)