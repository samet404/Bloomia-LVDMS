from psycopg2 import sql

from src.db.postgresql import init_postgresql, main_postgresql
from src.helpers import get_user_postgresql_usage_in_bytes

init_postgresql()
cursor = main_postgresql.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS "user_quota" (
    "user_id" VARCHAR(100) NOT NULL PRIMARY KEY,
    "max_ai_token" INTEGER NOT NULL,
    "ai_token_usage" INTEGER NOT NULL,
    "max_main_disk_size" INTEGER NOT NULL,
    "main_disk_usage" INTEGER NOT NULL,
    "max_vectordb_disk_size" INTEGER NOT NULL,
    "vectordb_disk_usage" INTEGER NOT NULL
);

INSERT INTO "user_quota" ("user_id", "max_ai_token", "ai_token_usage", "max_main_disk_size", "main_disk_usage", "max_vectordb_disk_size", "vectordb_disk_usage")
VALUES ('user_id', 1000000, 0, 500, 0, 1000, 0);

""")

query = sql.SQL("SELECT max_main_disk_size, main_disk_usage FROM user_quota WHERE  user_id = %s")
cursor.execute(query, [
    "user_id"
])

result = cursor.fetchone()

print(result[0])

get_user_postgresql_usage_in_bytes("user_id", cursor)