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

