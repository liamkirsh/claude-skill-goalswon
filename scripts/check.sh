#!/usr/bin/env bash
set -euo pipefail

command -v goalswon >/dev/null 2>&1 || {
  echo "goalswon CLI not installed. Run: npm install -g @goalswon/cli" >&2
  exit 127
}

goalswon auth status --json >/dev/null 2>&1 || {
  echo "Not authenticated. Run: goalswon auth login <YOUR_API_KEY>" >&2
  echo "Get your key at: app.goalswon.com > Settings > API Access" >&2
  exit 1
}

echo "ok"
