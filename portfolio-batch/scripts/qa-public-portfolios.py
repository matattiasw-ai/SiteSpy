import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"
EXPECTED_ACTIVE_COUNT = 17
MIN_DISTINCT_LAYOUTS = 12

FORBIDDEN_TERMS = [
    "presentation prep",
    "use the guide",
    "prepare answers",
    "evidence to be added",
    "screenshots still required",
    "capture screenshots",
    "replace",
    "placeholder",
    "todo",
    "student should",
    "student must",
    "manual screenshot",
    "add screenshots",
    "local guide",
    "sample evidence",
]

FORBIDDEN_REGEX = [
    re.compile(r"\bAI\b"),
]

REQUIRED_PUBLIC_TEXT = [
    "Project Overview",
    "My Contribution",
    "Skills",
    "Challenge and Solution",
    "Learning Reflection",
]


class PublicParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.ids = set()
        self.classes = []
        self.body_layout = ""
        self.has_header = False
        self.has_footer = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "body":
            self.body_layout = values.get("data-layout", "")
        if tag == "header":
            self.has_header = True
        if tag == "footer":
            self.has_footer = True
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


def certificates(site):
    cert_dir = site / "assets" / "certificates"
    if not cert_dir.exists():
        return []
    return [
        file
        for file in cert_dir.iterdir()
        if file.is_file() and file.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
    ]


def is_local_reference(href):
    lowered = href.lower()
    return not (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )


def public_files(site):
    return [site / "index.html", site / "script.js", *sorted(site.glob("*.json"))]


def main():
    failures = []
    items = active_items()
    layouts = set()

    if len(items) != EXPECTED_ACTIVE_COUNT:
        failures.append(f"Expected {EXPECTED_ACTIVE_COUNT} active portfolios, found {len(items)}")

    for item in items:
        portfolio = Path(item["portfolioPath"])
        site = portfolio / "site"
        index = site / "index.html"
        css = site / "styles.css"
        cert_dir = site / "assets" / "certificates"

        if not index.exists():
            failures.append(f"{item['studentName']}: missing site/index.html")
            continue
        if not css.exists():
            failures.append(f"{item['studentName']}: missing site/styles.css")
        if not cert_dir.exists():
            failures.append(f"{item['studentName']}: missing site/assets/certificates")

        html = index.read_text(encoding="utf-8", errors="ignore")
        lowered = html.lower()
        parser = PublicParser()
        parser.feed(html)

        if not parser.body_layout:
            failures.append(f"{index}: missing body data-layout marker")
        else:
            layouts.add(parser.body_layout)

        if not parser.has_header:
            failures.append(f"{index}: missing non-empty header element")
        if not parser.has_footer:
            failures.append(f"{index}: missing footer element")

        for required in REQUIRED_PUBLIC_TEXT:
            if required.lower() not in lowered:
                failures.append(f"{index}: missing public section text: {required}")

        for term in FORBIDDEN_TERMS:
            if term in lowered:
                failures.append(f"{index}: forbidden public term found: {term}")
        for pattern in FORBIDDEN_REGEX:
            if pattern.search(html):
                failures.append(f"{index}: forbidden public term found: {pattern.pattern}")

        for src in parser.images:
            if is_local_reference(src) and not (site / src).resolve().exists():
                failures.append(f"{index}: broken local image reference: {src}")

        for href in parser.links:
            if href.endswith(".pdf") and is_local_reference(href) and not (site / href).resolve().exists():
                failures.append(f"{index}: missing linked PDF: {href}")

        screenshot_files = public_screenshots(site)
        has_evidence = (
            "work-record" in parser.ids
            or "evidence-section" in parser.classes
            or "evidence-grid" in parser.classes
        )
        if not screenshot_files and has_evidence:
            failures.append(f"{index}: public evidence section is visible without real screenshots")

        cert_files = certificates(site)
        has_certificate_section = "certificates" in parser.ids or "certificate-section" in parser.classes
        if not cert_files and has_certificate_section:
            failures.append(f"{index}: public certificate section is visible without certificate files")

        if css.exists():
            css_text = css.read_text(encoding="utf-8", errors="ignore").lower()
            if "@media" not in css_text or "760px" not in css_text:
                failures.append(f"{css}: missing mobile media query near 760px")

        for file in public_files(site):
            if not file.exists():
                continue
            content = file.read_text(encoding="utf-8", errors="ignore")
            lowered_content = content.lower()
            for term in FORBIDDEN_TERMS:
                if term in lowered_content:
                    failures.append(f"{file}: forbidden public term found: {term}")
            for pattern in FORBIDDEN_REGEX:
                if pattern.search(content):
                    failures.append(f"{file}: forbidden public term found: {pattern.pattern}")

    if len(layouts) < MIN_DISTINCT_LAYOUTS:
        failures.append(f"Expected at least {MIN_DISTINCT_LAYOUTS} distinct data-layout values, found {len(layouts)}")

    for failure in failures:
        print(failure)

    if failures:
        print(f"Public portfolio QA failed with {len(failures)} issue(s).")
        return 1

    print(f"Public portfolio QA passed for {len(items)} active portfolios.")
    print(f"Distinct layout families: {len(layouts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
