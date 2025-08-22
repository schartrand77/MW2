#!/usr/bin/env bash
set -euo pipefail
URL=${POSTGRES_URL:-postgresql://makerworks:makerworks@postgres:5432/makerworks}
URL_NO_DRIVER=${URL/psycopg/}
psql "$URL_NO_DRIVER" < backup.sql
echo "Database restored from backup.sql"
