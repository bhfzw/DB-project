"""
Модуль для работы с триггерами
Распределение по студентам:
- Студент 1 (Вострухин Д.М.): Триггеры 1-3
- Студент 2 (Яценко И.Ю.): Триггеры 4-6
"""

TRIGGERS = {
    # Студент 1: Вострухин Д.М.
    'audit_graduate_changes': {
        'sql': """
            CREATE TRIGGER audit_graduate_changes 
            AFTER UPDATE ON graduates
            FOR EACH ROW
            BEGIN
                IF OLD.first_name != NEW.first_name OR OLD.last_name != NEW.last_name OR OLD.email != NEW.email THEN
                    INSERT INTO audit_log (user_id, event_type, timestamp, details)
                    VALUES (
                        COALESCE(@current_user_id, 1), 
                        'GRADUATE_UPDATED',
                        NOW(),
                        CONCAT('Изменен выпускник: ', OLD.first_name, ' ', OLD.last_name, 
                               ' (ID: ', OLD.graduate_id, ')')
                    );
                END IF;
            END
        """,
        'description': 'Аудит изменений данных выпускников',
        'student': 'Вострухин Д.М.'
    },
    
    'prevent_duplicate_emails': {
        'sql': """
            CREATE TRIGGER prevent_duplicate_emails
            BEFORE INSERT ON graduates
            FOR EACH ROW
            BEGIN
                DECLARE email_count INT;
                SELECT COUNT(*) INTO email_count FROM graduates WHERE email = NEW.email;
                IF email_count > 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Email уже существует в системе';
                END IF;
            END
        """,
        'description': 'Запрет дублирования email выпускников',
        'student': 'Вострухин Д.М.'
    },
    
    'log_survey_creation': {
        'sql': """
            CREATE TRIGGER log_survey_creation
            AFTER INSERT ON surveys
            FOR EACH ROW
            BEGIN
                INSERT INTO audit_log (user_id, event_type, timestamp, details)
                VALUES (
                    NEW.created_by,
                    'SURVEY_CREATED',
                    NOW(),
                    CONCAT('Создан опрос: ', NEW.title, ' (ID: ', NEW.survey_id, ')')
                );
            END
        """,
        'description': 'Логирование создания новых опросов',
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'validate_graduation_year': {
        'sql': """
            CREATE TRIGGER validate_graduation_year
            BEFORE INSERT ON graduates
            FOR EACH ROW
            BEGIN
                IF NEW.graduation_year < 1950 OR NEW.graduation_year > YEAR(CURDATE()) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Недопустимый год выпуска. Допустимый диапазон: 1950-текущий год';
                END IF;
            END
        """,
        'description': 'Валидация года выпуска',
        'student': 'Яценко И.Ю.'
    },
    
    'prevent_future_graduation': {
        'sql': """
            CREATE TRIGGER prevent_future_graduation
            BEFORE INSERT ON graduates
            FOR EACH ROW
            BEGIN
                IF NEW.graduation_year > YEAR(CURDATE()) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Год выпуска не может быть в будущем';
                END IF;
            END
        """,
        'description': 'Запрет указания будущего года выпуска',
        'student': 'Яценко И.Ю.'
    },
    
    'log_answer_submission': {
        'sql': """
            CREATE TRIGGER log_answer_submission
            AFTER INSERT ON answers
            FOR EACH ROW
            BEGIN
                INSERT INTO audit_log (user_id, event_type, timestamp, details)
                VALUES (
                    COALESCE(@current_user_id, 1),
                    'ANSWER_SUBMITTED',
                    NOW(),
                    CONCAT('Добавлен ответ: опрос ', NEW.survey_id, ', выпускник ', NEW.graduate_id)
                );
            END
        """,
        'description': 'Логирование отправки ответов на опросы',
        'student': 'Яценко И.Ю.'
    }
}

def create_triggers():
    """Создание всех триггеров в базе данных"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor(commit=True) as cursor:
            for trigger_name, trigger_data in TRIGGERS.items():
                try:
                    # Удаляем триггер если существует
                    cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
                    # Создаем новый триггер
                    cursor.execute(trigger_data['sql'])
                    print(f"✅ Триггер {trigger_name} создан успешно")
                except Exception as e:
                    print(f"❌ Ошибка создания триггера {trigger_name}: {e}")
                    return False
                    
        return True
    except Exception as e:
        print(f"❌ Ошибка создания триггеров: {e}")
        return False

def drop_triggers():
    """Удаление всех триггеров"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor(commit=True) as cursor:
            for trigger_name in TRIGGERS.keys():
                try:
                    cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
                    print(f"✅ Триггер {trigger_name} удален")
                except Exception as e:
                    print(f"❌ Ошибка удаления триггера {trigger_name}: {e}")
        return True
    except Exception as e:
        print(f"❌ Ошибка удаления триггеров: {e}")
        return False

def check_triggers_exist():
    """Проверка существования триггеров в БД"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT trigger_name 
                FROM information_schema.triggers 
                WHERE trigger_schema = DATABASE()
            """)
            existing_triggers = [row['trigger_name'] for row in cursor.fetchall()]
            
            result = {}
            for trigger_name in TRIGGERS.keys():
                result[trigger_name] = trigger_name in existing_triggers
                
            return result
    except Exception as e:
        print(f"❌ Ошибка проверки триггеров: {e}")
        return {}

def demonstrate_triggers():
    """Демонстрация работы триггеров"""
    from modules.database import execute_query
    
    demonstrations = [
        {
            'name': 'Проверка уникальности email (триггер prevent_duplicate_emails)',
            'query': "INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES ('Test', 'User', 'ivan.petrov@email.com', 2023, 1)",
            'expected_error': True,
            'student': 'Вострухин Д.М.'
        },
        {
            'name': 'Проверка валидации года выпуска (триггер validate_graduation_year)',
            'query': "INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES ('Test', 'User', 'test123@email.com', 1800, 1)",
            'expected_error': True,
            'student': 'Яценко И.Ю.'
        },
        {
            'name': 'Проверка будущего года выпуска (триггер prevent_future_graduation)',
            'query': "INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES ('Test', 'User', 'future@email.com', 2030, 1)",
            'expected_error': True,
            'student': 'Яценко И.Ю.'
        },
        {
            'name': 'Успешное добавление выпускника',
            'query': "INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES ('Test', 'User', 'unique.email@test.com', 2023, 1)",
            'expected_error': False,
            'student': 'Оба студента'
        }
    ]
    
    results = []
    for demo in demonstrations:
        try:
            execute_query(demo['query'], fetch=False)
            results.append({
                'name': demo['name'],
                'student': demo['student'],
                'status': 'SUCCESS' if not demo['expected_error'] else 'FAILED',
                'message': '✅ Запрос выполнен успешно' if not demo['expected_error'] else '❌ Ожидалась ошибка, но запрос прошел'
            })
        except Exception as e:
            results.append({
                'name': demo['name'],
                'student': demo['student'],
                'status': 'EXPECTED_ERROR' if demo['expected_error'] else 'UNEXPECTED_ERROR',
                'message': f"✅ Триггер сработал: {str(e)}" if demo['expected_error'] else f"❌ Неожиданная ошибка: {str(e)}"
            })
    
    return results

def get_triggers_by_student(student_name):
    """Получение триггеров по имени студента"""
    student_triggers = {}
    for trigger_name, trigger_data in TRIGGERS.items():
        if trigger_data.get('student') == student_name:
            student_triggers[trigger_name] = trigger_data
    return student_triggers
