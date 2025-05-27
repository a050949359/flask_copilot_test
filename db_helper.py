import os
from dotenv import load_dotenv
import sqlite3
try:
    import pymysql
except ImportError:
    pymysql = None

load_dotenv()

DB_TYPE = os.getenv('DB_TYPE', 'sqlite')

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'app'),
    'charset': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
}

SQLITE_DB = os.getenv('SQLITE_DB', 'app.db')

def get_conn():
    if DB_TYPE == 'sqlite':
        return sqlite3.connect(SQLITE_DB)
    elif DB_TYPE == 'mysql' and pymysql:
        return pymysql.connect(**MYSQL_CONFIG)
    else:
        raise RuntimeError('Unsupported DB_TYPE or missing pymysql')

def is_integrity_error(e):
    if DB_TYPE == 'sqlite':
        return isinstance(e, sqlite3.IntegrityError)
    elif DB_TYPE == 'mysql' and pymysql:
        return isinstance(e, pymysql.err.IntegrityError)
    return False

def is_database_error(e):
    if DB_TYPE == 'sqlite':
        return isinstance(e, sqlite3.DatabaseError)
    elif DB_TYPE == 'mysql' and pymysql:
        return isinstance(e, pymysql.MySQLError)
    return False
