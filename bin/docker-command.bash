#!/bin/bash

# The next block will read your .env
if [ -f .env ]; then
    export $(cat .env | grep -v ^# | xargs)
fi

#django commands
cd app
python manage.py collectstatic --noinput -i other &
python manage.py migrate
python manage.py livereload --host 0.0.0.0 --port 35729 &
python manage.py runserver 0.0.0.0:8000
