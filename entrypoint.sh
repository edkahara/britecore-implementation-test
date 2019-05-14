#!/bin/sh

echo "Setting up PostgreSQL..."

while ! nc -z db 5432; do
  sleep 1
done

echo "...PostgreSQL setup complete"

python3 manage.py db init

python3 manage.py db migrate

python3 manage.py db upgrade

gunicorn -b 0.0.0.0:5000 manage:app
