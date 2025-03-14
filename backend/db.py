import mysql.connector
from mysql.connector import pooling
from config import Config

# Database Connection Pool
db_pool = pooling.MySQLConnectionPool(
    pool_name="chatbot_pool",
    pool_size=5,
    pool_reset_session=True,
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB
)

def get_db_connection():
    try:
        return db_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None
