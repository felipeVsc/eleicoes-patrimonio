#!/usr/bin/env bash
# Prepares Superset's metadata on every start (idempotent) and starts the web server.
set -e

superset db upgrade
superset fab create-admin \
    --username "${ADMIN_USERNAME:-admin}" \
    --password "${ADMIN_PASSWORD:-admin}" \
    --firstname Admin --lastname Superset --email admin@localhost || true
superset init

# Registers the project's DuckDB file (read-only) as the "eleicoes" database
superset set-database-uri \
    --database_name eleicoes \
    --uri "duckdb:////data/eleicoes.duckdb?access_mode=read_only"

exec /usr/bin/run-server.sh
