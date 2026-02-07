# Как работает прокси

## Процесс получения страницы

### 1. Пользователь делает запрос к прокси

```
Браузер → http://127.0.0.1:8232/item?id=123
```

### 2. Прокси формирует URL для Hacker News

В коде (`cmd/server/main.py`):
```python
target_url = f'{settings.hn_base_url}/{path}'
# Результат: https://news.ycombinator.com/item?id=123
```

### 3. Прокси делает HTTP запрос к Hacker News

Используется библиотека `httpx` для асинхронного HTTP запроса:

```python
async with httpx.AsyncClient() as client:
    response = await client.get(target_url, follow_redirects=True, timeout=30.0)
```

**Что происходит:**
- Создается HTTP клиент
- Выполняется GET запрос к `https://news.ycombinator.com/item?id=123`
- Hacker News возвращает HTML страницу
- Прокси получает полный HTML контент

### 4. Прокси получает HTML ответ

```python
response.text  # Полный HTML код страницы
response.status_code  # HTTP статус (200, 404, и т.д.)
response.headers  # HTTP заголовки
```

### 5. Прокси модифицирует HTML

```python
processed_html = process_html(response.text, proxy_url)
```

**Что модифицируется:**
- Текст: добавляется ™ после слов из 6 букв
- Ссылки: заменяются на ссылки прокси
- Формы: action заменяется на прокси

### 6. Прокси возвращает модифицированный HTML

```python
return HTMLResponse(content=processed_html, status_code=response.status_code)
```

Браузер получает модифицированный HTML и отображает его.

## Схема работы

```
┌─────────┐                    ┌──────────────┐                    ┌─────────────┐
│ Браузер │                    │   Прокси     │                    │ Hacker News │
│         │                    │              │                    │             │
│ 1. GET  │───────────────────▶│              │                    │             │
│ /item   │                    │              │                    │             │
│         │                    │ 2. GET       │───────────────────▶│             │
│         │                    │ https://...  │                    │             │
│         │                    │              │                    │ 3. HTML     │
│         │                    │              │◀───────────────────│ ответ       │
│         │                    │              │                    │             │
│         │                    │ 4. Модификация HTML                │             │
│         │                    │ - Добавить ™                     │             │
│         │                    │ - Заменить ссылки                │             │
│         │                    │              │                    │             │
│         │◀───────────────────│ 5. Модифицированный HTML         │             │
│         │                    │              │                    │             │
└─────────┘                    └──────────────┘                    └─────────────┘
```

## Пример запроса

**Запрос пользователя:**
```http
GET http://127.0.0.1:8232/item?id=123
```

**Прокси делает запрос:**
```http
GET https://news.ycombinator.com/item?id=123
```

**Hacker News возвращает:**
```html
<html>
  <body>
    <p>The visual description of the colliding files</p>
    <a href="/item?id=456">Next article</a>
  </body>
</html>
```

**Прокси модифицирует и возвращает:**
```html
<html>
  <body>
    <p>The visual™ description™ of the colliding files</p>
    <a href="http://127.0.0.1:8232/item?id=456">Next article</a>
  </body>
</html>
```

## Технические детали

### HTTP клиент (httpx)

`httpx` - это асинхронная библиотека для HTTP запросов в Python:

```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

**Параметры:**
- `follow_redirects=True` - следовать редиректам
- `timeout=30.0` - таймаут 30 секунд

### Асинхронность

Используется `async/await` для неблокирующих запросов:
- Пока прокси ждет ответ от HN, он может обрабатывать другие запросы
- Это позволяет обрабатывать много запросов одновременно

### Обработка ошибок

```python
try:
    response = await client.get(target_url, ...)
    response.raise_for_status()
    # Обработка успешного ответа
except httpx.HTTPError:
    return HTMLResponse(content='Error fetching page', status_code=500)
```

Если HN недоступен или вернул ошибку, прокси вернет сообщение об ошибке.

## Отличие от редиректа

**Редирект (HTTP 302):**
```
Браузер → Прокси → Редирект → Браузер идет на HN напрямую
```

**Проксирование:**
```
Браузер → Прокси → HN → Прокси → Модификация → Браузер
```

Браузер всегда остается на адресе прокси, но видит контент с HN.
