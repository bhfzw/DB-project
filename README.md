# DB-project
# Мануал по запуску проекта

## Предварительные требования
- Ubuntu/Linux система
- Установленный Python 3.12
- Установленный MySQL

## Полная последовательность команд для запуска

# 1. Запуск MySQL сервера
sudo systemctl start mysql

# 2. Установка venv (если не установлен)
sudo apt install python3.12-venv

# 3. Переход в папку с проектом
cd /путь/к/вашему/проекту

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
