#!/bin/bash

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

npm install
poetry config virtualenvs.in-project true
poetry install
poetry shell
screen -S app
.venv/bin/python manage.py migrate
# .venv/bin/python manage.py seeds
.venv/bin/python manage.py manage.py runserver 0.0.0.0:8000
tail -f /dev/null