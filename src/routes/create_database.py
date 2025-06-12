from flask import Flask, request
from pymilvus import MilvusClient
from src.Logger import logger
from marshmallow import Schema, fields

class _RequestSchema(Schema):
    user_id = fields.String(required=True)

# https://milvus.io/docs/manage_databases.md
# Each user can have unique database
# This function creates a database for a user
def create_database(flask: Flask,  milvus: MilvusClient):
    @flask.route('/create-database', methods=['POST'])
    def create_database():
        logger.info('Route: /create-database called')
        schema = _RequestSchema()

        try:
            data = schema.load(request.get_json())

            milvus.create_database(
                db_name=data['user_id'] ,
            )

            logger.info('Route successful: /create-database')
            return 'Database created successfully', 200
        except Exception as e:
            logger.error(f'Route Error: /create-database - {str(e)}')
            return f'Error creating database: {str(e)}', 500

    @flask.route('/hello', methods=['GET'])
    def hello():
        logger.info('Route: /hello called')
        return 'Hello World!', 200
