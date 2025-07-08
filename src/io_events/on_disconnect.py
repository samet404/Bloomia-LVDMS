import logging

from flask import request, session
from flask_socketio import SocketIO

def on_disconnect(socketio: SocketIO):
    @socketio.on('disconnect')
    def handle_disconnect():
        logging.info(f'USER DISCONNECTED \n session_id: {request.sid} | auth_session_id: {session["auth_session"]}')
