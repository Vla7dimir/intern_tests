# Places Remember

Веб-приложение для хранения впечатлений о посещаемых местах. Задание: [Task-itself.md](Task-itself.md).

## Возможности

- Вход через **VK** или **Google** (OAuth2)
- Главная страница: приветствие для гостей, список воспоминаний для авторизованных
- Добавление воспоминания: выбор точки на карте (Leaflet), название и комментарий
- Выход из аккаунта; после повторного входа список воспоминаний сохраняется

## Стек

- Python 3.10+
- Django 4.2
- python-social-auth (VK, Google)
- Bootstrap 5, Leaflet
- SQLite по умолчанию (опционально PostgreSQL)
- pytest-django для тестов

## Установка и запуск

### 1. Виртуальное окружение и зависимости (обязательно при первом запуске)

Из корня репозитория или из каталога `Places Remember`:

```bash
cd "Places Remember/my_django_project"
python3 -m venv .venv
source .venv/bin/activate   
pip install -r ../requirements.txt
```

Без активации `.venv` будет ошибка `ModuleNotFoundError: No module named 'django'`.

### 2. Переменные окружения

Скопируйте пример в **корень проекта** (каталог `Places Remember/`), иначе `settings` не подхватит переменные:

```bash
cd "Places Remember"
cp .env.example .env
```

Для локальной разработки можно оставить значения по умолчанию (SQLite, DEBUG=True). Для входа через VK/Google укажите ключи в `.env` (см. .env.example).

### 3. Миграции и запуск

Убедитесь, что виртуальное окружение активировано (`source .venv/bin/activate`), затем **обязательно** примените миграции (один раз или после pull):

```bash
cd "Places Remember/my_django_project"
python manage.py migrate
python manage.py runserver 8000
```

Если при запуске видите *«You have 35 unapplied migration(s)»* — остановите сервер (Ctrl+C), выполните `python manage.py migrate`, затем снова `python manage.py runserver 8000`.

Откройте в браузере: **http://127.0.0.1:8000/**



Если видите `{"detail":"Not Found"}`, на порту 8000 запущено другое приложение (например FastAPI). Остановите его или запустите Django на другом порту: `python manage.py runserver 8001` и откройте http://127.0.0.1:8001/

## Тесты

```bash
cd my_django_project
pytest places_remember/tests/ -v
```

С покрытием:

```bash
pytest places_remember/tests/ --cov=places_remember --cov-report=term-missing
```

## Линтеры

- **flake8** (PEP8): `flake8 my_django_project/ places_remember/`
- Настройки в `setup.cfg` (max-line-length 119, исключены миграции и venv).

## Структура проекта

```
Places Remember/
├── .env.example
├── requirements.txt
├── Task-itself.md
├── my_django_project/
│   ├── manage.py
│   ├── my_django_project/          # конфиг Django
│   │   ├── settings.py
│   │   └── urls.py
│   └── places_remember/            # приложение
│       ├── models.py               # CustomUser (avatar_url), Memory (user, title, comment, lat, lng)
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       ├── pipeline.py             # сохранение аватарки из VK/Google
│       ├── templates/
│       │   ├── base.html
│       │   └── places_remember/
│       │       ├── index.html      # приветствие + кнопки входа
│       │       ├── memory_list.html
│       │       └── form.html       # карта + форма добавления
│       └── tests/
│           ├── test_models.py
│           ├── test_views.py
│           └── test_forms.py
│   └── screens/                  # скрины реализации
│       └── README.md             # описание скриншотов
```

## База данных

По умолчанию используется SQLite (`db.sqlite3` в каталоге `my_django_project/`). Для PostgreSQL задайте в `.env`:

- `DB_ENGINE=postgresql`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## OAuth (VK / Google)

Если ключи не заданы в `.env`, кнопки «Войти через VK» и «Войти через Google» на главной не показываются (ошибка «Missing required parameter: client_id» не возникнет).

**VK:** создайте приложение в [VK ID](https://id.vk.com/), укажите в `.env`:
- `SOCIAL_AUTH_VK_OAUTH2_KEY`
- `SOCIAL_AUTH_VK_OAUTH2_SECRET`

**Google:** в [Google Cloud Console](https://console.cloud.google.com/apis/credentials) создайте «OAuth 2.0 Client ID» (тип «Веб-приложение»), укажите в «Authorized redirect URIs»:
- `http://127.0.0.1:8000/complete/google-oauth2/`

В `.env` пропишите:
- `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` (Client ID)
- `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` (Client Secret)

После изменения `.env` перезапустите `runserver`.

## Docker (опционально)

Из корня репозитория (`Places Remember/`):

```bash
cp .env.example .env
docker-compose up --build
```

Приложение будет доступно по адресу http://localhost:8000/

В `.env` для Docker можно оставить `ALLOWED_HOSTS=localhost,127.0.0.1`. При доступе по другому имени хоста добавьте его в `ALLOWED_HOSTS` или задайте `ALLOWED_HOSTS=*` только для локальной разработки.

