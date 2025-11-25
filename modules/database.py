import mysql.connector
from flask import current_app
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

def get_db_config():
    """Получение конфигурации БД из настроек приложения"""
    return {
        'host': current_app.config.get('MYSQL_HOST', 'localhost'),
        'user': current_app.config.get('MYSQL_USER', 'web_user'),
        'password': current_app.config.get('MYSQL_PASSWORD', 'StrongPassword123!'),
        'database': current_app.config.get('MYSQL_DB', 'graduate_surveys'),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }

def get_raw_connection():
    """Получение прямого соединения с БД (без контекстного менеджера)"""
    config = get_db_config()
    return mysql.connector.connect(**config)

@contextmanager
def get_db_connection():
    """Контекстный менеджер для соединения с БД"""
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    try:
        yield conn
    except mysql.connector.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """Контекстный менеджер для работы с курсором"""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            yield cursor
            if commit:
                conn.commit()
        except mysql.connector.Error as e:
            conn.rollback()
            logger.error(f"Database cursor error: {e}")
            raise
        finally:
            cursor.close()

def execute_query(query, params=None, fetch=True):
    """Универсальная функция выполнения запросов"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            return None
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise
