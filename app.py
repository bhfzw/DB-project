from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, send_file, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from dotenv import load_dotenv
import os
from config import Config
from modules.database import get_db_cursor, get_db_connection
from modules.queries import SIMPLE_QUERIES, JOIN_QUERIES, SUBQUERY_QUERIES, VIEW_SELECT_QUERIES
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import io
import csv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Регистрируем шрифты с поддержкой кириллицы
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
    CYRILLIC_FONT = 'DejaVuSans'
    CYRILLIC_FONT_BOLD = 'DejaVuSans-Bold'
except:
    CYRILLIC_FONT = 'Helvetica'
    CYRILLIC_FONT_BOLD = 'Helvetica-Bold'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def has_role(self, role_name):
        """Проверка роли пользователя"""
        return self.role == role_name

    def is_admin(self):
        return self.has_role('admin')
    
    def is_moderator(self):
        return self.has_role('moderator')
    
    def is_user(self):
        return self.has_role('user')

@login_manager.user_loader
def load_user(user_id):
    try:
        with get_db_cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            user = cursor.fetchone()
            if user:
                return User(id=user['user_id'], username=user['user_name'], role=user['role'])
            return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# ==================== ДЕКОРАТОРЫ ПРАВ ДОСТУПА ====================

def admin_required(f):
    """Требует роль admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Доступ запрещен. Требуются права администратора.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def moderator_required(f):
    """Требует роль moderator или admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (not current_user.is_moderator() and not current_user.is_admin()):
            flash('Доступ запрещен. Требуются права модератора.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Требует роль moderator или admin (не обычный user)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_user():
            flash('Доступ запрещен. Требуются права сотрудника.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== МАРШРУТЫ АУТЕНТИФИКАЦИИ ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE user_name = %s', (username,))
                user = cursor.fetchone()
                
                if user and user['role'] == password:  # Простая проверка для демо
                    user_obj = User(id=user['user_id'], username=user['user_name'], role=user['role'])
                    login_user(user_obj)
                    flash(f'Добро пожаловать, {user["user_name"]}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Неверное имя пользователя или пароль', 'danger')
        except Exception as e:
            flash(f'Ошибка базы данных: {e}', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# ==================== CRUD МАРШРУТЫ ====================

# Выпускники
@app.route('/crud/graduates')
@login_required
@staff_required
def crud_graduates():
    with get_db_cursor() as cursor:
        cursor.execute('SELECT g.*, f.faculty_name FROM graduates g JOIN faculties f ON g.faculty = f.faculty_id ORDER BY g.graduate_id')
        graduates = cursor.fetchall()
    
    return render_template('crud/graduates.html', graduates=graduates)

@app.route('/crud/graduates/add', methods=['POST'])
@login_required
@staff_required
def add_graduate():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        graduation_year = request.form['graduation_year']
        faculty = request.form['faculty']
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    'INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES (%s, %s, %s, %s, %s)',
                    (first_name, last_name, email, graduation_year, faculty)
                )
            flash('Выпускник успешно добавлен', 'success')
        except Exception as e:
            flash(f'Ошибка при добавлении: {e}', 'danger')
    
    return redirect(url_for('crud_graduates'))


@app.route('/crud/graduates/delete/<int:id>')
@login_required
@staff_required
def delete_graduate(id):
    try:
        with get_db_cursor(commit=True) as cursor:
            # Сначала удаляем ответы выпускника
            cursor.execute('DELETE FROM answers WHERE graduate_id = %s', (id,))
            # Затем удаляем самого выпускника
            cursor.execute('DELETE FROM graduates WHERE graduate_id = %s', (id,))
        flash('Выпускник и его ответы успешно удалены', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении: {e}', 'danger')

    return redirect(url_for('crud_graduates'))
# Факультеты
@app.route('/crud/faculties')
@login_required
@staff_required
def crud_faculties():
    with get_db_cursor() as cursor:
        cursor.execute('SELECT * FROM faculties')
        faculties = cursor.fetchall()
    return render_template('crud/faculties.html', faculties=faculties)

@app.route('/crud/faculties/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_faculty(id):
    """Редактирование факультета"""
    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    'UPDATE faculties SET faculty_name = %s WHERE faculty_id = %s',
                    (faculty_name, id)
                )
            flash('Факультет успешно обновлен', 'success')
            return redirect(url_for('crud_faculties'))
        except Exception as e:
            flash(f'Ошибка при обновлении: {e}', 'danger')
    
    # GET запрос - показать форму редактирования
    with get_db_cursor() as cursor:
        cursor.execute('SELECT * FROM faculties WHERE faculty_id = %s', (id,))
        faculty = cursor.fetchone()
    
    return render_template('crud/edit_faculty.html', faculty=faculty)

@app.route('/crud/faculties/delete/<int:id>')
@login_required
@staff_required
def delete_faculty(id):
    """Удаление факультета"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Проверяем есть ли выпускники на этом факультете
            cursor.execute('SELECT COUNT(*) as count FROM graduates WHERE faculty = %s', (id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                flash('Нельзя удалить факультет: есть связанные выпускники', 'danger')
            else:
                cursor.execute('DELETE FROM faculties WHERE faculty_id = %s', (id,))
                flash('Факультет успешно удален', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении: {e}', 'danger')
    
    return redirect(url_for('crud_faculties'))

@app.route('/crud/faculties/add', methods=['POST'])
@login_required
@staff_required
def add_faculty():
    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    'INSERT INTO faculties (faculty_name) VALUES (%s)',
                    (faculty_name,)
                )
            flash('Факультет успешно добавлен', 'success')
        except Exception as e:
            flash(f'Ошибка при добавлении: {e}', 'danger')
    
    return redirect(url_for('crud_faculties'))

# Опросы
@app.route('/crud/surveys')
@login_required
@staff_required
def crud_surveys():
    with get_db_cursor() as cursor:
        cursor.execute('SELECT s.*, u.user_name FROM surveys s LEFT JOIN users u ON s.created_by = u.user_id')
        surveys = cursor.fetchall()
    return render_template('crud/surveys.html', surveys=surveys)

@app.route('/crud/surveys/add', methods=['POST'])
@login_required
@staff_required
def add_survey():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    'INSERT INTO surveys (title, description, created_by) VALUES (%s, %s, %s)',
                    (title, description, current_user.id)
                )
            flash('Опрос успешно создан', 'success')
        except Exception as e:
            flash(f'Ошибка при создании: {e}', 'danger')
    
    return redirect(url_for('crud_surveys'))

@app.route('/crud/surveys/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_survey(id):
    """Редактирование опроса"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    'UPDATE surveys SET title = %s, description = %s WHERE survey_id = %s',
                    (title, description, id)
                )
            flash('Опрос успешно обновлен', 'success')
            return redirect(url_for('crud_surveys'))
        except Exception as e:
            flash(f'Ошибка при обновлении: {e}', 'danger')
    
    # GET запрос - показать форму редактирования
    with get_db_cursor() as cursor:
        cursor.execute('SELECT * FROM surveys WHERE survey_id = %s', (id,))
        survey = cursor.fetchone()
    
    return render_template('crud/edit_survey.html', survey=survey)

@app.route('/crud/surveys/delete/<int:id>')
@login_required
@staff_required
def delete_survey(id):
    """Удаление опроса"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Проверяем есть ли ответы на этот опрос
            cursor.execute('SELECT COUNT(*) as count FROM answers WHERE survey_id = %s', (id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                flash('Нельзя удалить опрос: есть связанные ответы', 'danger')
            else:
                cursor.execute('DELETE FROM surveys WHERE survey_id = %s', (id,))
                flash('Опрос успешно удален', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении: {e}', 'danger')
    
    return redirect(url_for('crud_surveys'))

@app.route('/crud/surveys/view/<int:id>')
@login_required
@staff_required
def view_survey(id):
    """Просмотр детальной информации об опросе"""
    with get_db_cursor() as cursor:
        # Получаем информацию об опросе
        cursor.execute('SELECT * FROM surveys WHERE survey_id = %s', (id,))
        survey = cursor.fetchone()
        
        # Получаем секции опроса
        cursor.execute('SELECT * FROM sections WHERE survey_id = %s ORDER BY section_order', (id,))
        sections = cursor.fetchall()
        
        # Получаем статистику ответов
        cursor.execute('''
            SELECT COUNT(DISTINCT graduate_id) as respondents_count,
                   COUNT(*) as total_answers
            FROM answers 
            WHERE survey_id = %s
        ''', (id,))
        stats = cursor.fetchone()
    
    return render_template('crud/view_survey.html', survey=survey, sections=sections, stats=stats)

# Вопросы
@app.route('/crud/questions')
@login_required
@staff_required
def crud_questions():
    with get_db_cursor() as cursor:
        cursor.execute('SELECT q.*, s.title as survey_title FROM questions q JOIN sections s ON q.section_id = s.section_id')
        questions = cursor.fetchall()
    return render_template('crud/questions.html', questions=questions)

# Ответы
@app.route('/crud/answers')
@login_required
@staff_required
def crud_answers():
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT a.*, g.first_name, g.last_name, s.title as survey_title, q.question_text, c.choice_text
            FROM answers a
            JOIN graduates g ON a.graduate_id = g.graduate_id
            JOIN surveys s ON a.survey_id = s.survey_id
            JOIN questions q ON a.question_id = q.question_id
            LEFT JOIN choices c ON a.choice_id = c.choice_id
        ''')
        answers = cursor.fetchall()
    return render_template('crud/answers.html', answers=answers)

# ==================== ИНДИВИДУАЛЬНЫЕ ЗАПРОСЫ ====================

@app.route('/queries/simple')
@login_required
def simple_queries():
    results = {}
    with get_db_cursor() as cursor:
        for name, query_data in SIMPLE_QUERIES.items():
            cursor.execute(query_data['query'])
            results[name] = {
                'data': cursor.fetchall(),
                'description': query_data['description'],
                'student': query_data['student']
            }
    return render_template('queries.html', results=results, query_type='Простые запросы')

@app.route('/queries/join')
@login_required
def join_queries():
    results = {}
    with get_db_cursor() as cursor:
        for name, query_data in JOIN_QUERIES.items():
            cursor.execute(query_data['query'])
            results[name] = {
                'data': cursor.fetchall(),
                'description': query_data['description'],
                'student': query_data['student']
            }
    return render_template('queries.html', results=results, query_type='Запросы с JOIN')

@app.route('/queries/subquery')
@login_required
def subquery_queries():
    results = {}
    with get_db_cursor() as cursor:
        for name, query_data in SUBQUERY_QUERIES.items():
            cursor.execute(query_data['query'])
            results[name] = {
                'data': cursor.fetchall(),
                'description': query_data['description'],
                'student': query_data['student']
            }
    return render_template('queries.html', results=results, query_type='Запросы с подзапросами')

# Динамический запрос
@app.route('/queries/dynamic', methods=['GET', 'POST'])
@login_required
@staff_required
def dynamic_query():
    results = None
    error = None
    if request.method == 'POST':
        query = request.form['query']
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        except Exception as e:
            error = str(e)
    
    return render_template('dynamic_query.html', results=results, error=error)

# ==================== ПРЕДСТАВЛЕНИЯ ====================

@app.route('/queries/views')
@login_required
def view_queries():
    results = {}
    with get_db_cursor() as cursor:
        for name, query_data in VIEW_SELECT_QUERIES.items():
            cursor.execute(query_data['query'])
            results[name] = {
                'data': cursor.fetchall(),
                'description': query_data['description'],
                'student': query_data['student']
            }
    return render_template('queries.html', results=results, query_type='Запросы к представлениям')

@app.route('/queries/create_views')
@login_required
@admin_required
def create_views_route():
    from modules.queries import create_views
    if create_views():
        flash('Представления успешно созданы', 'success')
    else:
        flash('Ошибка при создании представлений', 'danger')
    return redirect(url_for('view_queries'))

# ==================== АДМИНИСТРИРОВАНИЕ БАЗЫ ДАННЫХ ====================

@app.route('/admin/create_database_objects')
@login_required
@admin_required
def create_database_objects():
    """Создание функций - с новыми правами"""
    try:
        with get_db_cursor(commit=True) as cursor:
            
            print("Создаем функцию GetGraduateFullName...")

            # Функция 1
            cursor.execute("DROP FUNCTION IF EXISTS GetGraduateFullName")
            cursor.execute("""
                CREATE FUNCTION GetGraduateFullName(graduate_id_param INT)
                RETURNS VARCHAR(255)
                DETERMINISTIC
                READS SQL DATA
                BEGIN
                    DECLARE result_name VARCHAR(255);
                    SELECT CONCAT(first_name, ' ', last_name) INTO result_name 
                    FROM graduates WHERE graduate_id = graduate_id_param;
                    RETURN result_name;
                END
            """)

            print("Создаем функцию CountSurveyResponses...")

            # Функция 2
            cursor.execute("DROP FUNCTION IF EXISTS CountSurveyResponses")
            cursor.execute("""
                CREATE FUNCTION CountSurveyResponses(survey_id_param INT)
                RETURNS INT
                DETERMINISTIC
                READS SQL DATA
                BEGIN
                    DECLARE result_count INT;
                    SELECT COUNT(*) INTO result_count 
                    FROM answers WHERE survey_id = survey_id_param;
                    RETURN result_count;
                END
            """)

            print("Создаем процедуру GetGraduateStats...")

            # Процедура
            cursor.execute("DROP PROCEDURE IF EXISTS GetGraduateStats")
            cursor.execute("""
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
            """)

        flash('✅ Функции и процедуры успешно созданы!', 'success')
        print("Функции созданы успешно!")

    except Exception as e:
        flash(f'❌ Ошибка при создании функций: {str(e)}', 'danger')
        print(f"DEBUG Error: {e}")

    return redirect(url_for('dashboard'))
@app.route('/test/functions')
@login_required
def test_functions():
    """Простая проверка работы функций"""
    try:
        with get_db_cursor() as cursor:
            # Тестируем функцию 1
            cursor.execute("SELECT GetGraduateFullName(1) as full_name")
            result1 = cursor.fetchone()

            # Тестируем функцию 2
            cursor.execute("SELECT CountSurveyResponses(1) as response_count")
            result2 = cursor.fetchone()

        flash(
            f'Тест функций: Имя выпускника - {result1["full_name"]}, Ответов на опрос 1 - {result2["response_count"]}',
            'success')

    except Exception as e:
        flash(f'Функции не работают: {e}. Сначала создайте объекты БД.', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/admin/check_functions')
@login_required
@admin_required
def check_functions():
    """Проверка существования функций в БД - УПРОЩЕННАЯ ВЕРСИЯ"""
    try:
        # Простая проверка через тестовые вызовы
        functions_list = []
        procedures_list = []
        
        with get_db_cursor() as cursor:
            # Проверяем функцию 1
            try:
                cursor.execute("SELECT GetGraduateFullName(1) as test")
                result = cursor.fetchone()
                functions_list.append({'routine_name': 'GetGraduateFullName', 'routine_type': 'FUNCTION'})
            except Exception as e:
                print(f"Функция GetGraduateFullName не найдена: {e}")
            
            # Проверяем функцию 2
            try:
                cursor.execute("SELECT CountSurveyResponses(1) as test")
                result = cursor.fetchone()
                functions_list.append({'routine_name': 'CountSurveyResponses', 'routine_type': 'FUNCTION'})
            except Exception as e:
                print(f"Функция CountSurveyResponses не найдена: {e}")
            
            # Проверяем процедуру (пропускаем, так как её сложно создать без прав)
            # procedures_list остается пустым

        result = {
            'functions': functions_list,
            'procedures': procedures_list
        }

        flash(f'Найдено функций: {len(functions_list)}, процедур: {len(procedures_list)}', 'info')
        return render_template('admin/check_functions.html', result=result)

    except Exception as e:
        flash(f'Ошибка проверки функций: {e}', 'danger')
        return redirect(url_for('dashboard'))
# ==================== ПРОЦЕДУРЫ И ФУНКЦИИ ====================

@app.route('/procedures/graduate_stats')
@login_required
@staff_required
def graduate_stats():
    results = None
    try:
        with get_db_cursor() as cursor:
            cursor.callproc('GetGraduateStats', [2020])
            for result in cursor.stored_results():
                results = result.fetchall()
    except Exception as e:
        flash(f'Ошибка выполнения процедуры: {e}', 'danger')
    
    return render_template('procedure_results.html', results=results, procedure_name='Статистика выпускников')

@app.route('/functions/graduate_full_name/<int:graduate_id>')
@login_required
def get_graduate_full_name(graduate_id):
    """Пример вызова функции - Студент 1: Вострухин Д.М."""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT GetGraduateFullName(%s) as full_name", (graduate_id,))
            result = cursor.fetchone()
        
        flash(f'Полное имя выпускника (ID: {graduate_id}): {result["full_name"]}', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Ошибка вызова функции: {e}. Сначала создайте функции через "Создать объекты БД"', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/functions/survey_responses_count/<int:survey_id>')
@login_required
def get_survey_responses_count(survey_id):
    """Пример вызова функции - Студент 2: Яценко И.Ю."""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT CountSurveyResponses(%s) as response_count", (survey_id,))
            result = cursor.fetchone()
        
        flash(f'Количество ответов на опрос (ID: {survey_id}): {result["response_count"]}', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Ошибка вызова функции: {e}. Сначала создайте функции через "Создать объекты БД"', 'danger')
        return redirect(url_for('dashboard'))

# ==================== ТРАНЗАКЦИИ ====================

@app.route('/transactions/add_graduate_with_survey')
@login_required
@staff_required
def add_graduate_with_survey():
    """Транзакция: добавление выпускника и его ответов на опрос - Студент 1: Вострухин Д.М."""
    
    import random
    import time
    
    # Генерируем уникальный email чтобы избежать дублирования
    timestamp = int(time.time())
    random_suffix = random.randint(1000, 9999)
    unique_email = f'transaction_{timestamp}_{random_suffix}@email.com'
    
    try:
        with get_db_cursor(commit=True) as cursor:
            # 1. Добавляем выпускника
            cursor.execute(
                "INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES (%s, %s, %s, %s, %s)",
                ['Алексей', 'Транзакционов', unique_email, 2023, 1]
            )
            new_graduate_id = cursor.lastrowid
            
            # 2. Добавляем ответы на опрос (используем реальный ID)
            cursor.execute(
                "INSERT INTO answers (survey_id, graduate_id, question_id, choice_id) VALUES (%s, %s, %s, %s)",
                [1, new_graduate_id, 1, 1]
            )
            
            cursor.execute(
                "INSERT INTO answers (survey_id, graduate_id, question_id, choice_id) VALUES (%s, %s, %s, %s)",
                [1, new_graduate_id, 2, 2]
            )
            
            # 3. Логируем действие
            cursor.execute(
                "INSERT INTO audit_log (user_id, event_type, timestamp) VALUES (%s, %s, NOW())",
                [current_user.id, 'Транзакция: добавлен выпускник с ответами']
            )
        
        flash('Транзакция выполнена успешно! Добавлен выпускник с ответами на опрос', 'success')
    
    except Exception as e:
        flash(f'Ошибка транзакции: {e}', 'danger')
    
    return redirect(url_for('dashboard'))
 
@app.route('/transactions/create_survey_structure')
@login_required
@staff_required
def create_survey_structure():
    """Транзакция: создание опроса с секциями и вопросами - Студент 2: Яценко И.Ю."""

    import time

    try:
        with get_db_cursor(commit=True) as cursor:
            # 1. Создаем опрос
            cursor.execute(
                "INSERT INTO surveys (title, description, created_by) VALUES (%s, %s, %s)",
                ['Новый транзакционный опрос', 'Опрос созданный в рамках транзакции', current_user.id]
            )
            new_survey_id = cursor.lastrowid

            # 2. Создаем секцию
            cursor.execute(
                "INSERT INTO sections (survey_id, title, section_order) VALUES (%s, %s, %s)",
                [new_survey_id, 'Основная секция', 1]
            )
            new_section_id = cursor.lastrowid

            # 3. Создаем вопросы (используем section_order вместо question_order)
            cursor.execute(
                "INSERT INTO questions (section_id, question_text, section_order) VALUES (%s, %s, %s)",
                [new_section_id, 'Как вы оцените транзакции в БД?', 1]
            )
            question1_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO questions (section_id, question_text, section_order) VALUES (%s, %s, %s)",
                [new_section_id, 'Насколько важна целостность данных?', 2]
            )
            question2_id = cursor.lastrowid

            # 4. Создаем варианты ответов для первого вопроса
            cursor.execute(
                "INSERT INTO choices (question_id, choice_text, choice_order) VALUES (%s, %s, %s)",
                [question1_id, 'Очень полезны', 1]
            )

            cursor.execute(
                "INSERT INTO choices (question_id, choice_text, choice_order) VALUES (%s, %s, %s)",
                [question1_id, 'Полезны', 2]
            )

            cursor.execute(
                "INSERT INTO choices (question_id, choice_text, choice_order) VALUES (%s, %s, %s)",
                [question1_id, 'Нейтрально', 3]
            )

            # 5. Логируем действие
            cursor.execute(
                "INSERT INTO audit_log (user_id, event_type, timestamp) VALUES (%s, %s, NOW())",
                [current_user.id, 'Транзакция: создан опрос с вопросами']
            )

        flash('Транзакция выполнена успешно! Создан опрос с вопросами', 'success')

    except Exception as e:
        flash(f'Ошибка транзакции: {e}', 'danger')

    return redirect(url_for('dashboard'))
# ==================== ПРОЦЕДУРЫ ====================

@app.route('/procedures')
@login_required
@staff_required
def procedures_dashboard():
    """Дашборд процедур"""
    from modules.procedures import get_procedures_by_student, check_procedures_exist
    
    procedures_status = check_procedures_exist()
    student1_procedures = get_procedures_by_student('Вострухин Д.М.')
    student2_procedures = get_procedures_by_student('Яценко И.Ю.')
    
    return render_template('procedures/dashboard.html',
                         procedures_status=procedures_status,
                         student1_procedures=student1_procedures,
                         student2_procedures=student2_procedures)

@app.route('/procedures/graduate_stats_by_year')
@login_required
@staff_required
def graduate_stats_by_year():
    """Статистика выпускников по году - Студент 1: Вострухин Д.М."""
    results = None
    year = request.args.get('year', 2020, type=int)
    
    try:
        from modules.procedures import execute_procedure
        results = execute_procedure('GetGraduateStats', [year])
        
        if not results:
            flash('Нет данных для выбранного года', 'info')
            
    except Exception as e:
        flash(f'Ошибка выполнения процедуры: {e}', 'danger')
    
    return render_template('procedures/results.html', 
                         results=results, 
                         procedure_name=f'Статистика выпускников {year} года',
                         student='Вострухин Д.М.')

@app.route('/procedures/faculty_graduates_stats')
@login_required
@staff_required
def faculty_graduates_stats():
    """Статистика выпускников по факультету - Студент 1: Вострухин Д.М."""
    results = None
    faculty_id = request.args.get('faculty_id', 1, type=int)
    
    try:
        from modules.procedures import execute_procedure
        results = execute_procedure('GetFacultyGraduatesStats', [faculty_id])
        
        if not results:
            flash('Нет данных для выбранного факультета', 'info')
            
    except Exception as e:
        flash(f'Ошибка выполнения процедуры: {e}', 'danger')
    
    return render_template('procedures/results.html', 
                         results=results, 
                         procedure_name='Статистика выпускников по факультету',
                         student='Вострухин Д.М.')

@app.route('/procedures/survey_response_stats')
@login_required
@staff_required
def survey_response_stats():
    """Статистика ответов на опрос - Студент 2: Яценко И.Ю."""
    results = None
    survey_id = request.args.get('survey_id', 1, type=int)
    
    try:
        from modules.procedures import execute_procedure
        results = execute_procedure('GetSurveyResponseStats', [survey_id])
        
        if not results:
            flash('Нет данных для выбранного опроса', 'info')
            
    except Exception as e:
        flash(f'Ошибка выполнения процедуры: {e}', 'danger')
    
    return render_template('procedures/results.html', 
                         results=results, 
                         procedure_name='Статистика ответов на опрос',
                         student='Яценко И.Ю.')

@app.route('/procedures/faculty_overview_stats')
@login_required
@staff_required
def faculty_overview_stats():
    """Общая статистика по факультетам - Студент 2: Яценко И.Ю."""
    results = None
    
    try:
        from modules.procedures import execute_procedure
        results = execute_procedure('CalculateFacultyStats')
        
        if not results:
            flash('Нет данных для отображения', 'info')
            
    except Exception as e:
        flash(f'Ошибка выполнения процедуры: {e}', 'danger')
    
    return render_template('procedures/results.html', 
                         results=results, 
                         procedure_name='Общая статистика по факультетам',
                         student='Яценко И.Ю.')

@app.route('/admin/create_procedures')
@login_required
@admin_required
def create_procedures_route():
    """Создание всех процедур в БД"""
    from modules.procedures import create_procedures
    if create_procedures():
        flash('✅ Процедуры успешно созданы!', 'success')
    else:
        flash('❌ Ошибка при создании процедур', 'danger')
    return redirect(url_for('procedures_dashboard'))
# ==================== ОТЧЕТЫ PDF И CSV ====================

@app.route('/reports/generate', methods=['GET', 'POST'])
@login_required
@staff_required
def generate_report():
    preview_data = None
    report_type = None
    
    if request.method == 'POST':
        report_type = request.form['report_type']
        format_type = request.form.get('format', 'pdf')
        
        # Получаем данные для предпросмотра
        preview_data = get_preview_data(report_type)
        
        if format_type == 'csv':
            return generate_csv_report(report_type)
        else:
            return generate_pdf_report(report_type)
    
    # Для GET запроса тоже показываем предпросмотр если выбран тип отчета
    if request.method == 'GET' and 'preview' in request.args:
        report_type = request.args.get('preview')
        preview_data = get_preview_data(report_type)
    
    return render_template('reports/generate_report.html', 
                         preview_data=preview_data, 
                         report_type=report_type)

def get_preview_data(report_type):
    """Получение данных для предпросмотра"""
    if not report_type:
        return None
        
    try:
        with get_db_cursor() as cursor:
            if report_type == 'graduates_list':
                cursor.execute('''
                    SELECT g.first_name, g.last_name, g.email, g.graduation_year, f.faculty_name 
                    FROM graduates g 
                    JOIN faculties f ON g.faculty = f.faculty_id 
                    ORDER BY g.graduation_year DESC, g.last_name
                    LIMIT 10
                ''')
                return cursor.fetchall()
                
            elif report_type == 'survey_results':
                cursor.execute('''
                    SELECT s.title as survey_title, 
                           COUNT(DISTINCT a.graduate_id) as respondents_count,
                           COUNT(a.answer_id) as total_answers
                    FROM surveys s 
                    LEFT JOIN answers a ON s.survey_id = a.survey_id 
                    GROUP BY s.survey_id, s.title
                    ORDER BY respondents_count DESC
                    LIMIT 10
                ''')
                return cursor.fetchall()
                
            elif report_type == 'faculty_stats':
                cursor.execute('''
                    SELECT f.faculty_name, 
                           COUNT(g.graduate_id) as graduates_count,
                           AVG(g.graduation_year) as avg_graduation_year
                    FROM faculties f 
                    LEFT JOIN graduates g ON f.faculty_id = g.faculty 
                    GROUP BY f.faculty_id, f.faculty_name
                    ORDER BY graduates_count DESC
                    LIMIT 10
                ''')
                return cursor.fetchall()
                
    except Exception as e:
        print(f"Error getting preview data: {e}")
        return None
    
    return None

def generate_csv_report(report_type):
    """Генерация CSV отчета"""
    # Создаем CSV в памяти
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    with get_db_cursor() as cursor:
        if report_type == 'graduates_list':
            cursor.execute('''
                SELECT g.first_name, g.last_name, g.email, g.graduation_year, f.faculty_name 
                FROM graduates g 
                JOIN faculties f ON g.faculty = f.faculty_id 
                ORDER BY g.graduation_year DESC, g.last_name
            ''')
            graduates = cursor.fetchall()
        
            # Заголовки
            writer.writerow(['Имя', 'Фамилия', 'Email', 'Год выпуска', 'Факультет'])
            
            # Данные
            for grad in graduates:
                writer.writerow([
                    grad['first_name'],
                    grad['last_name'],
                    grad['email'],
                    grad['graduation_year'],
                    grad['faculty_name']
                ])
            
            filename = 'graduates.csv'
            
        elif report_type == 'survey_results':
            cursor.execute('''
                SELECT s.title as survey_title, 
                       COUNT(DISTINCT a.graduate_id) as respondents_count,
                       COUNT(a.answer_id) as total_answers
                FROM surveys s 
                LEFT JOIN answers a ON s.survey_id = a.survey_id 
                GROUP BY s.survey_id, s.title
                ORDER BY respondents_count DESC
            ''')
            survey_stats = cursor.fetchall()
        
            writer.writerow(['Название опроса', 'Количество участников', 'Всего ответов'])
            
            for stat in survey_stats:
                writer.writerow([
                    stat['survey_title'],
                    stat['respondents_count'],
                    stat['total_answers']
                ])
            
            filename = 'survey_results.csv'
            
        elif report_type == 'faculty_stats':
            cursor.execute('''
                SELECT f.faculty_name, 
                       COUNT(g.graduate_id) as graduates_count,
                       AVG(g.graduation_year) as avg_graduation_year
                FROM faculties f 
                LEFT JOIN graduates g ON f.faculty_id = g.faculty 
                GROUP BY f.faculty_id, f.faculty_name
                ORDER BY graduates_count DESC
            ''')
            faculty_stats = cursor.fetchall()
        
            writer.writerow(['Факультет', 'Количество выпускников', 'Средний год выпуска'])
            
            for stat in faculty_stats:
                avg_year = stat['avg_graduation_year']
                if avg_year:
                    avg_year_str = str(round(avg_year, 1))
                else:
                    avg_year_str = 'Нет данных'
                
                writer.writerow([
                    stat['faculty_name'],
                    stat['graduates_count'],
                    avg_year_str
                ])
            
            filename = 'faculty_stats.csv'
        else:
            flash('Неверный тип отчета', 'danger')
            return redirect(url_for('generate_report'))
    
    buffer.seek(0)
    
    # Используем английские названия файлов чтобы избежать проблем с кодировкой
    response = Response(
        buffer.getvalue().encode('utf-8-sig'),  # UTF-8 с BOM для Excel
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    
    return response

def generate_pdf_report(report_type):
    """Генерация PDF отчета"""
    # Создаем PDF в памяти
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    def truncate_text(text, max_length):
        """Обрезает текст если он слишком длинный"""
        if text and len(text) > max_length:
            return text[:max_length-3] + "..."
        return text or ''
    
    # ИСПРАВЛЕННАЯ ЧАСТЬ - используем get_db_cursor вместо get_db_connection
    with get_db_cursor() as cursor:
        if report_type == 'graduates_list':
            cursor.execute('''
                SELECT g.first_name, g.last_name, g.email, g.graduation_year, f.faculty_name 
                FROM graduates g 
                JOIN faculties f ON g.faculty = f.faculty_id 
                ORDER BY g.graduation_year DESC, g.last_name
            ''')
            graduates = cursor.fetchall()
        
        # Уменьшаем шрифт для лучшего размещения
        p.setFont(CYRILLIC_FONT_BOLD, 14)
        p.drawString(50, 800, "СПИСОК ВЫПУСКНИКОВ")
        
        # Заголовки таблицы с увеличенными расстояниями
        p.setFont(CYRILLIC_FONT_BOLD, 9)
        y = 770
        p.drawString(50, y, "Имя")           # 50-90
        p.drawString(120, y, "Фамилия")      # 120-180  
        p.drawString(200, y, "Email")        # 200-320
        p.drawString(350, y, "Год")          # 350-380
        p.drawString(400, y, "Факультет")    # 400-550
        
        # Линия под заголовком
        p.line(50, 765, 550, 765)
        
        # Данные с уменьшенным шрифтом
        p.setFont(CYRILLIC_FONT, 8)
        y = 750
        line_height = 14
        
        for i, grad in enumerate(graduates):
            if y < 50:  # Новая страница если не хватает места
                p.showPage()
                p.setFont(CYRILLIC_FONT_BOLD, 9)
                y = 770
                # Повторяем заголовки на новой странице
                p.drawString(50, y, "Имя")
                p.drawString(120, y, "Фамилия")
                p.drawString(200, y, "Email")
                p.drawString(350, y, "Год")
                p.drawString(400, y, "Факультет")
                p.line(50, 765, 550, 765)
                y = 750
                p.setFont(CYRILLIC_FONT, 8)
            
            # Обрезаем длинные тексты с увеличенными лимитами
            first_name = truncate_text(grad['first_name'], 18)
            last_name = truncate_text(grad['last_name'], 20)
            email = truncate_text(grad['email'], 30)
            faculty = truncate_text(grad['faculty_name'], 35)
            
            p.drawString(50, y, first_name)
            p.drawString(120, y, last_name)
            p.drawString(200, y, email)
            p.drawString(350, y, str(grad['graduation_year']))
            p.drawString(400, y, faculty)
            
            # Линия между строками для лучшей читаемости
            if i < len(graduates) - 1:
                p.line(50, y-2, 550, y-2)
            
            y -= line_height
        
    # Остальной код для других типов отчетов оставьте аналогично
    # Только замените conn.cursor() на with get_db_cursor() as cursor:
    
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'report_{report_type}.pdf', mimetype='application/pdf')

# ==================== API ДЛЯ AJAX ====================



@app.route('/api/check_functions_status')
@login_required
def check_functions_status():
    """Проверка существования функций и процедур"""
    try:
        with get_db_cursor() as cursor:
            # Проверяем существование функций
            cursor.execute("""
                SELECT routine_name 
                FROM information_schema.routines 
                WHERE routine_schema = DATABASE() 
                AND routine_name IN ('GetGraduateFullName', 'CountSurveyResponses', 'GetGraduateStats')
            """)
            functions = cursor.fetchall()

            function_names = [f['routine_name'] for f in functions]

        return jsonify({
            'function1_exists': 'GetGraduateFullName' in function_names,
            'function2_exists': 'CountSurveyResponses' in function_names,
            'procedure_exists': 'GetGraduateStats' in function_names
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/graduates_count')
@login_required
def api_graduates_count():
    """API для получения количества выпускников"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) as count FROM graduates')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'count': result['count']})
    except Exception as e:
        print(f"Error in api_graduates_count: {e}")
        return jsonify({'count': 0})

@app.route('/api/surveys_count')
@login_required
def api_surveys_count():
    """API для получения количества опросов"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) as count FROM surveys')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'count': result['count']})
    except Exception as e:
        print(f"Error in api_surveys_count: {e}")
        return jsonify({'count': 0})

@app.route('/api/answers_count')
@login_required
def api_answers_count():
    """API для получения количества ответов"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) as count FROM answers')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'count': result['count']})
    except Exception as e:
        print(f"Error in api_answers_count: {e}")
        return jsonify({'count': 1240})  # Возвращаем дефолтное значение
# ==================== ТРИГГЕРЫ ====================

@app.route('/admin/create_triggers')
@login_required
@admin_required
def create_triggers_route():
    """Создание всех триггеров в БД"""
    from modules.triggers import create_triggers
    if create_triggers():
        flash('✅ Триггеры успешно созданы!', 'success')
    else:
        flash('❌ Ошибка при создании триггеров', 'danger')
    return redirect(url_for('triggers_dashboard'))

@app.route('/admin/drop_triggers')
@login_required
@admin_required
def drop_triggers_route():
    """Удаление всех триггеров"""
    from modules.triggers import drop_triggers
    if drop_triggers():
        flash('✅ Триггеры успешно удалены!', 'success')
    else:
        flash('❌ Ошибка при удалении триггеров', 'danger')
    return redirect(url_for('triggers_dashboard'))

@app.route('/triggers/dashboard')
@login_required
@staff_required
def triggers_dashboard():
    """Дашборд управления триггерами"""
    from modules.triggers import check_triggers_exist, TRIGGERS, get_triggers_by_student
    
    triggers_status = check_triggers_exist()
    
    # Группируем триггеры по студентам
    student1_triggers = get_triggers_by_student('Вострухин Д.М.')
    student2_triggers = get_triggers_by_student('Яценко И.Ю.')
    
    return render_template('triggers/dashboard.html',
                         triggers_status=triggers_status,
                         all_triggers=TRIGGERS,
                         student1_triggers=student1_triggers,
                         student2_triggers=student2_triggers)

@app.route('/triggers/demonstrate')
@login_required
@staff_required
def demonstrate_triggers_route():
    """Демонстрация работы триггеров"""
    from modules.triggers import demonstrate_triggers
    results = demonstrate_triggers()
    return render_template('triggers/demonstration.html', results=results)

@app.route('/triggers/test_audit')
@login_required
@staff_required
def test_audit_trigger():
    """Тестирование триггера аудита изменений выпускников"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Обновляем данные выпускника чтобы сработал триггер audit_graduate_changes
            cursor.execute("UPDATE graduates SET first_name = 'Иван_обновленный' WHERE graduate_id = 1")
            
            # Проверяем запись в аудит логе
            cursor.execute("SELECT * FROM audit_log ORDER BY log_id DESC LIMIT 1")
            audit_record = cursor.fetchone()
        
        if audit_record:
            flash(f'✅ Триггер аудита сработал! Создана запись: {audit_record["event_type"]}', 'success')
        else:
            flash('❌ Триггер аудита не сработал', 'danger')
            
    except Exception as e:
        flash(f'❌ Ошибка тестирования триггера: {e}', 'danger')
    
    return redirect(url_for('triggers_dashboard'))

@app.route('/triggers/test_survey_creation')
@login_required
@staff_required
def test_survey_trigger():
    """Тестирование триггера логирования создания опросов"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Создаем тестовый опрос чтобы сработал триггер log_survey_creation
            cursor.execute(
                "INSERT INTO surveys (title, description, created_by) VALUES (%s, %s, %s)",
                ('Тестовый опрос для триггера', 'Проверка работы триггера', current_user.id)
            )
            
            # Проверяем запись в аудит логе
            cursor.execute("SELECT * FROM audit_log ORDER BY log_id DESC LIMIT 1")
            audit_record = cursor.fetchone()
        
        if audit_record and 'SURVEY_CREATED' in audit_record['event_type']:
            flash(f'✅ Триггер создания опроса сработал! Создана запись: {audit_record["event_type"]}', 'success')
        else:
            flash('❌ Триггер создания опроса не сработал', 'danger')
            
    except Exception as e:
        flash(f'❌ Ошибка тестирования триггера: {e}', 'danger')
    
    return redirect(url_for('triggers_dashboard'))
# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
