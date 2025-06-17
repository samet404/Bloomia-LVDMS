from flask import Flask, request
from flask_socketio import SocketIO
from pydantic import BaseModel
from pymilvus import MilvusClient
from src.Logger import logger


# https://milvus.io/docs/manage_databases.md
# Each user can have unique database
# This function creates a database for a user
def create_database(socketio: SocketIO,  milvus: MilvusClient):
    @socketio.on('/create-database')
    def create_database(json):
        logger.info('Route: /create-database called')
        input = json.loads(str(input))
        input = _RequestSchema(**input)

        try:
            milvus.create_database(
                db_name=data['user_id'] ,
            )

            logger.info('Route successful: /create-database')
            return 'Database created successfully', 200
        except Exception as e:
            logger.error(f'Route Error: /create-database - {str(e)}')
            return f'Error creating database: {str(e)}', 500
