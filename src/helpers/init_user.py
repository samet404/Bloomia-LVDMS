from flask_socketio import SocketIO
from pymilvus import MilvusClient
from src.Logger import logger
from src.db.milvus import default_milvus_client
from src.helpers.socketio_helpers import send_io_client_error

# https://milvus.io/docs/manage_databases.md
# Each user can have unique database
# This function creates a database for a user
def create_database(socketio: SocketIO, session_id: str):
    try:
        logger.info(f"Milvus database is creating for user {session_id}...")

        all_databases = default_milvus_client.list_databases()
        if session_id in all_databases:
            logger.info(f"Milvus database for user {session_id} already exists")
            return

        milvus.create_database(
            db_name=session_id,
        )

        logger.info(f'Milvus database for user {session_id} created successfully')
        return 'Database created successfully', 200
    except Exception as e:
        logger.error(f'Error happened when creating database - {str(e)}')
        send_io_client_error(socketio, f"Error creating database: {str(e)}")


def init_socketio_connection(session_id, socketio: SocketIO):
    create_database(socketio, session_id)