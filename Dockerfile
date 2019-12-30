FROM python:3.7-alpine

WORKDIR /tesouro-direto
ENV PYTHONPATH "/tesouro-direto"

COPY database /tesouro-direto/database
COPY network /tesouro-direto/network
COPY parsers /tesouro-direto/parsers
COPY spiders /tesouro-direto/spiders
COPY static_data /tesouro-direto/static_data
COPY main.py /tesouro-direto

RUN apk add --no-cache postgresql-dev libpq gcc python3-dev musl-dev && \
    pip install --no-cache-dir psycopg2 psycopg2-binary
