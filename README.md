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

## Amazon Affiliate

Enable the `amazon_affiliate` feature flag and set `AMAZON_ASSOCIATE_TAG` to activate the Amazon search endpoint:

- `GET /api/v1/amazon/search?q=`

Results are cached in Redis and include your affiliate tag.

## Inventory

Available endpoints:

- `GET /api/v1/inventory/levels`
- `PATCH /api/v1/inventory/levels`
- `GET /api/v1/inventory/moves`
- `POST /api/v1/inventory/moves`
- `GET /api/v1/user/inventory`
- `POST /api/v1/user/inventory`
- `DELETE /api/v1/user/inventory/{id}`

Use the `/scan` page in the frontend to scan barcodes and post inventory moves by SKU.

## Printing Integrations

Available endpoints:

- `POST /api/v1/printing/{provider}/jobs`
- `GET /api/v1/printing/{provider}/jobs/{id}`
- `POST /api/v1/printing/{provider}/webhook`

Supported providers: `bambu` and `octoprint`. Set `BAMBU_CONNECT_API_KEY`,
`OCTOPRINT_BASE_URL`, and `OCTOPRINT_API_KEY` in your environment to enable.

## Models

Upload STL or 3MF files and generate thumbnails:

- `GET /api/v1/models`
- `POST /api/v1/models` (multipart file field `file`)
- `GET /api/v1/models/{id}`
- `GET /api/v1/models/{id}/file`
- `POST /api/v1/models/{id}/color` to set a hex color and re-render the thumbnail
- `POST /api/v1/models/{id}/rethumb` to regenerate the thumbnail

