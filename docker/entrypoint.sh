#!/bin/env bash

# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "postgres" -c '\q'; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done

exec "$@"
