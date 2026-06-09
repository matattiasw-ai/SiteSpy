#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:-portfolio-batch/deployment-config.local.json}"
WATCH_ARG="${2:-}"
[[ -f "$CONFIG_PATH" ]] || { echo "Config file not found: $CONFIG_PATH"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python - "$CONFIG_PATH" "$WATCH_ARG" "$SCRIPT_DIR" <<'PY'
import json
import shlex
import subprocess
import sys
from pathlib import Path

config = json.loads(Path(sys.argv[1]).read_text())
watch = sys.argv[2] == "--watch"
script = Path(sys.argv[3]) / "deploy-portfolio.sh"
for item in config:
    cmd = [
        str(script),
        "--portfolio-path", item["portfolioPath"],
        "--student-name", item["studentName"],
        "--github-username", item["githubUsername"],
        "--student-email", item["studentEmail"],
        "--repo-name", item["repoName"],
        "--token-env", item["tokenEnvironmentVariable"],
    ]
    if watch:
        cmd.append("--watch")
    print("Running:", " ".join(shlex.quote(part) for part in cmd))
    subprocess.check_call(cmd)
PY
