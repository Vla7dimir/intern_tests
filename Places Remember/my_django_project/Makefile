.PHONY: runserver migrate migrations test flake8

runserver:
	python manage.py runserver

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

test:
	python -m pytest places_remember/tests/ -v

cov:
	python -m pytest places_remember/tests/ --cov=places_remember --cov-report=term-missing

flake8:
	flake8 .
