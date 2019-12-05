#!/bin/bash
set -e

until psql --command='\q' --host="$PGHOST" --port="$PGPORT" --username="$PGUSER"
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - running django"

src/manage.py runserver 0.0.0.0:8000
