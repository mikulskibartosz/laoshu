# ----------- Builder for frontend (Next.js) -----------
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ----------- Final image -----------
FROM python:3.10-slim

# Install Node.js for Next.js runtime
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies directly in final image
COPY cli/pyproject.toml cli/poetry.lock ./cli/
WORKDIR /app/cli
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main
WORKDIR /app

# Copy CLI code
COPY cli/ ./cli/

# Copy frontend build and node_modules
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY --from=frontend-builder /app/frontend/package.json ./frontend/package.json
COPY --from=frontend-builder /app/frontend/package-lock.json ./frontend/package-lock.json
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules
COPY --from=frontend-builder /app/frontend/next.config.js ./frontend/next.config.js
COPY --from=frontend-builder /app/frontend/next-sitemap.config.js ./frontend/next-sitemap.config.js
COPY --from=frontend-builder /app/frontend/tailwind.config.js ./frontend/tailwind.config.js
COPY --from=frontend-builder /app/frontend/postcss.config.js ./frontend/postcss.config.js
COPY --from=frontend-builder /app/frontend/tsconfig.json ./frontend/tsconfig.json
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports
EXPOSE 3000 8000

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]