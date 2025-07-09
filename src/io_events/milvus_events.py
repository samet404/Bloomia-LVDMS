import json
import logging
from flask import session
from flask_socketio import SocketIO
from pydantic import BaseModel
from src.db.milvus import milvus_clients
from src.db.postgresql import main_postgresql_cursors
from src.helpers.socketio_helpers import send_io_client_error


class CreateCollectionInput(BaseModel):
    collection_name: str

def create_collection(socketio: SocketIO):
    @socketio.on('create_collection')
    def run(json):
       try:
           try:
               session_id = session["auth_session"]
               input = json.loads(str(json))
               input = CreateCollectionInput(**input)
               input.model_dump()



               send_list_collections(session_id, socketio)
               send_collection_stats(input.collection_name, session_id, socketio)
           except Exception as e:
               logging.error(f"Error creating collection: {str(e)}")
               send_io_client_error(socketio, f"Error creating collection: {str(e)}")
        except Exception as e:
            logging.error(f"UNAUTHORIZED create_collection: {str(e)}")
            send_io_client_error(socketio, f"UNAUTHORIZED create_collection", request.sid)

class RemoveCollectionInput(BaseModel):
    collection_name: str

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

class CollectionStatsInput(BaseModel):
    collection_name: str

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

def notify_about_files(session_id: str, socketio: SocketIO):
    try:
        main_postgresql_cursors[session_id].execute("""
            SELECT * FROM File WHERE user_id = %%s ORDER BY created_at DESC 
        """, (session_id,))

        for row in main_postgresql_cursors[session_id]:
            print(row)
    except Exception as e:
        logging.error(f"Error getting list of files: {str(e)}")
        send_io_client_error(socketio, "Error getting list of files.", session_id)