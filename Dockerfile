FROM python:3.8-alpine3.14

ENV FNET_ENV production

ADD . /app
WORKDIR /app

RUN apk add --update --no-cache build-base nginx curl supervisor mysql-client mariadb-connector-c-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

ENTRYPOINT ["sh", "/app/deploy/entrypoint.sh" ]