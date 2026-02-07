# Тестовое задание Самокат (SQL #97)

## Условие

Посчитать количество работающих складов на текущую дату по каждому городу. Вывести только те города, у которых количество складов более 80.

## Входные данные

Таблица **warehouses**:
- `warehouse_id` — идентификатор склада
- `name` — название
- `city` — город
- `date_open` — дата открытия
- `date_close` — дата закрытия (NULL, если склад работает)

Работающий склад: открыт (`date_open <= CURRENT_DATE`) и не закрыт (`date_close IS NULL` или `date_close > CURRENT_DATE`).

## Формат результата

| city | warehouse_count |
|------|-----------------|
| ...  | ...             |

Поля результирующей таблицы: `city`, `warehouse_count`.

## Решение

```sql
SELECT
    city,
    COUNT(*) AS warehouse_count
FROM warehouses
WHERE date_open <= CURRENT_DATE
  AND (date_close IS NULL OR date_close > CURRENT_DATE)
GROUP BY city
HAVING COUNT(*) > 80
ORDER BY warehouse_count DESC;
```

- **Снимок экрана 2026-02-07 в 01.03.21.png** — скриншот результата
