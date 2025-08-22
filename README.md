# MakerWorks V2

Dockerized monorepo containing a FastAPI backend and a React/Vite frontend.

## Getting Started

1. Copy `makerworks/infra/.env.example` to `makerworks/infra/.env` and adjust values as needed.
2. Start the development stack:
   ```bash
   make docker-up
   ```
   Backend runs at [http://localhost:8000](http://localhost:8000) and frontend at [http://localhost:5173](http://localhost:5173).

## Migrations

Run database migrations with Alembic:

```bash
cd makerworks/backend
alembic upgrade head
```

## Testing

- Backend: `make backend-test`
- Frontend: `make frontend-test`

## Admin Seeding

Run `python makerworks/backend/app/seed.py` after the database is up to create a default admin user.

## Feature Flags

Feature flags are stored in the `feature_flags` table. Toggle `enabled` for each flag to enable or disable features.

## Auth

Available endpoints:

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/signin`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/signout` (requires `X-CSRF-Token` header matching the `csrf` cookie)
- `POST /api/v1/auth/totp/setup` and `/api/v1/auth/totp/verify` for 2FA

OAuth logins for Google, GitHub, and Apple are stubbed for now.

## Storefront

Available endpoints:

- `GET /api/v1/products`
- `GET /api/v1/products/{id}`
- `GET /api/v1/cart`
- `POST /api/v1/cart/items`
- `POST /api/v1/checkout/session`
- `POST /api/v1/checkout/webhook`

Stripe operates in test mode by default. Provide `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in your environment to enable real sessions.
Webhook requests must include the `Stripe-Signature` header and are verified against the webhook secret.

