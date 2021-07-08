#!/bin/bash
while ! nc -z mysqldb 3306; do
  sleep 0.5
done

echo "MySQL started"

flask db init
flask db migrate
flask db upgrade
gunicorn --bind 0.0.0.0:5000 microblog:app
