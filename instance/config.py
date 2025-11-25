import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2024'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'web_user'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'StrongPassword123!'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'graduate_surveys'
    
    # Настройки сессии
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 час
