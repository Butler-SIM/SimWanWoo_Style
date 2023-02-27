FROM python:3.9-alpine3.16

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# This is for cryptography<3.5
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN apk update

RUN apk add --no-cache mariadb-connector-c-dev

RUN apk add --virtual .tmp-build-deps \
    gcc python3-dev musl-dev libffi-dev libressl-dev openssl-dev cargo \
    jpeg-dev zlib-dev libjpeg mysql-dev libxml2-dev libxslt-dev \
    && pip install -r /app/requirements.txt \
    && apk del .tmp-build-deps

COPY . /app

RUN adduser -D user
USER user

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

