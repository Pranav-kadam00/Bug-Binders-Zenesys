# AQURA — Procurement Intelligence That Sees Ahead

> **AQURA does not just tell you which vendor is best.  
> It predicts the potential outcome, risk, and true cost of choosing each vendor  
> before the purchase decision is made.**

---

## Overview

AQURA is a full-stack procurement intelligence platform built with:

| Layer | Technology |
|---|---|
| Frontend | React 19 · TypeScript · Vite · Tailwind CSS v4 · TanStack Query · Wouter |
| Backend | Python 3.13 · FastAPI · Pydantic v2 · SQLAlchemy (optional) |
| Database | Supabase PostgreSQL (optional — in-memory demo data works out of the box) |
| Auth | JWT (HS256) · bcrypt password hashing |
| Package manager | pnpm workspaces |

### Main workflow

```
Purchase Request → Approval → Vendor Discovery → Vendor Comparison
  → AQURA Decision Twin™ → Vendor Selection → Purchase Order
  → Order Tracking → Vendor Performance Analysis
```

### AQURA Decision Twin™

The signature feature.  For each vendor it calculates:

```
True Purchase Cost =
    Quoted Price
  + Predicted Delay Cost      (delay probability × business impact)
  + Reliability Risk Cost     (1 - reliability% × order value)
  + Quality Risk Cost
```

A cheaper quote does not always produce a lower True Purchase Cost.

---

## Project structure

```
Bug-Binders-Zenesys/
├── artifacts/
│   ├── aqura/            ← React frontend (Vite)
│   │   ├── src/
│   │   │   ├── App.tsx   ← all pages + routes in one file
│   │   │   └── ...
│   │   ├── vite.config.ts
│   │   ├── .env.example
│   │   └── Dockerfile
│   └── api-server/       ← legacy Node stub (superseded by backend/)
│
├── backend/              ← FastAPI backend (Python)
│   ├── app/
│   │   └── main.py       ← complete API
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── lib/
│   ├── api-client-react/ ← generated TanStack Query hooks + typed fetcher
│   ├── api-spec/         ← OpenAPI spec (source of truth)
│   └── db/               ← Drizzle ORM schema (for future Node backend)
│
├── docker-compose.yml
├── README.md
└── pnpm-workspace.yaml
```

---

## Prerequisites

| Tool | Minimum version |
|---|---|
| Node.js | 20 LTS |
| pnpm | 9+ (`npm i -g pnpm`) |
| Python | 3.11+ |
| (Optional) Docker | 24+ |

A Supabase account is **not required** to run the application.  
When `DATABASE_URL` is left blank the backend serves realistic in-memory demo data.

---

## Backend setup

### 1. Create a virtual environment

```bash
cd backend
python -m venv venv
```

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Open `backend/.env` and set at minimum:

```env
JWT_SECRET=<strong-random-string>
# Optional — leave blank to use in-memory demo data:
DATABASE_URL=
```

To generate a secure `JWT_SECRET`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the backend

```bash
# From the backend/ directory:
uvicorn app.main:app --reload

# Or from the repo root:
uvicorn backend.app.main:app --reload
```

The backend starts on **http://localhost:8000**.

| URL | Description |
|---|---|
| http://localhost:8000/api/healthz | Health check |
| http://localhost:8000/api/docs | Swagger UI |
| http://localhost:8000/api/redoc | ReDoc |

---

## Frontend setup

### 1. Install dependencies

```bash
# From the repo root (installs all workspace packages):
pnpm install
```

### 2. Configure environment

```bash
cp artifacts/aqura/.env.example artifacts/aqura/.env
```

The default `artifacts/aqura/.env` already points at `http://localhost:8000`.  
The Vite dev server proxies `/api/*` to the backend automatically — no CORS
issue during local development.

### 3. Run the frontend

```bash
cd artifacts/aqura
pnpm run dev
```

The frontend starts on **http://localhost:5173**.

### 4. Build for production

```bash
cd artifacts/aqura
pnpm run build
```

Output lands in `artifacts/aqura/dist/public/`.

---

## Demo credentials

The backend ships with four pre-seeded users (all share the same password):

| Email | Password | Role |
|---|---|---|
| `maya@aqura.demo` | `password123` | Procurement Manager |
| `aarav@aqura.demo` | `password123` | Employee / Requester |
| `kavita@aqura.demo` | `password123` | Approver |
| `admin@aqura.demo` | `password123` | Admin |

> The login form in the current UI redirects directly to the dashboard.
> To exercise the JWT flow, `POST /api/v1/auth/login` with
> `username=<email>&password=<password>` (standard OAuth2 form encoding).

---

## API reference

All endpoints are documented in Swagger at `http://localhost:8000/api/docs`.

### Auth

| Method | Path | Auth required |
|---|---|---|
| POST | `/api/v1/auth/register` | No |
| POST | `/api/v1/auth/login` | No |
| GET | `/api/v1/auth/me` | Yes |

