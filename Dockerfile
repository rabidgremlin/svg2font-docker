FROM ghcr.io/astral-sh/uv:0.9 AS uv

FROM debian:trixie-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv python3-fontforge ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /build
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT=/opt/venv UV_PYTHON_DOWNLOADS=never
RUN uv venv --system-site-packages --python /usr/bin/python3 /opt/venv && uv sync --locked --no-install-project --no-dev

FROM debian:trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-fontforge && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/venv /opt/venv
COPY main.py /app/main.py
WORKDIR /data
ENTRYPOINT ["/opt/venv/bin/python", "/app/main.py"]
