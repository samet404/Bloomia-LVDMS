# ==============================================================================
# This file is the entry point of the application
# ==============================================================================

from flask import Flask, request
from pymilvus import MilvusClient

from Env import Env, EnvKey
from src.Logger import logger
from src.routes.create_database import create_database
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from src.routes.ws.ws import ws

socketio = SocketIO(cors_allowed_origins="*")  # Allow all origins

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app)  # Enable CORS for all routes
    socketio.init_app(app)
    return app

if __name__ == '__main__':
    logger.info('=================================================\n')
    logger.info('WELCOME TO BLOOMIA GAIS (General AI Server)\n')
    logger.info('=================================================\n')

    logger.info('ENVIRONMENT VARIABLES:')
    for key in EnvKey:
        logger.info(f'{key.value}: {Env(key)}')

    print("\nCreating Flask app...")
    flask= create_app()

    # Connect to Milvus
    logger.info('\nConnecting to Milvus...')
    milvus_client = MilvusClient(
        uri=Env(EnvKey.MILVUS_URI)
    )

    # Register flask routes
    create_database(flask, milvus_client)
    ws(socketio, milvus_client)

    logger.info('Starting Flask server at http://localhost:' + str(Env(EnvKey.PORT)))
    flask.run(debug=True, port=int(Env(EnvKey.PORT)))
