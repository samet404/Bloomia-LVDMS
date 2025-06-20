from flask import Flask, request
from flask_socketio import SocketIO
from pydantic import BaseModel
from pymilvus import MilvusClient
from src.Logger import logger
from src.helpers.socketio_helpers import send_io_client_error


# https://milvus.io/docs/manage_databases.md
# Each user can have unique database
# This function creates a database for a user
def create_database(socketio: SocketIO, user_id: str, milvus: MilvusClient):
    try:
        logger.info(f"Milvus database is creating for user {user_id}...")

        all_databases = milvus.list_databases()
        if user_id in all_databases:
            logger.info(f"Milvus database for user {user_id} already exists")

            return

        milvus.create_database(
            db_name=user_id,
        )

        logger.info('Milvus database for user {user_id} created successfully')
        return 'Database created successfully', 200
    except Exception as e:
        logger.error(f'Route Error: /create-database - {str(e)}')
        send_io_client_error(socketio, f"Error creating database: {str(e)}")


def init_socketio_connection(user_id, milvus: MilvusClient):
    create_database(user_id, milvus)