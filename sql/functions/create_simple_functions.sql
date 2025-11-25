-- create_simple_functions.sql
-- Выполните: mysql -u web_user -p graduate_surveys < create_simple_functions.sql

DROP FUNCTION IF EXISTS GetGraduateFullName;
CREATE FUNCTION GetGraduateFullName(graduate_id_param INT)
RETURNS VARCHAR(255)
DETERMINISTIC
NO SQL
RETURN (SELECT CONCAT(first_name, ' ', last_name) FROM graduates WHERE graduate_id = graduate_id_param);

DROP FUNCTION IF EXISTS CountSurveyResponses;
CREATE FUNCTION CountSurveyResponses(survey_id_param INT)
RETURNS INT
DETERMINISTIC
NO SQL
RETURN (SELECT COUNT(*) FROM answers WHERE survey_id = survey_id_param);

SELECT 'Функции успешно созданы!' as status;
