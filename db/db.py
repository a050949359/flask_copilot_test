import os
import sqlite3
try:
    import pymysql
except ImportError:
    pymysql = None
from dotenv import load_dotenv
from db.user_sql import USER_SQL
from db.message_sql import MESSAGE_SQL

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

# SQL 語法集中管理
SQL_REGISTRY = {
    'user': USER_SQL,
    'message': MESSAGE_SQL,
}

def get_sql(resource, key):
    """取得指定資源的 SQL 語法"""
    return SQL_REGISTRY[resource][key]

def init_db():
    if DB_TYPE == 'sqlite':
        conn = sqlite3.connect(SQLITE_DB)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
        conn.commit()
        conn.close()
    elif DB_TYPE == 'mysql' and pymysql:
        conn = pymysql.connect(**MYSQL_CONFIG)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS message (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                content TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        conn.commit()
        conn.close()
    else:
        raise RuntimeError('Unsupported DB_TYPE or missing pymysql')
