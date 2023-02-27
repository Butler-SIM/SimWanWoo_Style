#!/bin/sh

echo "Waiting for DATABASE..."
echo "$RDS_HOST $RDS_PORT"

while ! nc -z $RDS_HOST $RDS_PORT; do
    sleep 0.1
done

echo "DATABASE started"

# Migrate
# python manage.py migrate

# Static Files
# python manage.py collectstatic --noinput --settings=config.settings

exec "$@"