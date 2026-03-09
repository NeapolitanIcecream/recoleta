# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:0.10.6 AS uv


FROM python:3.14-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    RECOLETA_DB_PATH=/data/recoleta.db \
    MARKDOWN_OUTPUT_DIR=/data/outputs \
    ARTIFACTS_DIR=/data/artifacts \
    RAG_LANCEDB_DIR=/data/lancedb \
    RECOLETA_CONFIG_PATH=/config/recoleta.yaml

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "${VIRTUAL_ENV}"

WORKDIR /app


FROM base AS builder

COPY --from=uv /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project --no-editable

COPY recoleta ./recoleta
COPY recoleta.example.yaml ./recoleta.example.yaml

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable


FROM base AS runtime

COPY --from=builder /opt/venv /opt/venv
COPY recoleta.example.yaml /app/recoleta.example.yaml

RUN mkdir -p /data/outputs /data/artifacts /data/lancedb /config

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD ["recoleta", "doctor", "--healthcheck"]

ENTRYPOINT ["recoleta"]
CMD ["run"]


FROM runtime AS runtime-full

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        pandoc \
    && rm -rf /var/lib/apt/lists/* \
    && python -m playwright install --with-deps chromium
