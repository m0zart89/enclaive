# FastApi App

- `GET /healthz` -> `200 {"SYS_ENV": "<value>"}`
- `GET /metrics` -> Prometheus metrics with counter `app_custom_events_total`
- `SYS_ENV` injected secret from Vault (`/vault/secrets/env`).

## Image

- Multi-stage
- minimal base (`python:3.12-alpine`), 
- Non-root `appuser` (uid 10001, guid 10001),
- HEALTHCHECK on `/healthz`.

## Build

```bash
./build.sh
```
Script builds image with tags `latest` and `GIT_SHA`
