-- create_functions_as_root.sql
-- Выполните: mysql -u root -p < create_functions_as_root.sql

USE graduate_surveys;

-- Временно включаем настройку
SET GLOBAL log_bin_trust_function_creators = 1;

-- Функция 1
DROP FUNCTION IF EXISTS GetGraduateFullName;
DELIMITER $$
CREATE FUNCTION GetGraduateFullName(graduate_id_param INT)
RETURNS VARCHAR(255)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE result_name VARCHAR(255);
    SELECT CONCAT(first_name, ' ', last_name) INTO result_name 
    FROM graduates WHERE graduate_id = graduate_id_param;
    RETURN result_name;
END$$
DELIMITER ;

-- Функция 2
DROP FUNCTION IF EXISTS CountSurveyResponses;
DELIMITER $$
CREATE FUNCTION CountSurveyResponses(survey_id_param INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE result_count INT;
    SELECT COUNT(*) INTO result_count 
    FROM answers WHERE survey_id = survey_id_param;
    RETURN result_count;
END$$
DELIMITER ;

-- Выключаем настройку обратно
SET GLOBAL log_bin_trust_function_creators = 0;

SELECT '✅ Функции успешно созданы!' as status;
