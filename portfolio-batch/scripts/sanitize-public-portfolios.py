import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"

FORBIDDEN_TERMS = [
    "use the guide",
    "prepare answers",
    "evidence to be added",
    "screenshots still required",
    "capture screenshots",
    "replace",
    "placeholder",
    "todo",
    "ai generated",
    "student should",
    "student must",
    "manual screenshot",
    "add screenshots",
    "local guide",
]


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def active_items():
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    items = []
    for item in data:
        name = clean(item.get("studentName"))
        username = clean(item.get("githubUsername"))
        if name.lower() in {"penny", "ndaitavela"}:
            continue
        if name.lower().startswith("nambuli") or username == "studentgithub":
            continue
        items.append(item)
    return items


def public_files(portfolio_path):
    site = Path(portfolio_path) / "site"
    files = [
        site / "index.html",
        site / "script.js",
        site / "styles.css",
    ]
    files.extend(sorted(site.glob("*.json")))
    return [file for file in files if file.exists()]


def main():
    failures = []
    processed = 0
    for item in active_items():
        processed += 1
        for file in public_files(item["portfolioPath"]):
            content = file.read_text(encoding="utf-8", errors="ignore").lower()
            for term in FORBIDDEN_TERMS:
                if term in content:
                    failures.append((file, term))

    for file, term in failures:
        print(f"{file}: forbidden public term found: {term}")

    if failures:
        print(f"Public portfolio sanitizer failed with {len(failures)} issue(s).")
        return 1

    print(f"Public portfolio sanitizer passed for {processed} active portfolios.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
