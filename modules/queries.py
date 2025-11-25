"""
Модуль с предопределенными запросами для системы опросов выпускников
Распределение по студентам:
- Студент 1 (Вострухин Д.М.): Простые 1-3, JOIN 1, Подзапрос 1, Представление 1
- Студент 2 (Яценко И.Ю.): Простые 4-6, JOIN 2, Подзапрос 2, Представление 2
"""

# Простые запросы (по 3 на студента)
SIMPLE_QUERIES = {
    # Студент 1: Вострухин Д.М.
    'count_graduates': {
        'query': "SELECT COUNT(*) as total_graduates FROM graduates",
        'description': "Общее количество выпускников в системе",
        'student': 'Вострухин Д.М.'
    },
    'active_surveys_count': {
        'query': "SELECT COUNT(*) as active_surveys FROM surveys WHERE created_by IS NOT NULL",
        'description': "Количество активных опросов",
        'student': 'Вострухин Д.М.'
    },
    'recent_graduates': {
        'query': "SELECT first_name, last_name, graduation_year FROM graduates ORDER BY graduation_year DESC LIMIT 10",
        'description': "10 последних выпускников",
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'survey_titles': {
        'query': "SELECT title, description FROM surveys LIMIT 5",
        'description': "Список названий опросов",
        'student': 'Яценко И.Ю.'
    },
    'faculty_count': {
        'query': "SELECT COUNT(*) as faculty_count FROM faculties",
        'description': "Количество факультетов",
        'student': 'Яценко И.Ю.'
    },
    'user_roles': {
        'query': "SELECT DISTINCT role, COUNT(*) as count FROM users GROUP BY role",
        'description': "Распределение пользователей по ролям",
        'student': 'Яценко И.Ю.'
    }
}

# Запросы с JOIN (по 1 на студента)
JOIN_QUERIES = {
    # Студент 1: Вострухин Д.М.
    'graduates_with_faculty': {
        'query': """
            SELECT g.graduate_id, g.first_name, g.last_name, f.faculty_name, g.graduation_year 
            FROM graduates g 
            JOIN faculties f ON g.faculty = f.faculty_id 
            ORDER BY g.graduation_year DESC
            LIMIT 15
        """,
        'description': "Выпускники с информацией о факультетах",
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'survey_responses_count': {
        'query': """
            SELECT s.survey_id, s.title, COUNT(a.answer_id) as response_count 
            FROM surveys s 
            LEFT JOIN answers a ON s.survey_id = a.survey_id 
            GROUP BY s.survey_id, s.title
            ORDER BY response_count DESC
        """,
        'description': "Количество ответов по каждому опросу",
        'student': 'Яценко И.Ю.'
    }
}

# Запросы с подзапросами (по 1 на студента)
SUBQUERY_QUERIES = {
    # Студент 1: Вострухин Д.М.
    'graduates_above_average_year': {
        'query': """
            SELECT first_name, last_name, graduation_year 
            FROM graduates 
            WHERE graduation_year > (
                SELECT AVG(graduation_year) FROM graduates
            )
            ORDER BY graduation_year DESC
        """,
        'description': "Выпускники с годом выпуска выше среднего",
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'popular_surveys': {
        'query': """
            SELECT title, description 
            FROM surveys 
            WHERE survey_id IN (
                SELECT survey_id FROM answers 
                GROUP BY survey_id 
                HAVING COUNT(*) > 0
            )
        """,
        'description': "Опросы, на которые есть ответы",
        'student': 'Яценко И.Ю.'
    }
}

# Представления (по 1 на студента)
VIEW_QUERIES = {
    # Студент 1: Вострухин Д.М.
    'graduate_details': {
        'query': """
            CREATE OR REPLACE VIEW graduate_details AS
            SELECT 
                g.graduate_id,
                CONCAT(g.first_name, ' ', g.last_name) as full_name,
                g.email,
                g.graduation_year,
                f.faculty_name,
                COUNT(a.answer_id) as answers_count
            FROM graduates g
            LEFT JOIN faculties f ON g.faculty = f.faculty_id
            LEFT JOIN answers a ON g.graduate_id = a.graduate_id
            GROUP BY g.graduate_id, g.first_name, g.last_name, g.email, g.graduation_year, f.faculty_name
        """,
        'description': "Детальная информация о выпускниках с количеством ответов",
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'survey_statistics': {
        'query': """
            CREATE OR REPLACE VIEW survey_statistics AS
            SELECT 
                s.survey_id,
                s.title,
                s.description,
                u.user_name as created_by,
                COUNT(DISTINCT a.graduate_id) as unique_respondents,
                COUNT(a.answer_id) as total_answers
            FROM surveys s
            LEFT JOIN users u ON s.created_by = u.user_id
            LEFT JOIN answers a ON s.survey_id = a.survey_id
            GROUP BY s.survey_id, s.title, s.description, u.user_name
        """,
        'description': "Статистика по опросам",
        'student': 'Яценко И.Ю.'
    }
}

# Запросы к представлениям
VIEW_SELECT_QUERIES = {
    # Студент 1: Вострухин Д.М.
    'view_graduate_details': {
        'query': "SELECT * FROM graduate_details LIMIT 10",
        'description': "Данные из представления graduate_details",
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'view_survey_statistics': {
        'query': "SELECT * FROM survey_statistics",
        'description': "Данные из представления survey_statistics",
        'student': 'Яценко И.Ю.'
    }
}

def create_views():
    """Создание представлений в базе данных"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor(commit=True) as cursor:
            for view_name, view_data in VIEW_QUERIES.items():
                try:
                    cursor.execute(view_data['query'])
                    print(f"View {view_name} created successfully")
                except Exception as e:
                    print(f"Error creating view {view_name}: {e}")
        return True
    except Exception as e:
        print(f"Error creating views: {e}")
        return False

def get_queries_by_student(student_name):
    """Получение запросов по имени студента"""
    student_queries = {}
    
    for query_dict in [SIMPLE_QUERIES, JOIN_QUERIES, SUBQUERY_QUERIES, VIEW_SELECT_QUERIES]:
        for name, data in query_dict.items():
            if data.get('student') == student_name:
                student_queries[name] = data
    
    return student_queries
