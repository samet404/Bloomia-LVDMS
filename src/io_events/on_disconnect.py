import logging
from flask_socketio import SocketIO
from src.ai_pool import ai_pool
from src.io_events_constants import RECEIVE_CHAT_MSG_FROM_POOL_EVENT

def on_disconnect(socketio: SocketIO, session_id: str, auth_session_id: str):
    @socketio.on('disconnect')
    def handle_disconnect():
        logging.info(f'USER DISCONNECTED FROM WEBSOCKET SERVER \n session_id: {session_id} | auth_session_id: {auth_session_id}')

        # Remove events from ai pool socketio handlers
        ai_pool.handlers['/'].pop(RECEIVE_CHAT_MSG_FROM_POOL_EVENT(session_id))