# ==============================================================================
# This file is the entry point of the application
# ==============================================================================

from flask import Flask, request
from pymilvus import MilvusClient

from configuration import conf
from src.Logger import logger
from src.routes.create_database import create_database
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from src.routes.ws.ws import ws


def create_app():
    app = Flask(__name__)
    socketio = SocketIO(cors_allowed_origins=conf.allowed_origins)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app)  # Enable CORS for all routes
    socketio.init_app(app)

    logger.info('=================================================\n')
    logger.info('WELCOME TO BLOOMIA GAIS (General AI Server)\n')
    logger.info('=================================================\n')

    logger.info('Configuration:')
    for key in conf:
        logger.info(f'{key}: {conf[key]}')

    print("\nCreating Flask app...")
    flask = create_app()

    # Connect to Milvus
    logger.info('\nConnecting to Milvus...')
    milvus_client = MilvusClient(
        uri=conf["milvus_uri"]
    )

    # Register flask routes
    create_database(flask, milvus_client)
    ws(socketio, milvus_client)

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    logger.info('Starting Flask server at http://localhost:' + str(conf.port))
    socketio.run(app=app,
                host='0.0.0.0', # 0.0.0.0 is for external access
                port=conf.port,
                debug=True)
