-- sql/init/database_setup.sql
-- Основной скрипт инициализации базы данных

-- Создание базы данных
CREATE DATABASE IF NOT EXISTS graduate_surveys 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE graduate_surveys;

-- Запуск скриптов создания структуры
SOURCE sql/init/create_complete_structure.sql;

-- Добавление базовых данных
SOURCE sql/data/fill_complete_data.sql;

-- Создание функций
SOURCE sql/functions/create_simple_functions.sql;

-- Создание процедур (будет добавлено позже)
-- SOURCE sql/functions/create_procedures.sql;

-- Создание триггеров (будет добавлено позже)  
-- SOURCE sql/triggers/create_triggers.sql;
