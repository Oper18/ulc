#!/bin/bash

python manage.py runserver 0:8000 &
celery -A accounts worker -l info -B
