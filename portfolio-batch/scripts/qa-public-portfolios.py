import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"
EXPECTED_ACTIVE_COUNT = 17

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


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.ids = set()
        self.classes = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "img" and values.get("src"):
            self.images.append(values["src"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if values.get("id"):
            self.ids.add(values["id"])
        if values.get("class"):
            self.classes.extend(values["class"].split())


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


def public_screenshots(site):
    screenshot_dir = site / "assets" / "screenshots"
    if not screenshot_dir.exists():
        return []
    files = []
    for file in screenshot_dir.iterdir():
        if file.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        lowered = file.name.lower()
        if "asset" in lowered or "evidence" in lowered:
            continue
        files.append(file)
    return files


def is_local_reference(href):
    lowered = href.lower()
    return not (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )


def main():
    failures = []
    items = active_items()

    if len(items) != EXPECTED_ACTIVE_COUNT:
        failures.append(f"Expected {EXPECTED_ACTIVE_COUNT} active portfolios, found {len(items)}")

    for item in items:
        portfolio = Path(item["portfolioPath"])
        site = portfolio / "site"
        index = site / "index.html"
        if not index.exists():
            failures.append(f"{item['studentName']}: missing site/index.html")
            continue

        html = index.read_text(encoding="utf-8", errors="ignore")
        lowered = html.lower()
        for term in FORBIDDEN_TERMS:
            if term in lowered:
                failures.append(f"{index}: forbidden public term found: {term}")

        parser = LinkParser()
        parser.feed(html)

        for src in parser.images:
            if is_local_reference(src) and not (site / src).resolve().exists():
                failures.append(f"{index}: broken local image reference: {src}")

        for href in parser.links:
            if href.endswith(".pdf") and is_local_reference(href) and not (site / href).resolve().exists():
                failures.append(f"{index}: missing linked PDF: {href}")

        screenshots = public_screenshots(site)
        has_public_screen_section = "screens" in parser.ids or "screenshots" in parser.classes or "screen-grid" in parser.classes
        if not screenshots and has_public_screen_section:
            failures.append(f"{index}: public screenshot section is visible without real screenshots")

        for public_file in [site / "script.js", site / "styles.css", *sorted(site.glob("*.json"))]:
            if not public_file.exists():
                continue
            content = public_file.read_text(encoding="utf-8", errors="ignore").lower()
            for term in FORBIDDEN_TERMS:
                if term in content:
                    failures.append(f"{public_file}: forbidden public term found: {term}")

    for failure in failures:
        print(failure)

    if failures:
        print(f"Public portfolio QA failed with {len(failures)} issue(s).")
        return 1

    print(f"Public portfolio QA passed for {len(items)} active portfolios.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
