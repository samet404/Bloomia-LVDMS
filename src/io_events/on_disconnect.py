import logging

from flask import request, session
from flask_socketio import SocketIO
from src.db.postgresql import main_postgresql_cursors

def on_disconnect(socketio: SocketIO):
    @socketio.on('disconnect')
    def handle_disconnect(reason):
        # Destroy the main postgresql cursor for the user
        if main_postgresql_cursors.get(session.get("auth_session", None), None) is not None:
            main_postgresql_cursors[session.get("auth_session", None)].close()
            del main_postgresql_cursors[session.get("auth_session", None)]

        logging.info(f'USER DISCONNECTED CLEANING UP \n session_id: {request.sid} | auth_session_id: {session.get("auth_session", None)} | reason: {reason}')
