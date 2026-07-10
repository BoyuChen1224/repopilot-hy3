#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
API_DIR="$ROOT/apps/api"
WEB_DIR="$ROOT/apps/web"
VENV_DIR="$API_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
HOST_ADDRESS="${HOST_ADDRESS:-127.0.0.1}"
API_PORT="${API_PORT:-8000}"
WEB_PORT="${WEB_PORT:-5173}"

load_env() {
  file="$1"
  if [ ! -f "$file" ]; then
    return
  fi

  while IFS= read -r line || [ -n "$line" ]; do
    line=$(printf '%s' "$line" | tr -d '\r')

    case "$line" in
      ""|\#*) continue ;;
      export\ *) line=${line#export } ;;
    esac

    case "$line" in
      *=*) ;;
      *) continue ;;
    esac

    name=${line%%=*}
    value=${line#*=}
    name=$(printf '%s' "$name" | tr -d '[:space:]')

    case "$value" in
      \"*\") value=${value#\"}; value=${value%\"} ;;
      \'*\') value=${value#\'}; value=${value%\'} ;;
    esac

    case "$name" in
      HY3_API_KEY)
        if [ "${HY3_API_KEY:-}" = "" ]; then
          export HY3_API_KEY="$value"
        fi
        ;;
      HY3_BASE_URL)
        if [ "${HY3_BASE_URL:-}" = "" ]; then
          export HY3_BASE_URL="$value"
        fi
        ;;
      HY3_MODEL)
        if [ "${HY3_MODEL:-}" = "" ]; then
          export HY3_MODEL="$value"
        fi
        ;;
      VITE_API_BASE_URL)
        if [ "${VITE_API_BASE_URL:-}" = "" ]; then
          export VITE_API_BASE_URL="$value"
        fi
        ;;
    esac
  done < "$file"
}

find_python() {
  if command -v python3 >/dev/null 2>&1; then
    printf '%s\n' python3
  elif command -v python >/dev/null 2>&1; then
    printf '%s\n' python
  else
    printf '%s\n' ""
  fi
}

find_package_manager() {
  if [ -f "$WEB_DIR/pnpm-lock.yaml" ] && command -v pnpm >/dev/null 2>&1; then
    printf '%s\n' pnpm
  elif command -v npm >/dev/null 2>&1; then
    printf '%s\n' npm
  elif command -v pnpm >/dev/null 2>&1; then
    printf '%s\n' pnpm
  else
    printf '%s\n' ""
  fi
}

load_env "$API_DIR/.env"
load_env "$ROOT/.env"

if [ "${HY3_API_KEY:-}" = "" ] || [ "${HY3_API_KEY:-}" = "replace_with_your_hy3_api_key" ]; then
  echo "HY3_API_KEY is not configured. Copy .env.example to .env or apps/api/.env, then set your Hy3 API key." >&2
  exit 1
fi

PYTHON_CMD=$(find_python)
if [ "$PYTHON_CMD" = "" ]; then
  echo "Python was not found. Install Python 3.10+ and retry." >&2
  exit 1
fi

if [ ! -x "$VENV_PYTHON" ]; then
  echo
  echo "==> Creating backend virtual environment"
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

echo
echo "==> Installing backend dependencies"
"$VENV_PYTHON" -m pip install -r "$API_DIR/requirements.txt"

PM_CMD=$(find_package_manager)
if [ "$PM_CMD" = "" ]; then
  echo "Node.js package manager was not found. Install Node.js 18+ with npm, or install pnpm." >&2
  exit 1
fi

echo
echo "==> Installing frontend dependencies"
(cd "$WEB_DIR" && "$PM_CMD" install)

export VITE_API_BASE_URL="http://$HOST_ADDRESS:$API_PORT"

cleanup() {
  if [ "${API_PID:-}" != "" ]; then
    kill "$API_PID" 2>/dev/null || true
  fi
  if [ "${WEB_PID:-}" != "" ]; then
    kill "$WEB_PID" 2>/dev/null || true
  fi
}
trap cleanup INT TERM EXIT

echo
echo "Starting RepoPilot Hy3..."
echo "API: http://$HOST_ADDRESS:$API_PORT"
echo "Web: http://$HOST_ADDRESS:$WEB_PORT"
echo "Press Ctrl+C to stop both services."
echo

(cd "$API_DIR" && "$VENV_PYTHON" -m uvicorn app.main:app --host "$HOST_ADDRESS" --port "$API_PORT") &
API_PID=$!

(cd "$WEB_DIR" && "$PM_CMD" run dev -- --host "$HOST_ADDRESS" --port "$WEB_PORT") &
WEB_PID=$!

wait "$API_PID" "$WEB_PID"
