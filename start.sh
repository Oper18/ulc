#!/bin/bash

gunicorn -b 0.0.0.0:8000 --access-logfile - --error-logfile - ulc.wsgi &
celery -A accounts worker -l info -B
