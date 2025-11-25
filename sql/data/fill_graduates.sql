-- Очищаем старые данные (если нужно)
DELETE FROM answers;
DELETE FROM graduates;
ALTER TABLE graduates AUTO_INCREMENT = 1;

-- Добавляем 50 выпускников с реалистичными годами выпуска
INSERT INTO graduates (first_name, last_name, email, graduation_year, faculty) VALUES
('Иван', 'Петров', 'ivan.petrov@email.com', 2020, 1),
('Мария', 'Сидорова', 'maria.sidorova@email.com', 2021, 2),
('Алексей', 'Козлов', 'alex.kozlov@email.com', 2019, 3),
('Елена', 'Иванова', 'elena.ivanova@email.com', 2022, 1),
('Дмитрий', 'Смирнов', 'dmitry.smirnov@email.com', 2020, 4),
('Ольга', 'Кузнецова', 'olga.kuznetsova@email.com', 2021, 2),
('Сергей', 'Попов', 'sergey.popov@email.com', 2018, 1),
('Анна', 'Васильева', 'anna.vasilyeva@email.com', 2023, 3),
('Михаил', 'Павлов', 'mikhail.pavlov@email.com', 2019, 2),
('Наталья', 'Семенова', 'natalia.semenova@email.com', 2020, 1),
('Андрей', 'Голубев', 'andrey.golubev@email.com', 2021, 4),
('Екатерина', 'Виноградова', 'ekaterina.vinogradova@email.com', 2022, 3),
('Артем', 'Богданов', 'artem.bogdanov@email.com', 2019, 2),
('Юлия', 'Воробьева', 'yulia.vorobyeva@email.com', 2020, 1),
('Павел', 'Федоров', 'pavel.fedorov@email.com', 2021, 4),
('Ирина', 'Михайлова', 'irina.mikhailova@email.com', 2018, 3),
('Владимир', 'Белов', 'vladimir.belov@email.com', 2022, 2),
('Светлана', 'Тимофеева', 'svetlana.timofeeva@email.com', 2020, 1),
('Александр', 'Морозов', 'alexander.morozov@email.com', 2021, 4),
('Татьяна', 'Андреева', 'tatyana.andreeva@email.com', 2019, 3),
('Никита', 'Зайцев', 'nikita.zaytsev@email.com', 2020, 2),
('Марина', 'Ершова', 'marina.ershova@email.com', 2021, 1),
('Роман', 'Григорьев', 'roman.grigoryev@email.com', 2022, 4),
('Людмила', 'Соколова', 'lyudmila.sokolova@email.com', 2018, 3),
('Станислав', 'Лебедев', 'stanislav.lebedev@email.com', 2020, 2),
('Виктория', 'Медведева', 'victoria.medvedeva@email.com', 2021, 1),
('Григорий', 'Киселев', 'grigory.kiselev@email.com', 2019, 4),
('Алина', 'Новикова', 'alina.novikova@email.com', 2022, 3),
('Константин', 'Макаров', 'konstantin.makarov@email.com', 2020, 2),
('Оксана', 'Орлова', 'oksana.orlova@email.com', 2021, 1),
('Вадим', 'Захаров', 'vadim.zakharov@email.com', 2018, 4),
('Евгения', 'Романова', 'evgeniya.romanova@email.com', 2022, 3),
('Тимур', 'Субботин', 'timur.subbotin@email.com', 2020, 2),
('Ангелина', 'Филиппова', 'angelina.filippova@email.com', 2021, 1),
('Даниил', 'Комарова', 'danil.komarov@email.com', 2019, 4),
('Кристина', 'Дмитриева', 'kristina.dmitrieva@email.com', 2022, 3),
('Валерий', 'Антонов', 'valery.antonov@email.com', 2020, 2),
('Яна', 'Тарасова', 'yana.tarasova@email.com', 2021, 1),
('Георгий', 'Давыдов', 'georgy.davydov@email.com', 2018, 4),
('Вероника', 'Жукова', 'veronika.zhukova@email.com', 2022, 3),
('Артур', 'Степанов', 'artur.stepanov@email.com', 2020, 2),
('Диана', 'Фролова', 'diana.frolova@email.com', 2021, 1),
('Руслан', 'Максимов', 'ruslan.maksimov@email.com', 2019, 4),
('Элина', 'Куликова', 'elina.kulikova@email.com', 2022, 3),
('Игорь', 'Карпов', 'igor.karpov@email.com', 2020, 2),
('Лариса', 'Афанасьева', 'larisa.afanaseva@email.com', 2021, 1),
('Семен', 'Власов', 'semen.vlasov@email.com', 2018, 4),
('Регина', 'Маслова', 'regina.maslova@email.com', 2022, 3),
('Юрий', 'Исаев', 'yury.isaev@email.com', 2020, 2),
('Алла', 'Титова', 'alla.titova@email.com', 2021, 1);

-- Добавляем реалистичные ответы на опросы
INSERT IGNORE INTO answers (survey_id, graduate_id, question_id, choice_id) VALUES
-- Ответы на опрос 1 (Удовлетворенность учебным процессом)
(1, 1, 1, 1), (1, 1, 2, 1),
(1, 2, 1, 2), (1, 2, 2, 2),
(1, 3, 1, 3), (1, 3, 2, 3),
(1, 4, 1, 1), (1, 4, 2, 1),
(1, 5, 1, 4), (1, 5, 2, 4),

-- Ответы на опрос 2 (Карьерные достижения)
(2, 1, 3, 1), (2, 1, 4, 3),
(2, 2, 3, 2), (2, 2, 4, 2),
(2, 3, 3, 3), (2, 3, 4, 1),
(2, 4, 3, 1), (2, 4, 4, 4),
(2, 5, 3, 2), (2, 5, 4, 2),

-- Ответы на опрос 3 (Оценка инфраструктуры)
(3, 6, 1, 2), (3, 6, 2, 1),
(3, 7, 1, 1), (3, 7, 2, 2),
(3, 8, 1, 3), (3, 8, 2, 3),
(3, 9, 1, 4), (3, 9, 2, 4),
(3, 10, 1, 1), (3, 10, 2, 1);

SELECT 'Данные успешно добавлены!' as status;
SELECT COUNT(*) as total_graduates FROM graduates;
SELECT COUNT(*) as total_answers FROM answers;
