FROM python:3.12-slim

RUN pip install --no-cache-dir dbt-core==1.12.6 dbt-duckdb==1.11.0

WORKDIR /usr/app

ENTRYPOINT ["dbt"]