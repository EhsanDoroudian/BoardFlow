#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p "$HOME/.local/share/boardflow"

wait_for_session() {
  local i
  for i in $(seq 1 60); do
    if [ -z "${XDG_RUNTIME_DIR:-}" ]; then
      export XDG_RUNTIME_DIR="/run/user/$(id -u)"
    fi

    if [ -n "${WAYLAND_DISPLAY:-}" ] && [ -S "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY}" ]; then
      return 0
    fi

    if [ -S "${XDG_RUNTIME_DIR}/wayland-1" ]; then
      export WAYLAND_DISPLAY=wayland-1
      return 0
    fi

    if [ -S "${XDG_RUNTIME_DIR}/wayland-0" ]; then
      export WAYLAND_DISPLAY=wayland-0
      return 0
    fi

    if [ -n "${DISPLAY:-}" ]; then
      return 0
    fi

    sleep 1
  done
}

wait_for_session
sleep 2

if [[ -x "$ROOT/venv/bin/python" ]]; then
  PYTHON="$ROOT/venv/bin/python"
else
  PYTHON="python3"
fi

exec "$PYTHON" -m app.main "$@"
