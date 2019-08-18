FROM python:3.7-alpine

WORKDIR /usr/src/app
COPY conf/requirements.freeze .

RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev postgresql-libs \
    && pip install --no-cache-dir -r requirements.freeze \
    && apk del gcc
COPY . .

WORKDIR /usr/src/app/ya_test

RUN python manage.py collectstatic --noinput

VOLUME /usr/src/app/ya_test/static

COPY docker/entrypoint.sh /entrypoint.sh
COPY conf/gunicorn.conf /gunicorn.conf

EXPOSE 8000

CMD ["gunicorn", "--config", "/gunicorn.conf", "ya_test.wsgi:application"]
