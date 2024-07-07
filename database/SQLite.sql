-- SQLite
-- SELECT show_id FROM ratings WHERE rating >= 6.0 LIMIT 10;
-- SELECT * FROM shows WHERE id = 62614;
-- SELECT * FROM shows WHERE id = 63881;

SELECT * FROM shows WHERE id IN
(SELECT show_id FROM ratings WHERE rating >= 6.0 LIMIT 10);