### Core procurement

| Method | Path | Auth required |
|---|---|---|
| GET | `/api/v1/dashboard` | Soft |
| GET / POST | `/api/v1/purchase-requests` | Soft / Yes |
| GET / PUT / DELETE | `/api/v1/purchase-requests/{id}` | Soft / Yes |
| GET | `/api/v1/approvals` | Soft |
| POST | `/api/v1/approvals/{id}/approve` | Yes |
| POST | `/api/v1/approvals/{id}/reject` | Yes |
| POST | `/api/v1/approvals/{id}/request-changes` | Yes |

### Vendors

| Method | Path | Auth required |
|---|---|---|
| GET | `/api/v1/vendors/discover` | Soft |
| GET / POST | `/api/v1/vendors` | Soft / Yes |
| GET / PUT | `/api/v1/vendors/{id}` | Soft / Yes |
| GET | `/api/v1/vendor-comparisons/{purchaseRequestId}` | Soft |

### Intelligence

| Method | Path | Auth required |
|---|---|---|
| GET | `/api/v1/decision-twin/{purchaseRequestId}` | Soft |
| POST | `/api/v1/decision-twin/analyze/{purchaseRequestId}` | Yes |

### Orders & tracking

| Method | Path | Auth required |
|---|---|---|
| GET / POST | `/api/v1/purchase-orders` | Soft / Yes |
| GET / PUT | `/api/v1/purchase-orders/{id}` | Soft / Yes |
| GET | `/api/v1/order-tracking` | Soft |
| POST | `/api/v1/order-tracking/{purchase_order_id}` | Yes |

### Analytics & notifications

| Method | Path | Auth required |
|---|---|---|
| GET | `/api/v1/vendor-performance` | Soft |
| GET | `/api/v1/vendor-performance/{vendor_id}` | Soft |
| GET | `/api/v1/analytics` | Soft |
| GET | `/api/v1/notifications` | Soft |
| POST | `/api/v1/notifications/{id}/read` | Yes |
| POST | `/api/v1/notifications/read-all` | Yes |

### AI assistant

| Method | Path | Auth required |
|---|---|---|
| POST | `/api/v1/ai/chat` | Soft |
| GET | `/api/v1/ai/conversations` | Yes |

> **Soft auth** — endpoint works without a token but may return personalized
> data when one is present.

---

## Supabase PostgreSQL (optional)

1. Create a project at [supabase.com](https://supabase.com).
2. Go to **Settings → Database → Connection string → URI**.
3. Copy the connection string and paste it into `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
```

4. Restart the backend.

> The current backend uses in-memory storage.  SQLAlchemy is installed and
> ready — connecting it to the Pydantic models is the next migration step.
> See `lib/db/src/schema/index.ts` for the Drizzle schema scaffold.

---

## Running with Docker

```bash
# Copy and configure env files first
cp backend/.env.example backend/.env
cp artifacts/aqura/.env.example artifacts/aqura/.env

# Edit backend/.env — set JWT_SECRET at minimum

docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger | http://localhost:8000/api/docs |

To stop:

```bash
docker compose down
```

---

## Environment variable reference

### `backend/.env`

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | Environment name |
| `DEBUG` | `true` | Enable debug output |
| `DATABASE_URL` | _(blank)_ | Supabase PostgreSQL connection URI |
| `JWT_SECRET` | _(must set)_ | Secret used to sign JWTs |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token lifetime |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Comma-separated allowed origins |
| `AI_PROVIDER` | `mock` | `mock` or `openai` |
| `AI_API_KEY` | _(blank)_ | AI provider API key |
| `MAP_PROVIDER` | `mock` | `mock` or `mappls` |
| `MAP_API_KEY` | _(blank)_ | Maps provider API key |
| `EMAIL_PROVIDER` | `mock` | Email provider |

### `artifacts/aqura/.env`

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend base URL exposed to the browser |

---

## Known limitations

| Area | Status |
|---|---|
| Real database persistence | Backend uses in-memory data; SQLAlchemy + Supabase wiring is ready to plug in |
| Frontend auth flow | UI navigates to dashboard directly; JWT is not yet sent on every API call (connect via `setAuthTokenGetter` in `custom-fetch.ts`) |
| Real AI provider | `AI_PROVIDER=mock` — swap in OpenAI/Gemini behind the `AIProvider` abstraction |
| Real maps / vendor discovery | `MAP_PROVIDER=mock` — plug in Mappls or Google Maps behind `MapProvider` |
| Email notifications | `EMAIL_PROVIDER=mock` — no emails are sent |
| Role enforcement UI | Backend RBAC is enforced; frontend hides controls based on role but does not yet read the JWT role claim |

---

## Contributing

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Make changes and verify both services start.
4. Open a pull request.

---

*AQURA — Procurement intelligence for consequential work.*
