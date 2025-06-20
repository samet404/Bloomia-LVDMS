import psycopg2
from configuration import conf
from src.Logger import logger

logger.info('\nConnecting to PostgreSQL...')
main_postgresql = psycopg2.connect(
    f"dbname={conf.postgres_db} user={conf.postgres_user} password={conf.postgres_password} host={conf.postgres_host} port={conf.postgres_port}")
main_postgres_cur = main_postgresql.cursor()

def close_main_postgresql():
    main_postgres_cur.close()
    main_postgresql.close()