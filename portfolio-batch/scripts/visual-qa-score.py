import json
import re
import struct
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"
VISUAL_QA_DIR = ROOT / "portfolio-batch" / "visual-qa"
REPORT_JSON = VISUAL_QA_DIR / "visual-qa-report.json"
REPORT_MD = VISUAL_QA_DIR / "visual-qa-report.md"

FORBIDDEN_TERMS = [
    "presentation prep",
    "use the guide",
    "prepare answers",
    "screenshots still required",
    "evidence to be added",
    "add screenshots",
    "capture screenshots",
    "student should",
    "student must",
    "manual screenshot",
    "placeholder",
    "replace",
    "todo",
    "sample evidence",
    "local guide",
]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.layout = ""
        self.images = []
        self.classes = []
        self.ids = set()
        self.tags = Counter()
        self.text_chunks = []
        self._capture_text = True

    def handle_starttag(self, tag, attrs):
        self.tags[tag] += 1
        values = dict(attrs)
        if tag == "body":
            self.layout = values.get("data-layout", "")
        if values.get("class"):
            self.classes.extend(values["class"].split())
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "img" and values.get("src"):
            self.images.append(values["src"])
        if tag in {"script", "style"}:
            self._capture_text = False

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self._capture_text = True

    def handle_data(self, data):
        if self._capture_text:
            text = re.sub(r"\s+", " ", data).strip()
            if text:
                self.text_chunks.append(text)


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


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


