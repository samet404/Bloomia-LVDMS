import logging

from flask_socketio import SocketIO, emit
from pydantic import BaseModel
from pymilvus import MilvusClient

from src.helpers.socketio_helpers import send_error


class CreateCollectionData(BaseModel):
    collection_name: str

def create_collection(socketio: SocketIO, session_id: str, milvus: MilvusClient):
    @socketio.on('create_collection')
    def run(json):
       try:
           input = json.loads(str(json))
           input = CreateCollectionData(**input)
           input.model_dump()

           milvus.create_collection(
               collection_name=input.collection_name,
               dimension=1024,
               metric_type="IP",
               id_type='VARCHAR',
           )
       except Exception as e:
            logging.error(f"Error creating collection: {str(e)}")
            send_error(socketio, f"Error creating collection: {str(e)}")
