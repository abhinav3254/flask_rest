import psycopg2

# Configuration for the PostgreSQL database
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'flask'
DB_USER = 'postgres'
DB_PASSWORD = 'root3254'


def create_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn
