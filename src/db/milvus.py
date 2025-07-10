# ==============================================================================
# This file is responsible for creating, deleting and initializing Milvus clients
# ==============================================================================

from pymilvus import MilvusClient
from configuration import conf

default_milvus_client = None

# This is a dictionary of Milvus clients for each connected user
milvus_clients: dict[str, MilvusClient] = {}

def create_milvus_client(user_id: str, sio_session_id: str):
    milvus_clients[f"{user_id}_{sio_session_id}"] = MilvusClient(
        uri=conf.milvus_uri,
        db_name=user_id
    )

def get_milvus_client(user_id: str, sio_session_id: str):
    return milvus_clients[f"{user_id}_{sio_session_id}"]

def delete_milvus_client(user_id: str, sio_session_id: str):
    del milvus_clients[f"{user_id}_{sio_session_id}"]

def init_milvus_client():
    global default_milvus_client
    default_milvus_client = MilvusClient(
        uri=conf.milvus_uri,
    )