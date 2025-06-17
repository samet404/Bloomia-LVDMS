# ==============================================================================
# This file is the entry point of the application
# ==============================================================================

from flask import Flask
from pymilvus import MilvusClient

from configuration import conf
from src.Logger import logger
from flask_socketio import SocketIO
from flask_cors import CORS
from src.io_events.on_connect import on_connect as on_socketio_connect

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(cors_allowed_origins=conf.allowed_origins)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app)  # Enable CORS for all io_events
    socketio.init_app(app)

    logger.info('=================================================\n')
    logger.info('WELCOME TO BLOOMIA GAIS (General AI Server)\n')
    logger.info('=================================================\n')

    logger.info('Configuration:')
    for key in conf:
        logger.info(f'{key}: {conf[key]}')

    print("\nCreating Flask app...")
    flask = create_app()

    on_socketio_connect(socketio)

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    logger.info('Starting Flask server at http://localhost:' + str(conf.port))
    socketio.run(app=app,
                host='0.0.0.0', # 0.0.0.0 is for external access
                port=conf.port,
                debug=True)
