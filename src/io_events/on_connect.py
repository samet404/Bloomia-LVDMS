import logging
from flask import request, session
from flask_socketio import emit, join_room, SocketIO
from configuration import conf
from src.auth import get_auth_session
from src.db.milvus import create_milvus_client, default_milvus_client
from src.db.postgresql import set_main_postgresql_cursor
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
            session["user_id"] = auth_session.user.id

            set_main_postgresql_cursor(session["auth_session"], request.sid)

            init_milvus_database(session["user_id"])
            create_milvus_client(session["user_id"], request.sid)

            emit('connect-success')
            session["authorized"] = True
            join_room(session["auth_session"])
        except Exception as e:
            logging.error(f"User could not connect to server: {str(e)}")
            emit('connect-error', to=request.sid)
            send_io_client_error(socketio, f"Could not connect to server.", request.sid)


def init_milvus_database(user_id: str):
    existing_databases = default_milvus_client.list_database()

    if user_id in existing_databases:
        logging.info(f"Milvus database for user {user_id} already exists")
        return

    default_milvus_client.create_database(
        db_name=user_id,
        description=f"Database for user {user_id}",
        properties={
            "database.diskQuota.mb": 500,
            "database.max.collections": 100,
        }
    )
