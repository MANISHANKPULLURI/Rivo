#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
BACKEND_RELOAD="${BACKEND_RELOAD:-false}"
WEBUI_HOST="${WEBUI_HOST:-0.0.0.0}"
WEBUI_PORT="${WEBUI_PORT:-8080}"
WEBUI_DATA_DIR="${WEBUI_DATA_DIR:-$ROOT_DIR/.open-webui-data}"
OPENAI_PROXY_URL="${OPENAI_PROXY_URL:-http://localhost:${BACKEND_PORT}/v1}"
OPENAI_PROXY_KEY="${OPENAI_PROXY_KEY:-dummy}"
DEFAULT_MODEL="${DEFAULT_MODEL:-finance-agent}"

is_port_open() {
  local port="$1"
  lsof -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
}

ensure_backend() {
  if is_port_open "$BACKEND_PORT"; then
    echo "[start] detected existing backend on port ${BACKEND_PORT}; reusing it"
    BACKEND_STARTED_BY_SCRIPT=false
    return 0
  fi

  echo "[start] backend: http://${BACKEND_HOST}:${BACKEND_PORT}"
  BACKEND_ARGS=(--host "$BACKEND_HOST" --port "$BACKEND_PORT")
  if [[ "$BACKEND_RELOAD" == "true" ]]; then
    BACKEND_ARGS+=(--reload)
  fi
  uv run --project "$ROOT_DIR" python -m uvicorn backend.server:app "${BACKEND_ARGS[@]}" &
  BACKEND_PID=$!
  BACKEND_STARTED_BY_SCRIPT=true
}

ensure_webui_port_free() {
  if is_port_open "$WEBUI_PORT"; then
    echo "[start] port ${WEBUI_PORT} already in use. Stop existing Open WebUI or run with WEBUI_PORT=<free-port>."
    return 1
  fi
}

cleanup() {
  set +e
  if [[ "${BACKEND_STARTED_BY_SCRIPT:-false}" == "true" && -n "${BACKEND_PID:-}" ]]; then
    kill -TERM "${BACKEND_PID}" >/dev/null 2>&1 || true
    pkill -TERM -P "${BACKEND_PID}" >/dev/null 2>&1 || true
    wait "${BACKEND_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${WEBUI_PID:-}" ]]; then
    kill -TERM "${WEBUI_PID}" >/dev/null 2>&1 || true
    pkill -TERM -P "${WEBUI_PID}" >/dev/null 2>&1 || true
    wait "${WEBUI_PID}" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

wait_for_backend() {
  local retries=30
  local delay=1
  local url="${OPENAI_PROXY_URL}/models"

  echo "[start] waiting for backend readiness: ${url}"
  for ((i=1; i<=retries; i++)); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "[start] backend ready"
      return 0
    fi
    sleep "$delay"
  done

  echo "[start] backend did not become ready in time"
  return 1
}

echo "[start] syncing dependencies with uv"
uv sync --project "$ROOT_DIR"

mkdir -p "$WEBUI_DATA_DIR"

ensure_webui_port_free
ensure_backend

wait_for_backend

echo "[start] open-webui: http://${WEBUI_HOST}:${WEBUI_PORT}"
WEBUI_AUTH=False \
ENABLE_OLLAMA_API=False \
OLLAMA_BASE_URL="" \
ENABLE_OPENAI_API=True \
OPENAI_API_BASE_URL="$OPENAI_PROXY_URL" \
OPENAI_API_BASE_URLS="$OPENAI_PROXY_URL" \
OPENAI_API_KEY="$OPENAI_PROXY_KEY" \
OPENAI_API_KEYS="$OPENAI_PROXY_KEY" \
DEFAULT_MODELS="$DEFAULT_MODEL" \
DATA_DIR="$WEBUI_DATA_DIR" \
open-webui serve --host "$WEBUI_HOST" --port "$WEBUI_PORT" &
WEBUI_PID=$!

echo "[start] services are running (Ctrl+C to stop)"
wait "$BACKEND_PID" "$WEBUI_PID"
