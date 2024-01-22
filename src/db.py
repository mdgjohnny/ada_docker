import os
import mysql.connector
from mysql.connector import pooling, Error
import logging


db_config = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME", "myappdb"),
    "user": os.getenv("DB_USER", "ada"),
    "password": os.getenv("DB_PASSWORD", "test"),
}

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info(f"Db config: {db_config}")


connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_connection():
    try:
        return connection_pool.get_connection()
    except Error as e:
        logger.error(f"Error getting connection from pool: {e}")
        raise

def execute_query(query, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor(buffered=True) as cursor:
                logger.info(f"Executing query: {query}")
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                conn.commit()
    except Error as e:
        logger.error(f"Error executing query: {e}")
        raise

def check_and_create_tables():
    check_and_create_table_query = """
        CREATE TABLE IF NOT EXISTS api_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    execute_query(check_and_create_table_query)
    logger.info("Creating table")

def teardown_database():
    drop_table_query = "DROP TABLE IF EXISTS api_data;"
    execute_query(drop_table_query)
    print("Database teardown completed: 'api_data' table dropped.")

def insert_joke(joke):
    insert_query = "INSERT INTO api_data (data) VALUES (%s)"
    execute_query(insert_query, (joke,))

def get_jokes(count=1):
    select_query = f"SELECT data FROM api_data ORDER BY RAND() LIMIT {count}"
    result = execute_query(select_query)
    return [row[0] for row in result] if result else []

def get_total_jokes():
    get_total_jokes_query = """
        SELECT COUNT(*) FROM api_data;
    """
    total = execute_query(get_total_jokes_query)
    logger.info(f"Total jokes: {total}")
    total_jokes = total[0][0]
    return total_jokes if total else 0

check_and_create_tables()
