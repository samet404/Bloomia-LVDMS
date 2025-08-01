import psycopg2

from configuration import conf
from src.Logger import logger
from psycopg2.extensions import cursor, connection

main_postgresql: connection | None = None

# This is a dictionary of cursors for each connected user
# Each user has a unique cursor and cursors are closed when the user disconnects
# str is sum of socket.io session_id and user's session_id
main_postgresql_cursors: dict[str, cursor] = {}

def get_main_postgresql_cursor(sio_sid) -> cursor:
    return main_postgresql_cursors[sio_sid]

def set_main_postgresql_cursor(sio_sid: str):
    main_postgresql_cursors[sio_sid] = main_postgresql.cursor()

def remove_main_postgresql_cursor(sio_sid):
    del main_postgresql_cursors[sio_sid]

def init_postgresql():
    global main_postgresql

    logger.info('\nConnecting to PostgreSQL...')
    main_postgresql = psycopg2.connect(
        f"dbname={conf.postgres_db} user={conf.postgres_user} password={conf.postgres_password} host={conf.postgres_host} port={conf.postgres_port}")
    main_postgresql.autocommit = True
    logger.info('Connected to PostgreSQL successfully.')

def close_main_postgresql():
    global main_postgresql
    main_postgresql.close()

init_postgresql()
