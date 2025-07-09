import logging
from flask import request, session
from flask_socketio import emit, join_room, SocketIO
from configuration import conf
from src.auth import get_auth_session
from src.db.postgresql import  main_postgresql, main_postgresql_cursors
from src.helpers.socketio_helpers import send_io_client_error

def on_connect(socketio: SocketIO):
    @socketio.on('connect')
    def handle_connect():
        ip_address = request.headers.get('CF-Connecting-IP')
        if conf.is_prod:
            for i in range(10):
                logging.ERROR("CLOUDFLARE CLIENT IP HEADER NOT FOUND")
                raise Exception("CLOUDFLARE CLIENT IP HEADER NOT FOUND")
        else:
            # We are using google's ip address as a fallback for testing purposes
            ip_address = "8.8.8.8"

        try:
            better_auth_session_token = request.cookies.get("better-auth.session_token", None)

            logging.info(
                f"CONNECTION ESTABLISHED || sid: {request.sid} || IP: \n remote_addr: {request.remote_addr} | IP: {ip_address} | better_auth_session_token: {better_auth_session_token}")

            auth_session = get_auth_session(better_auth_session_token=better_auth_session_token)
            if auth_session is None:
                raise Exception('UNAUTHORIZED')

            logging.debug(f"sid: {request.sid} | auth_session_id: {auth_session.session.id} || auth_session_info: {auth_session.model_dump_json(indent=4)}")

            session["auth_info"] = auth_session
            session["auth_session"] = auth_session.session.id

            main_postgresql_cursors[session["auth_session"]] = main_postgresql.cursor()

            emit('connect-success')
            session["authorized"] = True
            join_room(session["auth_session"])
        except Exception as e:
            logging.error(f"User could not connect to server: {str(e)}")
            send_io_client_error(socketio, f"Could not connect to server.", request.sid)
