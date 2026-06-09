"""Quick validation for one prepared portfolio."""
import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
required = ["site/index.html", "site/styles.css", "site/script.js", ".github/workflows/deploy-pages.yml", "README.md"]
missing = [item for item in required if not (path / item).exists()]
public = (path / "site/index.html").read_text(encoding="utf-8") if (path / "site/index.html").exists() else ""
forbidden = [p for p in [r"\bReplace with\b", r"\bplaceholder\b", r"\bTODO\b", r"\bAI\b", r"ChatGPT", r"will be added later", r"insert here", r"pending replacement"] if re.search(p, public)]
if missing or forbidden:
    print({"missing": missing, "forbidden": forbidden})
    raise SystemExit(1)
print("Portfolio validation passed.")
