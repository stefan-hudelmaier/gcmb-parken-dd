# From: https://depot.dev/docs/container-builds/how-to-guides/optimal-dockerfiles/python-uv-dockerfile

FROM python:3.12-slim-bookworm AS base
 
FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev
COPY *.py /app/
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev
 
FROM base
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app

CMD ["python", "main.py"]