def png_dimensions(path):
    with path.open("rb") as handle:
        signature = handle.read(24)
    if len(signature) < 24 or signature[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", signature[16:24])


def public_screenshots(site):
    screenshot_dir = site / "assets" / "screenshots"
    if not screenshot_dir.exists():
        return []
    return [
        file
        for file in screenshot_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        and "asset" not in file.name.lower()
        and "evidence" not in file.name.lower()
    ]


def certificates(site):
    cert_dir = site / "assets" / "certificates"
    if not cert_dir.exists():
        return []
    return [
        file
        for file in cert_dir.iterdir()
        if file.is_file() and file.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
    ]


def css_hex_colors(css):
    return re.findall(r"#[0-9a-fA-F]{3,6}", css)


def main():
    VISUAL_QA_DIR.mkdir(parents=True, exist_ok=True)
    items = active_items()
    results = []
    failures = []
    layout_counts = Counter()
    structure_counts = Counter()

    for item in items:
        student = item["studentName"]
        slug = slugify(student)
        site = Path(item["portfolioPath"]) / "site"
        html_path = site / "index.html"
        css_path = site / "styles.css"
        desktop = VISUAL_QA_DIR / slug / "desktop.png"
        mobile = VISUAL_QA_DIR / slug / "mobile.png"
        issues = []

        html = html_path.read_text(encoding="utf-8", errors="ignore")
        css = css_path.read_text(encoding="utf-8", errors="ignore") if css_path.exists() else ""
        lowered = html.lower()
        parser = PageParser()
        parser.feed(html)

        layout_counts[parser.layout] += 1
        structure_key = "-".join(sorted(set(parser.classes))[:12])
        structure_counts[structure_key] += 1

        for term in FORBIDDEN_TERMS:
            if term in lowered:
                issues.append(f"forbidden public term: {term}")
        if re.search(r"\bAI\b", html):
            issues.append("forbidden public term: AI")

        if not parser.layout:
            issues.append("missing data-layout")
        if parser.tags["header"] == 0:
            issues.append("missing header")
        if parser.tags["footer"] == 0:
            issues.append("missing footer")
        if "@media" not in css or "760px" not in css:
            issues.append("missing mobile media query near 760px")
        if len(re.findall(r"min-height\s*:\s*(2[2-9][1-9]|[3-9]\d\d)px", css)) > 3:
            issues.append("too many large min-height cards")
        if len(css_hex_colors(css)) >= 2:
            colors = css_hex_colors(css)
            blueish = sum(1 for color in colors if color.lower() in {"#2563eb", "#0284c7", "#0ea5e9", "#0369a1"})
            white = sum(1 for color in colors if color.lower() in {"#ffffff", "#f8fafc", "#f5f7fb"})
            if blueish >= 2 and white >= 2:
                issues.append("possible white/blue clone styling")
        if not re.search(r"(section-title span|doc-icon|terminal-bar|profile-stack|phone-frame)", css):
            issues.append("missing icon or visual marker styling")

        cert_files = certificates(site)
        has_cert_section = "certificates" in parser.ids or "certificate-section" in parser.classes
        if not cert_files and has_cert_section:
            issues.append("certificate section visible without certificate files")

        screenshot_files = public_screenshots(site)
        has_evidence_section = "work-record" in parser.ids or "evidence-section" in parser.classes
        if not screenshot_files and has_evidence_section:
            issues.append("evidence section visible without real screenshots")

        for image in parser.images:
            image_path = site / image
            if not image_path.exists():
                issues.append(f"broken image reference: {image}")

        for screenshot_path, expected in [(desktop, (1440, 1000)), (mobile, (390, 900))]:
            if not screenshot_path.exists():
                issues.append(f"missing screenshot: {screenshot_path.name}")
            else:
                dimensions = png_dimensions(screenshot_path)
                if dimensions != expected:
                    issues.append(f"{screenshot_path.name} dimensions {dimensions}, expected {expected}")
                if screenshot_path.stat().st_size < 25000:
                    issues.append(f"{screenshot_path.name} appears visually sparse")

        all_text = " ".join(parser.text_chunks)
        long_lines = [chunk for chunk in parser.text_chunks if len(chunk) > 260]
        if long_lines:
            issues.append("body text line length may be too wide")

        result = {
            "studentName": student,
            "layout": parser.layout,
            "desktopScreenshot": str(desktop.relative_to(ROOT)) if desktop.exists() else "",
            "mobileScreenshot": str(mobile.relative_to(ROOT)) if mobile.exists() else "",
            "certificatesDisplayed": bool(cert_files),
            "evidenceDisplayed": bool(screenshot_files),
            "issues": issues,
            "textLength": len(all_text),
        }
        results.append(result)
        failures.extend(f"{student}: {issue}" for issue in issues)

    repeated_layouts = {layout: count for layout, count in layout_counts.items() if count > 3}
    if repeated_layouts:
        failures.append(f"More than 3 portfolios use same layout pattern: {repeated_layouts}")

    distinct_layouts = len([layout for layout in layout_counts if layout])
    if distinct_layouts < 14:
        failures.append(f"Expected at least 14 distinct visual composition patterns, found {distinct_layouts}")

    desktop_count = sum(1 for item in items if (VISUAL_QA_DIR / slugify(item["studentName"]) / "desktop.png").exists())
    mobile_count = sum(1 for item in items if (VISUAL_QA_DIR / slugify(item["studentName"]) / "mobile.png").exists())
    if desktop_count != 17:
        failures.append(f"Expected 17 desktop screenshots, found {desktop_count}")
    if mobile_count != 17:
        failures.append(f"Expected 17 mobile screenshots, found {mobile_count}")

    report = {
        "generatedAt": __import__("datetime").datetime.now().isoformat(),
        "portfoliosRendered": len(items),
        "desktopScreenshots": desktop_count,
        "mobileScreenshots": mobile_count,
        "distinctLayoutFamilies": distinct_layouts,
        "layoutCounts": dict(layout_counts),
        "results": results,
        "failures": failures,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Visual QA Report",
        "",
        f"- Portfolios rendered locally: {len(items)}",
        f"- Desktop screenshots captured: {desktop_count}",
        f"- Mobile screenshots captured: {mobile_count}",
        f"- Distinct visual composition patterns: {distinct_layouts}",
        f"- Failures: {len(failures)}",
        "",
        "## Layout Families",
    ]
    lines.extend(f"- {layout}: {count}" for layout, count in sorted(layout_counts.items()))
    lines.extend(["", "## Portfolio Results"])
    for result in results:
        issue_text = "; ".join(result["issues"]) if result["issues"] else "passed"
        lines.append(f"- {result['studentName']}: {result['layout']} - {issue_text}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if failures:
        for failure in failures:
            print(failure)
        print(f"Visual QA score failed with {len(failures)} issue(s).")
        return 1

    print("Visual QA score passed.")
    print(f"Portfolios rendered locally: {len(items)}")
    print(f"Desktop screenshots captured: {desktop_count}")
    print(f"Mobile screenshots captured: {mobile_count}")
    print(f"Distinct visual composition patterns: {distinct_layouts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
