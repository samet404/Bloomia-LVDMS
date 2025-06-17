from pymilvus import MilvusClient

from configuration import conf
from src.Logger import logger

logger.info('\nConnecting to Milvus...')
milvus_client = MilvusClient(
    uri=conf.milvus_uri,
)
