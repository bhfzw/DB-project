# DB-project
# Мануал по запуску проекта

## Предварительные требования
- Ubuntu/Linux система
- Установленный Python 3.12
- Установленный MySQL

## Полная последовательность команд для запуска

# 1. Запуск и настройка MySQL сервера
sudo systemctl start mysql
sudo mysql -u root -p
CREATE DATABASE graduate_surveys;
CREATE USER 'web_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON graduate_surveys.* TO 'web_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
cd /путь/к/вашему/проекту/sql/init (Пример: cd downloads/DB-project/sql/init)
sudo mysql -u root -p graduate_surveys < complete_database_dump.sql

# 2. Установка venv (если не установлен)
sudo apt install python3.12-venv

# 3. Переход обратно в папку с проектом
cd ../путь/к/вашему/проекту

# 4. Создание виртуального окружения
python3 -m venv venv

# 5. Активация виртуального окружения
source venv/bin/activate

# 6. Установка необходимых пакетов
pip install mysql-connector-python flask flask-login python-dotenv reportlab

# 7. Запуск приложения
python app.py

# 8. Выход из проекта
ctrl + C 
deactivate
