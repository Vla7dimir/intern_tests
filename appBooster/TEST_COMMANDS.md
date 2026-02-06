# Команды для запуска тестов

## Установка зависимостей

```bash
cd /Users/rinatkurmakaev/intern_tests/appBooster
pip install -r requirements.txt
```

Или с виртуальным окружением:

```bash
cd /Users/rinatkurmakaev/intern_tests/appBooster
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск тестов

### Базовый запуск всех тестов

```bash
pytest
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск конкретного файла тестов

```bash
pytest tests/test_api.py -v
```

### Запуск конкретного теста

```bash
pytest tests/test_api.py::test_get_experiments_new_device -v
```

### Запуск с покрытием кода

```bash
pytest --cov=app --cov-report=term-missing
```

### Запуск с HTML отчетом о покрытии

```bash
pytest --cov=app --cov-report=html
```

После выполнения откройте `htmlcov/index.html` в браузере для просмотра отчета.

### Запуск с минимальным покрытием 70%

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=70
```

### Запуск с выводом print statements

```bash
pytest -v -s
```

### Запуск только упавших тестов (после первого прогона)

```bash
pytest --lf
```

### Запуск с остановкой на первой ошибке

```bash
pytest -x
```

## Рекомендуемые команды

**Для разработки:**
```bash
pytest -v --cov=app --cov-report=term-missing
```

**Для CI/CD:**
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=70
```

**Для быстрой проверки:**
```bash
pytest -v
```
