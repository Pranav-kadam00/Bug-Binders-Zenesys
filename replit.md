# AQURA Procurement Intelligence

AQURA is an enterprise procurement workspace that helps teams see the true cost and risk of every purchase decision.

## Run & Operate

- `pnpm --filter @workspace/aqura run dev` — run the React/Vite web app
- `pnpm --filter @workspace/api-server run dev` — run the Python/FastAPI API
- `pnpm run typecheck` — full TypeScript typecheck
- `pnpm --filter @workspace/api-spec run codegen` — regenerate typed client and validation schemas from the OpenAPI contract
- API docs: `/api/docs` and `/api/redoc`

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, Wouter, TanStack Query, Recharts, Lucide
- Backend: Python, FastAPI, Pydantic, SQLAlchemy-ready persistence boundary
- API contract: OpenAPI in `lib/api-spec/openapi.yaml`, generated clients in `lib/api-client-react` and `lib/api-zod`
- Workspace: pnpm monorepo

## Where things live

- `artifacts/aqura/` — deployable frontend application
- `backend/app/main.py` — FastAPI application and seeded procurement endpoints
- `lib/api-spec/openapi.yaml` — source-of-truth API contract
- `lib/api-client-react/` — generated React Query hooks
- `lib/db/` — shared database package for future PostgreSQL persistence

## Architecture decisions

- The browser consumes generated API hooks rather than embedding request logic in pages.
- The backend keeps the Decision Twin calculations deterministic and provider-independent for the initial demonstration.
- The API service is Python/FastAPI while remaining reachable through the workspace’s existing `/api` service route.
- Initial seeded data is intentionally realistic and small enough to keep the first workspace responsive.

## Product

The app includes a public product landing page, supporting auth screens, a procurement dashboard, request creation and details, approvals, vendor discovery and directory, vendor comparison, AQURA Decision Twin analysis, purchase orders, order tracking, vendor performance, analytics, notifications, settings, and a globally available assistant.

## Gotchas

- Regenerate the client after any OpenAPI change before changing frontend consumers.
- The API workflow runs from the repository root so it can import `backend.app.main`.
- Keep API keys and provider credentials server-side; the initial AI, map, and email behaviors are mock/provider-neutral.