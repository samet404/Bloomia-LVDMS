# ==============================================================================
# This file is responsible for creating, deleting and initializing Milvus clients
# ==============================================================================

from pymilvus import MilvusClient
from configuration import conf

default_milvus_client: MilvusClient | None = None

# This is a dictionary of Milvus clients for each connected user
milvus_clients: dict[str, MilvusClient] = {}

def get_default_milvus_client() -> MilvusClient:
    if default_milvus_client is None:
        raise Exception("Default Milvus client is not initialized. Call init_milvus_client() first.")
    return default_milvus_client

def close_milvus_clients():
    if default_milvus_client is not None:
        default_milvus_client.close()

    for client in milvus_clients.values():
        client.close()

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