import psycopg2

from configuration import conf
from src.Logger import logger

main_postgresql: psycopg2.extensions.connection = None

def init_postgresql():
    logger.info('\nConnecting to PostgreSQL...')
    psycopg2.connect(
        f"dbname={conf.postgres_db} user={conf.postgres_user} password={conf.postgres_password} host={conf.postgres_host} port={conf.postgres_port}")
    logger.info('Connected to PostgreSQL successfully.')

def close_main_postgresql():
    main_postgresql.close()
