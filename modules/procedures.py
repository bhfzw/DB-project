"""
Модуль для работы с хранимыми процедурами
Распределение по студентам:
- Студент 1 (Вострухин Д.М.): GetGraduateStats, GetFacultyGraduatesStats
- Студент 2 (Яценко И.Ю.): GetSurveyResponseStats, CalculateFacultyStats
"""

PROCEDURES = {
    # Студент 1: Вострухин Д.М.
    'GetGraduateStats': {
        'sql': """
            CREATE PROCEDURE GetGraduateStats(IN graduation_year_param INT)
            BEGIN
                SELECT 
                    f.faculty_name,
                    COUNT(g.graduate_id) as graduate_count,
                    AVG(YEAR(CURDATE()) - g.graduation_year) as avg_years_since_graduation
                FROM graduates g
                JOIN faculties f ON g.faculty = f.faculty_id
                WHERE g.graduation_year = graduation_year_param
                GROUP BY f.faculty_id, f.faculty_name;
            END
        """,
        'description': 'Статистика выпускников по году выпуска',
        'student': 'Вострухин Д.М.'
    },
    
    'GetFacultyGraduatesStats': {
        'sql': """
            CREATE PROCEDURE GetFacultyGraduatesStats(IN faculty_id_param INT)
            BEGIN
                SELECT 
                    f.faculty_name,
                    COUNT(g.graduate_id) as total_graduates,
                    MIN(g.graduation_year) as earliest_graduation,
                    MAX(g.graduation_year) as latest_graduation,
                    AVG(g.graduation_year) as avg_graduation_year
                FROM graduates g
                JOIN faculties f ON g.faculty = f.faculty_id
                WHERE g.faculty = faculty_id_param
                GROUP BY f.faculty_id, f.faculty_name;
            END
        """,
        'description': 'Статистика выпускников по факультету',
        'student': 'Вострухин Д.М.'
    },
    
    # Студент 2: Яценко И.Ю.
    'GetSurveyResponseStats': {
        'sql': """
            CREATE PROCEDURE GetSurveyResponseStats(IN survey_id_param INT)
            BEGIN
                SELECT 
                    s.title as survey_title,
                    COUNT(DISTINCT a.graduate_id) as unique_respondents,
                    COUNT(a.answer_id) as total_answers,
                    (SELECT COUNT(*) FROM graduates) as total_graduates,
                    ROUND((COUNT(DISTINCT a.graduate_id) / (SELECT COUNT(*) FROM graduates)) * 100, 2) as response_rate_percent
                FROM surveys s
                LEFT JOIN answers a ON s.survey_id = a.survey_id
                WHERE s.survey_id = survey_id_param
                GROUP BY s.survey_id, s.title;
            END
        """,
        'description': 'Статистика ответов на опрос',
        'student': 'Яценко И.Ю.'
    },
    
    'CalculateFacultyStats': {
        'sql': """
            CREATE PROCEDURE CalculateFacultyStats()
            BEGIN
                SELECT 
                    f.faculty_name,
                    COUNT(g.graduate_id) as total_graduates,
                    AVG(g.graduation_year) as avg_graduation_year,
                    COUNT(DISTINCT a.graduate_id) as respondents_count
                FROM faculties f
                LEFT JOIN graduates g ON f.faculty_id = g.faculty
                LEFT JOIN answers a ON g.graduate_id = a.graduate_id
                GROUP BY f.faculty_id, f.faculty_name
                ORDER BY total_graduates DESC;
            END
        """,
        'description': 'Общая статистика по факультетам',
        'student': 'Яценко И.Ю.'
    }
}

def create_procedures():
    """Создание всех процедур в базе данных"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor(commit=True) as cursor:
            for procedure_name, procedure_data in PROCEDURES.items():
                try:
                    # Удаляем процедуру если существует
                    cursor.execute(f"DROP PROCEDURE IF EXISTS {procedure_name}")
                    # Создаем новую процедуру
                    cursor.execute(procedure_data['sql'])
                    print(f"✅ Процедура {procedure_name} создана успешно")
                except Exception as e:
                    print(f"❌ Ошибка создания процедуры {procedure_name}: {e}")
                    return False
                    
        return True
    except Exception as e:
        print(f"❌ Ошибка создания процедур: {e}")
        return False

def execute_procedure(procedure_name, params=None):
    """Выполнение хранимой процедуры"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor() as cursor:
            if params:
                cursor.callproc(procedure_name, params)
            else:
                cursor.callproc(procedure_name)
            
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            return results
    except Exception as e:
        print(f"❌ Ошибка выполнения процедуры {procedure_name}: {e}")
        return None

def get_procedures_by_student(student_name):
    """Получение процедур по имени студента"""
    student_procedures = {}
    for procedure_name, procedure_data in PROCEDURES.items():
        if procedure_data.get('student') == student_name:
            student_procedures[procedure_name] = procedure_data
    return student_procedures

def check_procedures_exist():
    """Проверка существования процедур в БД"""
    from modules.database import get_db_cursor
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT routine_name 
                FROM information_schema.routines 
                WHERE routine_schema = DATABASE() 
                AND routine_type = 'PROCEDURE'
            """)
            existing_procedures = [row['routine_name'] for row in cursor.fetchall()]
            
            result = {}
            for procedure_name in PROCEDURES.keys():
                result[procedure_name] = procedure_name in existing_procedures
                
            return result
    except Exception as e:
        print(f"❌ Ошибка проверки процедур: {e}")
        return {}
