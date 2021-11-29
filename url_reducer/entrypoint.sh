#!/bin/sh
while ! mysqladmin ping -h"$DB_HOST" --silent;
do
    sleep 1;
done

python manage.py migrate
python manage.py ensure_domains
python manage.py test


python manage.py collectstatic --noinput

gunicorn -w 2 -b 0.0.0.0:8000 partners.wsgi --timeout 3600 --workers 3