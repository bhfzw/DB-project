#!/bin/bash
echo "Starting deployment..."

# Активируем виртуальное окружение
source venv/bin/activate

# Останавливаем предыдущие процессы
pkill -f gunicorn

# Запускаем приложение через Gunicorn
gunicorn -c gunicorn_config.py app:app --daemon

echo "Application deployed successfully!"
