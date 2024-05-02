Тестовое задание.
Часть 1.
Для запуска, откройте проект в IDE, в терминале пропишите следующие команды:
docker compose build
docker compose up
Swagger - localhost/docs
Redis Commander - localhost:8191
Также Swagger этого API доступен по адресу http://213.171.3.234/docs, Redis Commander http://213.171.3.234:8191

Часть 2.
Условие: 
Дано две таблицы в СУБД Postgres.
В одной таблице хранятся имена файлов без расширения. В другой хранятся имена файлов с
расширением. Одинаковых названий с разными расширениями быть не может, количество
расширений не определено, помимо wav и mp3 может встретиться что угодно.
Нам необходимо минимальным количеством запросов к СУБД перенести данные о статусе из
таблицы short_names в таблицу full_names.
Необходимо понимать, что на выполнение запросов / время работы скрипта нельзя тратить
больше 10 минут. Лучшее время выполнения этого тестового задания в 2022 году - 45 секунд на
SQL запросе.
Необходимо предоставить два и более варианта решения этой задачи.

Решение 1.
CREATE INDEX part_name_idx on "full_names" ((SPLIT_PART(name, '.', 1)));

UPDATE "full_names"
SET status = "short_names".status
FROM "short_names"
WHERE "short_names".name = SPLIT_PART("full_names".name, '.', 1);

Создаем индекс по выражению SPLIT_PART(name, '.', 1) в таблице "full_names".
Обновляем колонку status таблицы "full_names" на значения "short_names".status
где "short_names".name равно выражению. Я заполнил базу банных записями, согласно заданию и протестировал запрос, он отработал менее чем за 26 секунд. 
Скриншоты отработанного запроса и скрипты заполнения таблиц прилагаю.

Решение 2.
ALTER TABLE "full_names"
ADD COLUMN short_name text;

UPDATE full_names
SET short_name = (regexp_match(name, '^[^.]*'))[1];

CREATE INDEX reg_name_idx ON "full_names" (short_name);

UPDATE "full_names"
SET status = "short_names".status
FROM "short_names"
WHERE "short_names".name = (regexp_match("full_names".name, '^[^.]*'))[1];

ALTER TABLE "full_names"
DROP COLUMN short_name;

Здесь потребовалось создать временную колонку short_name в таблице "full_names" и
заполнить ее именами файлов без расширений с помощью регулярного выражения.
В остальном решение похоже на первое решение. Последним запросом удаляем временную колонку.

Благодарю за уделенно время! Минка Владимир Python developer +7(918)010-86-43 telegram: https://t.me/VladimirKRD123![Создание таблицы shortname](https://github.com/VladimirMinkaKRD/LexicomAI.API/assets/125747669/715220ce-4f23-4e05-8f41-509faf7c66ce)
![Создание таблицы fullname](https://github.com/VladimirMinkaKRD/LexicomAI.API/assets/125747669/ec134bac-fb68-4d11-b417-ba73f0e4fb92)
![Результат](https://github.com/VladimirMinkaKRD/LexicomAI.API/assets/125747669/e6801158-c87e-4496-866b-2b65c9d31105)
