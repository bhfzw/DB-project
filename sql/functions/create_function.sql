-- Функция 1 - Полное имя выпускника
DROP FUNCTION IF EXISTS GetGraduateFullName;

DELIMITER $$
CREATE FUNCTION GetGraduateFullName(graduate_id_param INT)
RETURNS VARCHAR(255)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE full_name VARCHAR(255);
    SELECT CONCAT(first_name, ' ', last_name) INTO full_name 
    FROM graduates 
    WHERE graduate_id = graduate_id_param;
    RETURN full_name;
END$$
DELIMITER ;

-- Функция 2 - Количество ответов на опрос
DROP FUNCTION IF EXISTS CountSurveyResponses;

DELIMITER $$
CREATE FUNCTION CountSurveyResponses(survey_id_param INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE response_count INT;
    SELECT COUNT(*) INTO response_count 
    FROM answers 
    WHERE survey_id = survey_id_param;
    RETURN response_count;
END$$
DELIMITER ;

-- Процедура - Статистика выпускников
DROP PROCEDURE IF EXISTS GetGraduateStats;

DELIMITER $$
CREATE PROCEDURE GetGraduateStats(IN grad_year INT)
BEGIN
    SELECT 
        COUNT(*) as total_graduates,
        AVG(graduation_year) as avg_year,
        MIN(graduation_year) as min_year,
        MAX(graduation_year) as max_year,
        f.faculty_name
    FROM graduates g
    JOIN faculties f ON g.faculty = f.faculty_id
    WHERE graduation_year >= grad_year
    GROUP BY f.faculty_id, f.faculty_name
    ORDER BY total_graduates DESC;
END$$
DELIMITER ;
