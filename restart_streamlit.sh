#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8053}"
APP_FILE="streamlit_app.py"
PID_FILE="streamlit.pid"
LOG_FILE="streamlit.log"

if [[ -x "/workspaces/CompuStats/.venv_fresh/bin/python" ]]; then
  PYTHON_BIN="/workspaces/CompuStats/.venv_fresh/bin/python"
elif [[ -x "/workspaces/CompuStats/venv/bin/python" ]]; then
  PYTHON_BIN="/workspaces/CompuStats/venv/bin/python"
else
  PYTHON_BIN="python3"
fi

cd "/workspaces/CompuStats"

if [[ -f "$PID_FILE" ]]; then
  OLD_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "${OLD_PID}" ]] && ps -p "$OLD_PID" >/dev/null 2>&1; then
    kill "$OLD_PID" || true
    sleep 1
  fi
fi

pkill -f "streamlit run ${APP_FILE} --server.port ${PORT}" >/dev/null 2>&1 || true

nohup "$PYTHON_BIN" -m streamlit run "$APP_FILE" --server.port "$PORT" --server.address 0.0.0.0 > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

sleep 2

if ps -p "$NEW_PID" >/dev/null 2>&1; then
  echo "Streamlit restarted successfully"
  echo "PID: $NEW_PID"
  echo "Port: $PORT"
  echo "URL: http://localhost:$PORT"
else
  echo "Failed to start Streamlit. Check $LOG_FILE for details." >&2
  exit 1
fi