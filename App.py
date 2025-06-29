# ==============================================================================
# This file is the entry point of the application
# ==============================================================================

from flask import Flask
from pymilvus import MilvusClient
from configuration import conf
from src.Logger import logger
from flask_socketio import SocketIO
from flask_cors import CORS
from src.db.postgresql import close_main_postgresql
from src.io_events.on_connect import on_connect as on_socketio_connect
import atexit

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(cors_allowed_origins=conf.allowed_origins)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app)  # Enable CORS for all io_events
    socketio.init_app(app)

    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    logger.info('=================================================\n')
    logger.info('WELCOME TO BLOOMIA GAIS (General AI Server)\n')
    logger.info('=================================================\n')

    logger.info('Checking is milvus is running...')
    try:
        logger.info('\nConnecting to Main Milvus...')
        main_milvus_client = MilvusClient(
            uri=conf.milvus_uri,
        )
        logger.info('Looks like Milvus is running...')
    except Exception as e:
        logger.error(f"Error connecting to Main Milvus: {str(e)}")
        raise Exception(f"Error connecting to Main Milvus: {str(e)}")

    on_socketio_connect(socketio)

    logger.info('Starting Flask server at http://localhost:' + str(conf.port))
    logger.info('Server started successfully.')

    socketio.run(app=app,
                 host='0.0.0.0',
                 port=conf.port,
                 debug=False)  # Set to False in production


    def cleanup():
        # Your cleanup code here
        logger.info('Exiting...')
        logger.info('Performing cleanup...')
        close_main_postgresql()
        logger.info('Cleanup complete.')

    atexit.register(cleanup)
