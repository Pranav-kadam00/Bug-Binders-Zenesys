# ── AQURA Frontend — Dockerfile ───────────────────────────────────────────────
FROM node:22-alpine AS builder

# pnpm is the workspace package manager
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /workspace

# Copy workspace manifests first for layer caching
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml tsconfig.json tsconfig.base.json ./
COPY lib/ ./lib/
COPY artifacts/aqura/ ./artifacts/aqura/

# Install all workspace dependencies
RUN pnpm install --frozen-lockfile

# Build the frontend
WORKDIR /workspace/artifacts/aqura
RUN pnpm run build

# ── Serve with a lightweight static server ───────────────────────────────────
FROM node:22-alpine AS runner

WORKDIR /app
COPY --from=builder /workspace/artifacts/aqura/dist/public ./public
COPY --from=builder /workspace/artifacts/aqura/node_modules/.bin/vite /usr/local/bin/vite || true

# Use a simple serve package for the static files
RUN npm install -g serve@14

EXPOSE 4173

CMD ["serve", "-s", "public", "-l", "4173"]
