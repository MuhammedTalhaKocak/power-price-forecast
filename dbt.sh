#!/usr/bin/env bash
cd "$(dirname "$0")"

MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd)":/usr/app \
  -w /usr/app/power_price \
  -e DBT_PROFILES_DIR=/usr/app/power_price \
  dbt-duckdb "$@"