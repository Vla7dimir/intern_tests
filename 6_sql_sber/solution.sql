-- Задание Сбербанк #103: вывести список имён сотрудников,
-- получающих большую заработную плату, чем у непосредственного руководителя.

SELECT e.name
FROM employees e
INNER JOIN employees chief ON e.chief_id = chief.id
WHERE e.salary > chief.salary
ORDER BY e.name;
