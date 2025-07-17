import logging
from flask import request, session
from flask_socketio import emit, join_room, SocketIO
from configuration import conf
from src.auth import get_auth_session
from src.db.milvus import create_milvus_client, default_milvus_client, get_default_milvus_client
from src.db.postgresql import set_main_postgresql_cursor
from src.helpers import event_err_server


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

            session["auth_session"] = auth_session
            session["user_id"] = auth_session.user.id

            set_main_postgresql_cursor(session[""], request.sid)

            init_milvus_database(session["user_id"])
            create_milvus_client(session["user_id"], request.sid)

            join_room(session["user_id"])
            emit('connect-success')
        except Exception as e:
            event_err_server("User could not connect to server")
            emit('connect-error', to=request.sid)


def init_milvus_database(user_id: str):
    existing_databases = get_default_milvus_client().list_databases()

    if user_id in existing_databases:
        logging.info(f"Milvus database for user {user_id} already exists")
        return

    get_default_milvus_client().create_database(
        db_name=user_id,
        description=f"Database for user {user_id}",
        properties={
            "database.diskQuota.mb": 500,
            "database.max.collections": 100,
        }
    )
