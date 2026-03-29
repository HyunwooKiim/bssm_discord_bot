#!/usr/bin/env bash
set -euo pipefail

# Toggle script to start/stop the Discord bot
# Usage: ./toggle_bot.sh

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="bot.pid"
LOG_FILE="bot.log"
PYTHON="python3"

# Load environment variables from .env if present
if [ -f .env ]; then
  set -o allexport
  # shellcheck disable=SC1091
  source .env
  set +o allexport
fi

# If pid file exists and process is running -> stop
if [ -f "$PID_FILE" ]; then
  pid=$(cat "$PID_FILE" 2>/dev/null || true)
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    echo "Stopping bot (pid $pid)..."
    kill "$pid" 2>/dev/null || true
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
      echo "Process did not exit, sending SIGKILL..."
      kill -9 "$pid" 2>/dev/null || true
      sleep 1
    fi
    rm -f "$PID_FILE"
    echo "Stopped."
    exit 0
  else
    echo "Stale or empty pid file found, removing."
    rm -f "$PID_FILE"
  fi
fi

# Start the bot
echo "Starting bot..."
# Ensure certifi is available (non-fatal)
$PYTHON -m pip install --user certifi >/dev/null 2>&1 || true
CERT_FILE=$($PYTHON - <<PY
try:
    import certifi
    print(certifi.where())
except Exception:
    pass
PY
)
if [ -n "$CERT_FILE" ]; then
  export SSL_CERT_FILE="$CERT_FILE"
fi

nohup $PYTHON bot.py >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
sleep 0.5
if [ -f "$PID_FILE" ]; then
  echo "Started, pid $(cat $PID_FILE). Logs: $LOG_FILE"
else
  echo "Failed to start bot; check $LOG_FILE"
fi
