# Hacker News Proxy

HTTP-прокси для Hacker News с модификацией текста: добавление ™ после слов из 6 букв.

## Описание

Прокси получает страницы с Hacker News, модифицирует текст и отдаёт их через свой адрес. При навигации по ссылкам браузер остаётся на адресе прокси.

## Архитектура

Структура в стиле Python-проектов:

- `app/` — основной код
  - `main.py` — FastAPI, прокси-роутер
  - `proxy/` — обработка HTML (™, ссылки, формы)
  - `utils/` — утилиты (модификация текста)
  - `logger.py` — логирование
- `config/` — конфигурация
- `tests/` — тесты

## Основные компоненты

**FastAPI** (`app/main.py`): проксирует запросы к HN, обрабатывает HTML, переписывает ссылки.

**Обработка HTML** (`app/proxy/processor.py`): парсинг BeautifulSoup, ™ после слов из 6 букв, замена ссылок и форм на прокси-URL.

**Текст** (`app/utils/text.py`): регулярное выражение для слов из 6 букв, добавление ™.

## Технологии

- Python 3.9+
- FastAPI, httpx, BeautifulSoup4, lxml, Pydantic

## Установка и запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8232 --reload
```

Прокси: http://127.0.0.1:8232

### Docker

```bash
docker-compose up --build
```

## Использование

Откройте в браузере: http://127.0.0.1:8232 или http://127.0.0.1:8232/item?id=13713480  
Ссылки на HN перенаправляются через прокси.

## Тестирование

```bash
pytest -v
pytest --cov=app --cov-report=term-missing
./run_tests.sh
```

## Структура проекта

```
ivelum/
├── app/
│   ├── main.py
│   ├── logger.py
│   ├── proxy/
│   └── utils/
├── config/
├── tests/
├── screens/
├── run_tests.sh
└── requirements.txt
```

## Переменные окружения

- `HOST` — хост (по умолчанию 127.0.0.1)
- `PORT` — порт (8232)
- `HN_BASE_URL` — URL Hacker News (https://news.ycombinator.com)
- `LOG_LEVEL` — уровень логов (INFO)

## Дополнительно

- `Task.md` — описание задания
- `SCREEN.md` — скриншоты
- `HOW_IT_WORKS.md` — как работает прокси
