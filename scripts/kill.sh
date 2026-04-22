#!/usr/bin/env bash
set -euo pipefail

kill_by_port() {
  local port="$1"
  local name="$2"

  echo "[kill] checking port ${port} for ${name}..."
  
  local pids
  pids=$(lsof -ti tcp:$port 2>/dev/null || true)
  
  if [[ -n "$pids" ]]; then
    echo "[kill] stopping ${name} (PID: $pids) on port ${port}..."
    echo "$pids" | xargs kill -9 2>/dev/null || true
    sleep 2
    
    if lsof -ti tcp:$port >/dev/null 2>&1; then
      echo "[kill] force killing again..."
      lsof -ti tcp:$port | xargs kill -9 2>/dev/null || true
      sleep 1
    fi
  else
    echo "[kill] no process on port ${port}"
  fi
}

kill_by_port 8000 "backend"
kill_by_port 8080 "open-webui"

echo "[kill] done - ports should be free now"