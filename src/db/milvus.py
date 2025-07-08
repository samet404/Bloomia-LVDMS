# ==============================================================================
# This file is responsible for creating, deleting and initializing Milvus clients
# ==============================================================================

from pymilvus import MilvusClient
from configuration import conf

milvus_clients: dict[str, MilvusClient] = {}

def create_milvus_client(user_id: str):
    milvus_clients[user_id] = MilvusClient(
        uri=conf.milvus_uri,
        db_name=user_id,
    )

def delete_milvus_client(user_id: str):
    del milvus_clients[user_id]