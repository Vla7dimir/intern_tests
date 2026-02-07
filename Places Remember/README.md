# Places Remember

Веб-приложение для впечатлений о посещаемых местах. Задание: [Task-itself.md](Task-itself.md).

**Возможности:** вход через VK/Google (OAuth2), список воспоминаний, добавление места на карте (Leaflet), название и комментарий.

**Стек:** Python 3.10+, Django 4.2, Bootstrap 5, Leaflet, SQLite (или PostgreSQL).

---

## Запуск

```bash
cd "Places Remember/my_django_project"
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example .env   # при необходимости задать ключи VK/Google
python manage.py migrate
python manage.py runserver 8000
```

Открыть: **http://127.0.0.1:8000/**

`.env` — в `Places Remember/` или `my_django_project/`. OAuth: [VK ID](https://id.vk.com/), [Google Console](https://console.cloud.google.com/apis/credentials) (тип «Веб-приложение», redirect URI: `http://127.0.0.1:8000/complete/google-oauth2/`).

---

## Скриншоты

**Главная (кнопки входа)**

![Главная](my_django_project/screens/главная%20страница.png)

**Авторизация через Google**

![Авторизация Google](my_django_project/screens/авторизация%20в%20гугле.png)

![Авторизация Google — шаг 2](my_django_project/screens/авторизация%20в%20гугле%202.png)

**Список воспоминаний**

![Список воспоминаний](my_django_project/screens/список%20воспоминаний.png)

**Страница воспоминания**

![Страница воспоминания](my_django_project/screens/страница%20воспоминаний.png)

**Добавление воспоминания (карта)**

![Добавить воспоминание](my_django_project/screens/добавить%20воспоминания.png)

---

## Тесты и Docker

```bash
pytest places_remember/tests/ -v
# с покрытием: pytest places_remember/tests/ --cov=places_remember --cov-report=term-missing
```

Docker: из каталога `Places Remember/` — `docker-compose up --build`. Линтер: `flake8 my_django_project/ places_remember/` (настройки в `setup.cfg`).
