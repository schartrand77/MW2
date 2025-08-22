# MakerWorks V2

Dockerized monorepo containing a FastAPI backend and a React/Vite frontend.

## Getting Started

1. Copy `makerworks/infra/.env.example` to `makerworks/infra/.env` and adjust values as needed. The sample file includes
   placeholders for Postgres, Redis, OAuth providers, Stripe, storage backends and other integrations. Stub values are
   provided so the stack can boot without real secrets.
2. Start the development stack:
   ```bash
   make docker-up
   ```
   Backend runs at [http://localhost:8000](http://localhost:8000) and frontend at [http://localhost:5173](http://localhost:5173). A GraphQL endpoint is available at `/graphql`.

## Testing

- Backend: `make backend-test`
- Frontend: `make frontend-test`

## Admin Seeding

Run `python makerworks/backend/app/seed.py` after the database is up to create a default admin user.

## Feature Flags

Feature flags are stored in the `feature_flags` table. Toggle `enabled` for each flag to enable or disable features.

### API Keys & Webhooks

Issue API keys via `POST /api/v1/apikeys` and supply them with the `X-API-Key` header. Create webhooks via `POST /api/v1/webhooks`; deliveries are HMAC signed.

### Rate Limiting

A simple per-IP rate limiter is provided and used on `/api/v1/system/limited` as an example.

### Notifications

Subscribe API keys to events using `/api/v1/notifications/subscriptions` and dispatch with
`/api/v1/notifications/trigger/{event}`. When `DISCORD_BOT_TOKEN` and `DISCORD_CHANNEL_ID` are
configured, `/api/v1/notifications/discord` returns the latest messages for the notification center.

### Analytics

Prometheus metrics are exposed at `/metrics` and scraped by the bundled Prometheus container. A Grafana instance is
available on [http://localhost:3001](http://localhost:3001) with a basic dashboard for HTTP request rates.

### Backups

Run `makerworks/infra/backup.sh` to dump the Postgres database to `backup.sql` and `makerworks/infra/restore.sh` to
restore from it.

### Compliance

Export or delete persisted data using `/api/v1/compliance/export` and `/api/v1/compliance/delete`. A basic GDPR
checklist is available at `/api/v1/compliance/checklist`.

