#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8501}"
URL="http://localhost:${PORT}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${SCRIPT_DIR}/restart_streamlit.sh" "${PORT}"

echo "Opening: ${URL}"

if [[ -n "${BROWSER:-}" ]]; then
  "${BROWSER}" "${URL}" >/dev/null 2>&1 || true
else
  echo "BROWSER is not set. Open this URL manually: ${URL}"
fi
