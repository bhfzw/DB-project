-- Создание таблиц
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS faculties (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_name VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS graduates (
    graduate_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    graduation_year INT NOT NULL,
    faculty INT,
    FOREIGN KEY (faculty) REFERENCES faculties(faculty_id)
);

CREATE TABLE IF NOT EXISTS surveys (
    survey_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT,
    title VARCHAR(200) NOT NULL,
    section_order INT,
    faculty_target INT,
    FOREIGN KEY (survey_id) REFERENCES surveys(survey_id),
    FOREIGN KEY (faculty_target) REFERENCES faculties(faculty_id)
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT,
    question_text TEXT NOT NULL,
    section_order INT,
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
);

CREATE TABLE IF NOT EXISTS choices (
    choice_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    choice_text VARCHAR(500),
    choice_order INT,
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

CREATE TABLE IF NOT EXISTS answers (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT,
    graduate_id INT,
    question_id INT,
    choice_id INT,
    answer_text TEXT,
    FOREIGN KEY (survey_id) REFERENCES surveys(survey_id),
    FOREIGN KEY (graduate_id) REFERENCES graduates(graduate_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (choice_id) REFERENCES choices(choice_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Вставка тестовых данных
INSERT INTO users (user_name, role) VALUES 
('admin', 'admin'),
('user', 'user'),
('moderator', 'moderator');

INSERT INTO faculties (faculty_name) VALUES 
('Факультет компьютерных наук'),
('Инженерный факультет'),
('Экономический факультет'),
('Юридический факультет'),
('Медицинский факультет');

INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES 
('Иван', 'Петров', 'ivan.petrov@email.com', 2020, 1),
('Мария', 'Сидорова', 'maria.sidorova@email.com', 2021, 2),
('Алексей', 'Козлов', 'alex.kozlov@email.com', 2019, 3),
('Елена', 'Иванова', 'elena.ivanova@email.com', 2022, 1),
('Дмитрий', 'Смирнов', 'dmitry.smirnov@email.com', 2020, 4);

INSERT INTO surveys (title, description, created_by) VALUES 
('Опрос удовлетворенности выпускников 2023', 'Общий опрос для всех выпускников', 1),
('Трудоустройство выпускников IT-факультета', 'Опрос для выпускников факультета компьютерных наук', 1);
