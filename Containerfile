FROM alpine:3.24 AS builder

ENV UV_NO_DEV=1 \
    UV_NO_CACHE=1 \
    UV_LOCKED=0 \
    UV_NO_EDITABLE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_INSTALL_DIR=/python

RUN apk add --no-cache build-base python3

COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /usr/bin/

# Install the project dependencies
WORKDIR /app
COPY pyproject.toml /app/
RUN uv sync --no-install-project

# Install the project itself
COPY . /app/
RUN uv sync


FROM alpine:3.24

RUN apk add --no-cache ffmpeg deno

COPY --from=builder /python /python
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/static /app/static

WORKDIR /app

RUN ln -s /app/.venv/bin/cli-to-yaml /usr/bin/cli-to-yaml
RUN ln -s /app/.venv/bin/serve /usr/bin/serve

CMD ["serve"]
