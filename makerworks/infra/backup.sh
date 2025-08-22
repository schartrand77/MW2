#!/usr/bin/env bash
set -euo pipefail
URL=${POSTGRES_URL:-postgresql://makerworks:makerworks@postgres:5432/makerworks}
URL_NO_DRIVER=${URL/psycopg/}
pg_dump "$URL_NO_DRIVER" > backup.sql
echo "Backup written to backup.sql"
