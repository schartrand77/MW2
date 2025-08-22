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

Populate demo data after the stack is running:

```bash
make seed
```

This creates a sample API key and theme for the `demo` organization.

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

### Plugins & Edge Caching

Specify server plugins via the comma-separated `PLUGINS` environment variable. Each module should expose a
`setup(app)` function that receives the FastAPI instance. The frontend can load ES modules listed in `VITE_PLUGINS` and
call their optional `setup()` hook.

Responses now include `Cache-Control` and `ETag` headers by default, enabling Cloudflare-friendly caching with
`stale-while-revalidate` semantics.

### Security & Monitoring

Cross-origin requests are handled via permissive CORS settings for development and responses include a
`Content-Security-Policy` header. If `SENTRY_DSN`/`VITE_SENTRY_DSN` are set, backend and frontend errors are reported to
Sentry. React components are wrapped in an error boundary and common screens show loading skeletons and empty-state
placeholders.

### Offline Mode & Background Sync

The frontend registers a service worker that precaches assets and caches API GET requests. Failed API mutations are
queued and retried when connectivity is restored using Background Sync.

### Import/Export & Bulk Operations

API keys can be exported or imported in CSV or JSON form via `/api/v1/apikeys/export` and `/api/v1/apikeys/import`. The
import endpoint supports a `dry_run=true` flag for validation without persistence. Delete multiple keys at once with
`POST /api/v1/apikeys/bulk-delete`.

### Command Palette & Themes

Press `Cmd+K` (`Ctrl+K` on Windows/Linux) to open the global command palette for quick navigation. Brand colors are
loaded from `/api/v1/themes/{org}` and can be customized on the `/theme` page; edited tokens apply instantly across the
app.

## Documentation

Additional guides live in the `docs/` directory:

- `docs/api.md` – API usage and generated clients.
- `docs/plugins.md` – authoring server and client plugins.
- `docs/integrations.md` – configuring external services.

