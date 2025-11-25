-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: graduate_surveys
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answers` (
  `answer_id` int NOT NULL AUTO_INCREMENT,
  `survey_id` int DEFAULT NULL,
  `graduate_id` int DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `choice_id` int DEFAULT NULL,
  `answer_text` text,
  PRIMARY KEY (`answer_id`),
  KEY `survey_id` (`survey_id`),
  KEY `graduate_id` (`graduate_id`),
  KEY `question_id` (`question_id`),
  KEY `choice_id` (`choice_id`),
  CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `surveys` (`survey_id`),
  CONSTRAINT `answers_ibfk_2` FOREIGN KEY (`graduate_id`) REFERENCES `graduates` (`graduate_id`),
  CONSTRAINT `answers_ibfk_3` FOREIGN KEY (`question_id`) REFERENCES `questions` (`question_id`),
  CONSTRAINT `answers_ibfk_4` FOREIGN KEY (`choice_id`) REFERENCES `choices` (`choice_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1241 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
INSERT INTO `answers` VALUES (1201,1,1,1,1,NULL),(1202,1,1,2,1,NULL),(1203,1,2,1,2,NULL),(1204,1,2,2,2,NULL),(1205,1,3,1,3,NULL),(1206,1,3,2,3,NULL),(1207,1,4,1,1,NULL),(1208,1,4,2,1,NULL),(1209,1,5,1,4,NULL),(1210,1,5,2,4,NULL),(1211,2,1,3,1,NULL),(1212,2,1,4,3,NULL),(1213,2,2,3,2,NULL),(1214,2,2,4,2,NULL),(1215,2,3,3,3,NULL),(1216,2,3,4,1,NULL),(1217,2,4,3,1,NULL),(1218,2,4,4,4,NULL),(1219,2,5,3,2,NULL),(1220,2,5,4,2,NULL),(1231,1,51,1,1,NULL),(1232,1,51,2,2,NULL),(1233,1,52,1,1,NULL),(1234,1,52,2,2,NULL),(1235,1,53,1,1,NULL),(1236,1,53,2,2,NULL),(1237,1,54,1,1,NULL),(1238,1,54,2,2,NULL),(1239,1,55,1,1,NULL),(1240,1,55,2,2,NULL);
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `event_type` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,1,'Транзакция: добавлен выпускник 51 с ответами','2025-11-17 06:37:45',NULL),(2,1,'Транзакция: добавлен выпускник с ответами','2025-11-17 08:12:46',NULL),(3,1,'Транзакция: добавлен выпускник с ответами','2025-11-17 08:25:30',NULL),(4,1,'Транзакция: добавлен выпускник с ответами','2025-11-17 08:27:13',NULL),(5,1,'Транзакция: создан опрос с вопросами','2025-11-17 08:27:16',NULL),(6,1,'Транзакция: добавлен выпускник с ответами','2025-11-17 08:42:30',NULL),(7,1,'Транзакция: создан опрос с вопросами','2025-11-17 08:42:33',NULL);
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choices`
--

DROP TABLE IF EXISTS `choices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `choices` (
  `choice_id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `choice_text` varchar(500) DEFAULT NULL,
  `choice_order` int DEFAULT NULL,
  PRIMARY KEY (`choice_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `choices_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choices`
--

LOCK TABLES `choices` WRITE;
/*!40000 ALTER TABLE `choices` DISABLE KEYS */;
INSERT INTO `choices` VALUES (1,1,'Очень доволен',1),(2,1,'Доволен',2),(3,1,'Нейтрально',3),(4,1,'Не доволен',4),(5,2,'Определенно да',1),(6,2,'Вероятно да',2),(7,2,'Затрудняюсь',3),(8,2,'Вероятно нет',4),(9,3,'Отлично',1),(10,3,'Хорошо',2),(11,3,'Удовлетворительно',3),(12,3,'Плохо',4),(13,4,'Более чем достаточно',1),(14,4,'Достаточно',2),(15,4,'Недостаточно',3),(16,4,'Совсем недостаточно',4),(17,5,'Да, полностью',1),(18,5,'Частично',2),(19,5,'Нет',3),(20,6,'Менее 1 месяца',1),(21,6,'1-3 месяца',2),(22,6,'3-6 месяцев',3),(23,6,'Более 6 месяцев',4),(24,7,'До 50 000 руб.',1),(25,7,'50 000 - 100 000 руб.',2),(26,7,'100 000 - 150 000 руб.',3),(27,7,'Свыше 150 000 руб.',4),(28,8,'Да, обязательно',1),(29,8,'Возможно',2),(30,8,'Нет',3),(36,26,'Очень полезны',1),(37,26,'Полезны',2),(38,26,'Нейтрально',3),(39,28,'Очень полезны',1),(40,28,'Полезны',2),(41,28,'Нейтрально',3);
/*!40000 ALTER TABLE `choices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculties`
--

DROP TABLE IF EXISTS `faculties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculties` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `faculty_name` varchar(200) NOT NULL,
  PRIMARY KEY (`faculty_id`),
  UNIQUE KEY `faculty_name` (`faculty_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculties`
--

LOCK TABLES `faculties` WRITE;
/*!40000 ALTER TABLE `faculties` DISABLE KEYS */;
INSERT INTO `faculties` VALUES (2,'Инженерный факультет'),(5,'Медицинский факультет'),(1,'Факультет компьютерных наук'),(3,'Экономический факультет'),(4,'Юридический факультет');
/*!40000 ALTER TABLE `faculties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `graduate_details`
--

DROP TABLE IF EXISTS `graduate_details`;
/*!50001 DROP VIEW IF EXISTS `graduate_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `graduate_details` AS SELECT 
 1 AS `graduate_id`,
 1 AS `full_name`,
 1 AS `email`,
 1 AS `graduation_year`,
 1 AS `faculty_name`,
 1 AS `answers_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `graduates`
--

DROP TABLE IF EXISTS `graduates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graduates` (
  `graduate_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `graduation_year` int NOT NULL,
  `faculty` int DEFAULT NULL,
  PRIMARY KEY (`graduate_id`),
  UNIQUE KEY `email` (`email`),
  KEY `faculty` (`faculty`),
  CONSTRAINT `graduates_ibfk_1` FOREIGN KEY (`faculty`) REFERENCES `faculties` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graduates`
--

LOCK TABLES `graduates` WRITE;
/*!40000 ALTER TABLE `graduates` DISABLE KEYS */;
INSERT INTO `graduates` VALUES (1,'Иван','Петров','ivan.petrov@email.com',2020,1),(2,'Мария','Сидорова','maria.sidorova@email.com',2021,2),(3,'Алексей','Козлов','alex.kozlov@email.com',2019,3),(4,'Елена','Иванова','elena.ivanova@email.com',2022,1),(5,'Дмитрий','Смирнов','dmitry.smirnov@email.com',2020,4),(6,'Ольга','Кузнецова','olga.kuznetsova@email.com',2021,2),(7,'Сергей','Попов','sergey.popov@email.com',2018,1),(8,'Анна','Васильева','anna.vasilyeva@email.com',2023,3),(9,'Михаил','Павлов','mikhail.pavlov@email.com',2019,2),(10,'Наталья','Семенова','natalia.semenova@email.com',2020,1),(11,'Андрей','Голубев','andrey.golubev@email.com',2021,4),(12,'Екатерина','Виноградова','ekaterina.vinogradova@email.com',2022,3),(13,'Артем','Богданов','artem.bogdanov@email.com',2019,2),(14,'Юлия','Воробьева','yulia.vorobyeva@email.com',2020,1),(15,'Павел','Федоров','pavel.fedorov@email.com',2021,4),(16,'Ирина','Михайлова','irina.mikhailova@email.com',2018,3),(17,'Владимир','Белов','vladimir.belov@email.com',2022,2),(18,'Светлана','Тимофеева','svetlana.timofeeva@email.com',2020,1),(19,'Александр','Морозов','alexander.morozov@email.com',2021,4),(20,'Татьяна','Андреева','tatyana.andreeva@email.com',2019,3),(21,'Никита','Зайцев','nikita.zaytsev@email.com',2020,2),(22,'Марина','Ершова','marina.ershova@email.com',2021,1),(23,'Роман','Григорьев','roman.grigoryev@email.com',2022,4),(24,'Людмила','Соколова','lyudmila.sokolova@email.com',2018,3),(25,'Станислав','Лебедев','stanislav.lebedev@email.com',2020,2),(26,'Виктория','Медведева','victoria.medvedeva@email.com',2021,1),(27,'Григорий','Киселев','grigory.kiselev@email.com',2019,4),(28,'Алина','Новикова','alina.novikova@email.com',2022,3),(29,'Константин','Макаров','konstantin.makarov@email.com',2020,2),(30,'Оксана','Орлова','oksana.orlova@email.com',2021,1),(31,'Вадим','Захаров','vadim.zakharov@email.com',2018,4),(32,'Евгения','Романова','evgeniya.romanova@email.com',2022,3),(33,'Тимур','Субботин','timur.subbotin@email.com',2020,2),(34,'Ангелина','Филиппова','angelina.filippova@email.com',2021,1),(35,'Даниил','Комарова','danil.komarov@email.com',2019,4),(36,'Кристина','Дмитриева','kristina.dmitrieva@email.com',2022,3),(37,'Валерий','Антонов','valery.antonov@email.com',2020,2),(38,'Яна','Тарасова','yana.tarasova@email.com',2021,1),(39,'Георгий','Давыдов','georgy.davydov@email.com',2018,4),(40,'Вероника','Жукова','veronika.zhukova@email.com',2022,3),(41,'Артур','Степанов','artur.stepanov@email.com',2020,2),(42,'Диана','Фролова','diana.frolova@email.com',2021,1),(43,'Руслан','Максимов','ruslan.maksimov@email.com',2019,4),(44,'Элина','Куликова','elina.kulikova@email.com',2022,3),(45,'Игорь','Карпов','igor.karpov@email.com',2020,2),(46,'Лариса','Афанасьева','larisa.afanaseva@email.com',2021,1),(47,'Семен','Власов','semen.vlasov@email.com',2018,4),(48,'Регина','Маслова','regina.maslova@email.com',2022,3),(49,'Юрий','Исаев','yury.isaev@email.com',2020,2),(50,'Алла','Титова','alla.titova@email.com',2021,1),(51,'Алексей','Транзакционов','transaction1@email.com',2023,1),(52,'Алексей','Транзакционов','transaction_1763367166_4958@email.com',2023,1),(53,'Алексей','Транзакционов','transaction_1763367930_8161@email.com',2023,1),(54,'Алексей','Транзакционов','transaction_1763368033_1013@email.com',2023,1),(55,'Алексей','Транзакционов','transaction_1763368950_8491@email.com',2023,1);
/*!40000 ALTER TABLE `graduates` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `prevent_duplicate_emails` BEFORE INSERT ON `graduates` FOR EACH ROW BEGIN
    IF (SELECT COUNT(*) FROM graduates WHERE email = NEW.email) > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Email already exists';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `audit_graduate_changes` AFTER UPDATE ON `graduates` FOR EACH ROW BEGIN
    INSERT INTO audit_log (user_id, event_type, timestamp)
    VALUES (1, CONCAT('Graduate updated: ', OLD.first_name, ' ', OLD.last_name), NOW());
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `section_id` int DEFAULT NULL,
  `question_text` text NOT NULL,
  `section_order` int DEFAULT NULL,
  PRIMARY KEY (`question_id`),
  KEY `section_id` (`section_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,1,'Насколько вы довольны качеством образования?',1),(2,1,'Порекомендовали бы вы наш университет?',2),(3,2,'Оцените качество преподавания',1),(4,2,'Хватало ли практических занятий?',2),(5,3,'Устроились ли вы по специальности?',1),(6,3,'Сколько времени заняло трудоустройство?',2),(7,4,'Ваш текущий уровень дохода?',1),(8,4,'Планируете ли вы дальнейшее обучение?',2),(26,14,'Как вы оцените транзакции в БД?',1),(27,14,'Насколько важна целостность данных?',2),(28,15,'Как вы оцените транзакции в БД?',1),(29,15,'Насколько важна целостность данных?',2);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sections` (
  `section_id` int NOT NULL AUTO_INCREMENT,
  `survey_id` int DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `section_order` int DEFAULT NULL,
  `faculty_target` int DEFAULT NULL,
  PRIMARY KEY (`section_id`),
  KEY `survey_id` (`survey_id`),
  KEY `faculty_target` (`faculty_target`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `surveys` (`survey_id`),
  CONSTRAINT `sections_ibfk_2` FOREIGN KEY (`faculty_target`) REFERENCES `faculties` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (1,1,'Общая удовлетворенность',1,NULL),(2,1,'Качество образования',2,NULL),(3,2,'Трудоустройство',1,NULL),(4,2,'Карьера',2,NULL),(14,10,'Основная секция',1,NULL),(15,11,'Основная секция',1,NULL);
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `survey_statistics`
--

DROP TABLE IF EXISTS `survey_statistics`;
/*!50001 DROP VIEW IF EXISTS `survey_statistics`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `survey_statistics` AS SELECT 
 1 AS `survey_id`,
 1 AS `title`,
 1 AS `description`,
 1 AS `created_by`,
 1 AS `unique_respondents`,
 1 AS `total_answers`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `surveys`
--

DROP TABLE IF EXISTS `surveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surveys` (
  `survey_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`survey_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `surveys_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveys`
--

LOCK TABLES `surveys` WRITE;
/*!40000 ALTER TABLE `surveys` DISABLE KEYS */;
INSERT INTO `surveys` VALUES (1,'Опрос удовлетворенности выпускников 2023','Общий опрос для всех выпускников',1),(2,'Трудоустройство выпускников IT-факультета','Опрос для выпускников факультета компьютерных наук',1),(10,'Новый транзакционный опрос','Опрос созданный в рамках транзакции',1),(11,'Новый транзакционный опрос','Опрос созданный в рамках транзакции',1);
/*!40000 ALTER TABLE `surveys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin'),(2,'user','user'),(3,'moderator','moderator');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `graduate_details`
--

/*!50001 DROP VIEW IF EXISTS `graduate_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`web_user`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `graduate_details` AS select `g`.`graduate_id` AS `graduate_id`,concat(`g`.`first_name`,' ',`g`.`last_name`) AS `full_name`,`g`.`email` AS `email`,`g`.`graduation_year` AS `graduation_year`,`f`.`faculty_name` AS `faculty_name`,count(`a`.`answer_id`) AS `answers_count` from ((`graduates` `g` left join `faculties` `f` on((`g`.`faculty` = `f`.`faculty_id`))) left join `answers` `a` on((`g`.`graduate_id` = `a`.`graduate_id`))) group by `g`.`graduate_id`,`g`.`first_name`,`g`.`last_name`,`g`.`email`,`g`.`graduation_year`,`f`.`faculty_name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `survey_statistics`
--

/*!50001 DROP VIEW IF EXISTS `survey_statistics`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`web_user`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `survey_statistics` AS select `s`.`survey_id` AS `survey_id`,`s`.`title` AS `title`,`s`.`description` AS `description`,`u`.`user_name` AS `created_by`,count(distinct `a`.`graduate_id`) AS `unique_respondents`,count(`a`.`answer_id`) AS `total_answers` from ((`surveys` `s` left join `users` `u` on((`s`.`created_by` = `u`.`user_id`))) left join `answers` `a` on((`s`.`survey_id` = `a`.`survey_id`))) group by `s`.`survey_id`,`s`.`title`,`s`.`description`,`u`.`user_name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-17 14:37:52
