-- sql/functions/create_procedures.sql
-- Создание хранимых процедур

USE graduate_surveys;

-- Процедура 1: Статистика выпускников по году
DROP PROCEDURE IF EXISTS GetGraduateStats;
DELIMITER $$
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
END$$
DELIMITER ;

-- Процедура 2: Статистика по факультету
DROP PROCEDURE IF EXISTS GetFacultyGraduatesStats;
DELIMITER $$
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
END$$
DELIMITER ;

-- Процедура 3: Статистика ответов на опрос
DROP PROCEDURE IF EXISTS GetSurveyResponseStats;
DELIMITER $$
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
END$$
DELIMITER ;
