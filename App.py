# ==============================================================================
# This file is the entry point of the application
# ==============================================================================

import atexit
from flask import Flask
from src.Logger import logger
from flask_cors import CORS
from src.db.milvus import init_milvus_client
from src.db.postgresql import close_main_postgresql, init_postgresql
from src.io_events.create import *
from src.io_events.on_connect import *
from src.io_events.on_disconnect import on_disconnect
from src.io_events.remove import *
from src.io_events.update import *

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
    init_milvus_client()
    logger.info('Looks like Milvus is running...')

    init_postgresql()
except Exception as e:
    logger.error(f"Error connecting to Main Milvus: {str(e)}")
    raise Exception(f"Error connecting to Main Milvus: {str(e)}")

on_connect(socketio)
on_disconnect(socketio)
create_file(socketio)
create_folder(socketio)
create_heading(socketio)
create_paragraph(socketio)
create_folder(socketio)
create_file_tag(socketio)
create_list_block(socketio)
create_list_block(socketio)
create_rag_collection_group(socketio)
add_rag_collection_to_blocks(socketio)

update_heading_block(socketio)
update_paragraph_block(socketio)
update_todo_block(socketio)
update_code_block(socketio)
update_list_block(socketio)
swap_block(socketio)

remove_heading_block(socketio)
remove_paragraph_block(socketio),
remove_todo_block(socketio)
remove_code_block(socketio)
remove_list_block(socketio)
remove_image_block(socketio)
remove_rag_collection_from_blocks(socketio)

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
