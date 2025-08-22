# MakerWorks API

The backend exposes a REST API and a matching GraphQL endpoint. An OpenAPI
specification is generated via `make openapi` and stored in `makerworks/shared/openapi.json`.
A TypeScript client is produced alongside at `makerworks/shared/client.ts`.

## Usage

- `GET /api/v1/system/ping` – health check.
- `POST /api/v1/auth/signup` – create account.

Use the generated client in frontend or external tools:

```ts
import { paths } from '../shared/client';
```

See `docs/thunder-tests` for example requests.
