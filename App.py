# ==============================================================================
# This file is the entry point of the application
# ==============================================================================

from flask import Flask
from pymilvus import MilvusClient
from configuration import conf
from src.Logger import logger
from flask_socketio import SocketIO
from flask_cors import CORS
from src.db.postgresql import close_main_postgresql, init_postgresql
from src.io_events.create_collection import create_collection
from src.io_events.on_connect import on_connect as on_socketio_connect
import atexit
from src.io_events.on_disconnect import on_disconnect
from src.io_events.remove_collection import remove_collection
from src.io_events.req_collection_stats import req_collection_stats
from src.io_events.req_collections import req_collections

def create_app():
    logger.info('Creating flask app...')
    app = Flask(__name__)
    logger.info('Creating socketio app...')
    socketio = SocketIO(cors_allowed_origins=conf.allowed_origins)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app)  # Enable CORS for all io_events
    socketio.init_app(app)
    logger.info('app and socketio created successfully.')

    return app, socketio

app, socketio = create_app()

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

    init_postgresql()
except Exception as e:
    logger.error(f"Error connecting to Main Milvus: {str(e)}")
    raise Exception(f"Error connecting to Main Milvus: {str(e)}")

on_socketio_connect(socketio)
on_disconnect(socketio)
req_collection_stats(socketio)
remove_collection(socketio)
create_collection(socketio)
req_collections(socketio)

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
