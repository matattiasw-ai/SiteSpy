"""Regenerate static portfolio assets using scripts/generate_collab_portfolios.py."""
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
subprocess.check_call(["python", str(root / "scripts" / "generate_collab_portfolios.py")], cwd=root)
