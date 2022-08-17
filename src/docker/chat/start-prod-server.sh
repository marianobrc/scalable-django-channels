#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8001 config.asgi:application
