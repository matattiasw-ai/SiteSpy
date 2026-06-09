import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"


AREAS = {
    "Valentina Correia": {
        "pattern": "data-analytics",
        "role": "Reporting and cost summary reviewer",
        "contribution": "My contribution focused on reviewing report-ready cost summaries, BOQ-style presentation, and the way project totals are communicated clearly.",
        "challenge": "The main challenge was keeping technical estimate information readable. The solution was to present totals, categories, and project context in a compact reporting layout.",
        "reflection": "I strengthened my understanding of structured project reporting, GitHub Pages deployment, and the link between user-facing summaries and project records.",
        "skills": ["HTML", "CSS", "GitHub Pages", "Cost reports", "Project records", "Team review"],
    },
    "Haipumbu Beatha NP": {
        "pattern": "engineering-blueprint",
        "role": "Estimation workflow reviewer",
        "contribution": "My contribution focused on the calculation workflow that connects measurements, saved estimates, and clear construction project outputs.",
        "challenge": "The main challenge was explaining calculations without making the page feel overloaded. The solution was a direct technical layout with concise result blocks.",
        "reflection": "I improved my confidence with measurement logic, project documentation, and disciplined Git commits.",
        "skills": ["Measurement flow", "Estimates", "HTML", "CSS", "Git", "Documentation"],
    },
    "Hamberera Karl PM": {
        "pattern": "clean-documentation",
        "role": "Data model documentation reviewer",
        "contribution": "My contribution focused on documenting how project records are organised and how reliable data structure supports the SiteSpy workflow.",
        "challenge": "The main challenge was turning data structure notes into a readable showcase. The solution was a documentation-first layout with clear sections.",
        "reflection": "I learned how data decisions affect user experience, collaboration, and long-term project maintainability.",
        "skills": ["Data structure", "Documentation", "GitHub", "Review notes", "Static sites", "Project planning"],
    },
    "Hamukwaya NP Petrus": {
        "pattern": "cybersecurity-dark",
        "role": "Access and profile workflow reviewer",
        "contribution": "My contribution focused on sign-in, user profile flow, and the importance of controlled access in a team project tool.",
        "challenge": "The main challenge was presenting security-related work without exposing sensitive implementation details. The solution was a restrained access-control theme.",
        "reflection": "I gained a stronger understanding of responsible user workflows, account boundaries, and secure team collaboration.",
        "skills": ["Access control", "Profiles", "Git", "GitHub", "Security review", "Expo app context"],
    },
    "Martha Heita": {
        "pattern": "soft-glass",
        "role": "Interface quality reviewer",
        "contribution": "My contribution focused on form feedback, validation states, loading states, and the quality of the app experience during everyday use.",
        "challenge": "The main challenge was describing interface quality as practical project work. The solution was a polished product-quality layout with concise examples.",
        "reflection": "I learned how small interface details can make a technical app feel clearer, more reliable, and easier to trust.",
        "skills": ["UI quality", "Validation", "Loading states", "CSS", "Static portfolio", "Review writing"],
    },
    "Hilda Iita": {
        "pattern": "github-contribution",
        "role": "Quality and workflow reviewer",
        "contribution": "My contribution focused on project checks, workflow review, and documenting how the team keeps the project organised.",
        "challenge": "The main challenge was linking quality work to visible portfolio evidence. The solution was a contribution-log style layout.",
        "reflection": "I improved my understanding of checks, project review, and how GitHub supports shared responsibility.",
        "skills": ["Project checks", "GitHub workflow", "Documentation", "Static hosting", "Team review", "Quality notes"],
    },
    "Mathias Jonas": {
        "pattern": "dashboard-cards",
        "role": "Project history workflow reviewer",
        "contribution": "My contribution focused on how project history and detail views help users return to earlier work and understand saved records.",
        "challenge": "The main challenge was making workflow history feel concrete. The solution was a dashboard-style page with focused process cards.",
        "reflection": "I learned how navigation, saved records, and readable detail views support a practical project app.",
        "skills": ["Project history", "Detail views", "Dashboard layout", "HTML", "CSS", "Git"],
    },
    "Klaudia Kambowe": {
        "pattern": "modern-saas",
        "role": "Project service workflow reviewer",
        "contribution": "My contribution focused on create, edit, and project service workflows that keep SiteSpy useful for repeated project work.",
        "challenge": "The main challenge was presenting service workflow as a user-facing outcome. The solution was a modern SaaS-style case study.",
        "reflection": "I learned how service flow, form structure, and reliable saves support a professional mobile tool.",
        "skills": ["Project services", "CRUD flow", "Forms", "GitHub Pages", "CSS", "Workflow review"],
    },
    "Tunacky Kandere": {
        "pattern": "mobile-case",
        "role": "Mobile navigation and dashboard reviewer",
        "contribution": "My contribution focused on the landing experience, splash flow, dashboard structure, and how users move through the app.",
        "challenge": "The main challenge was capturing mobile flow on a static page. The solution was a compact mobile case-study layout.",
        "reflection": "I learned how first screens, navigation, and information hierarchy shape the user experience.",
        "skills": ["Mobile layout", "Navigation", "Dashboard", "Expo context", "CSS", "Git workflow"],
    },
    "Johannes M Kandjeke": {
        "pattern": "academic-report",
        "role": "Responsive documentation reviewer",
        "contribution": "My contribution focused on responsive layout review, spacing, typography, and documentation that supports final presentation.",
        "challenge": "The main challenge was making review work easy to assess. The solution was an academic report format with clear sections.",
        "reflection": "I learned how responsive design and written explanation work together in a technical portfolio.",
        "skills": ["Responsive design", "Typography", "Documentation", "Portfolio review", "HTML", "CSS"],
    },
    "Amalia Mangundu": {
        "pattern": "product-landing",
        "role": "Settings and reusable controls reviewer",
        "contribution": "My contribution focused on profile, settings, and reusable controls that help the app feel consistent across screens.",
        "challenge": "The main challenge was connecting reusable UI work to visible project value. The solution was a product-focused showcase.",
        "reflection": "I learned how consistency, settings, and reusable elements improve a user's confidence in an app.",
        "skills": ["Settings", "Reusable controls", "Profile flow", "Product UI", "Git", "CSS"],
    },
    "Washington Matattias": {
        "pattern": "presentation-deck",
        "role": "Release coordination and integration reviewer",
        "contribution": "My contribution focused on final integration, build readiness, portfolio coordination, and keeping the project aligned for delivery.",
        "challenge": "The main challenge was coordinating many moving parts into a coherent final package. The solution was a presentation-deck style report.",
        "reflection": "I strengthened my understanding of release preparation, Git history, team coordination, and technical handover.",
        "skills": ["Release readiness", "Integration", "GitHub", "Portfolio coordination", "Expo", "Firebase context"],
    },
    "Kavakuru Metarere": {
        "pattern": "split-hero",
        "role": "Authentication screen reviewer",
        "contribution": "My contribution focused on the authentication screens and the flow between login, registration, and password recovery.",
        "challenge": "The main challenge was presenting authentication flow without implementation clutter. The solution was a clear split-layout case study.",
        "reflection": "I learned how entry screens shape trust and how clear account flows support a practical mobile app.",
        "skills": ["Authentication flow", "Login screens", "Register flow", "CSS", "Git", "Static pages"],
    },
    "Emilly Ndapuka": {
        "pattern": "sidebar-profile",
        "role": "Field form and estimate reviewer",
        "contribution": "My contribution focused on project creation, field input structure, and manual estimate forms for construction project records.",
        "challenge": "The main challenge was making forms feel like field work instead of abstract data entry. The solution was a profile-and-process layout.",
        "reflection": "I learned how form structure, validation, and concise labels support efficient project recording.",
        "skills": ["Field forms", "Project creation", "Estimate forms", "HTML", "CSS", "GitHub workflow"],
    },
    "Shikongo Linus TK": {
        "pattern": "terminal-code",
        "role": "Deployment readiness reviewer",
        "contribution": "My contribution focused on deployment notes, release readiness, and the steps that help a project become presentable online.",
        "challenge": "The main challenge was making deployment work visible without turning the page into a command list. The solution was a compact code-themed report.",
        "reflection": "I learned how deployment settings, clear scripts, and GitHub workflows support project delivery.",
        "skills": ["Deployment", "GitHub Actions", "Pages", "Release notes", "Scripts", "Static hosting"],
    },
    "Hilma Shuumbwa": {
        "pattern": "minimal-monochrome",
        "role": "Runtime configuration reviewer",
        "contribution": "My contribution focused on configuration loading, environment awareness, and the checks that help the app start reliably.",
        "challenge": "The main challenge was explaining runtime configuration without exposing private values. The solution was a minimal technical report layout.",
        "reflection": "I learned how configuration choices affect reliability across development, preview, and release builds.",
        "skills": ["Runtime config", "Expo", "Firebase context", "Diagnostics", "Git", "Documentation"],
    },
    "Tjatindi Michael Kazundire": {
        "pattern": "portfolio-magazine",
        "role": "Security rules and access documentation reviewer",
        "contribution": "My contribution focused on security rules, access notes, and how project records can be protected in a Firebase-backed app.",
        "challenge": "The main challenge was communicating security work clearly. The solution was an editorial portfolio layout with concise report sections.",
        "reflection": "I learned how access rules and documentation help protect project information while supporting teamwork.",
        "skills": ["Security rules", "Access review", "Firebase context", "Documentation", "GitHub", "CSS"],
    },
}

PATTERN_LABELS = {
    "split-hero": "Split Hero",
    "sidebar-profile": "Sidebar Profile",
    "terminal-code": "Terminal Code",
    "dashboard-cards": "Dashboard Cards",
    "mobile-case": "Mobile Case Study",
    "academic-report": "Academic Report",
    "product-landing": "Product Landing",
    "cybersecurity-dark": "Cybersecurity Dark",
    "data-analytics": "Data Analytics",
    "github-contribution": "GitHub Contribution",
    "minimal-monochrome": "Minimal Monochrome",
    "soft-glass": "Soft Glass UI",
    "engineering-blueprint": "Engineering Blueprint",
    "clean-documentation": "Clean Documentation",
    "modern-saas": "Modern SaaS",
    "portfolio-magazine": "Portfolio Magazine",
    "presentation-deck": "Presentation Deck",
}

THEMES = {
    "split-hero": ("#f6f8fb", "#ffffff", "#142033", "#5b6778", "#2563eb", "#0f766e"),
    "sidebar-profile": ("#f7f2ea", "#fffdf8", "#241d18", "#6c6259", "#b45309", "#0f766e"),
    "terminal-code": ("#0b1020", "#121a2c", "#f8fafc", "#b8c4d4", "#22c55e", "#38bdf8"),
    "dashboard-cards": ("#f3f6fb", "#ffffff", "#14213d", "#59677f", "#4f46e5", "#0891b2"),
    "mobile-case": ("#eef7ff", "#ffffff", "#102a43", "#61758a", "#0284c7", "#16a34a"),
    "academic-report": ("#fffaf2", "#ffffff", "#2c241c", "#685f55", "#92400e", "#2563eb"),
    "product-landing": ("#f4fbf8", "#ffffff", "#10261f", "#596f68", "#059669", "#7c3aed"),
    "cybersecurity-dark": ("#0e1117", "#171b24", "#f5f7fb", "#bac3d1", "#ef4444", "#22c55e"),
    "data-analytics": ("#f6f8ff", "#ffffff", "#152033", "#5c667a", "#2563eb", "#14b8a6"),
    "github-contribution": ("#f6fbf7", "#ffffff", "#18221b", "#526055", "#16a34a", "#334155"),
    "minimal-monochrome": ("#f7f7f7", "#ffffff", "#111111", "#666666", "#111111", "#525252"),
    "soft-glass": ("#f8f5ff", "rgba(255,255,255,.82)", "#231b34", "#6d647a", "#db2777", "#6366f1"),
    "engineering-blueprint": ("#edf6ff", "#ffffff", "#102236", "#57708a", "#0369a1", "#ca8a04"),
    "clean-documentation": ("#f8fafc", "#ffffff", "#172033", "#64748b", "#475569", "#0f766e"),
    "modern-saas": ("#f5f7fb", "#ffffff", "#131c2b", "#5e6b7f", "#7c3aed", "#0ea5e9"),
    "portfolio-magazine": ("#fff7ed", "#ffffff", "#261b12", "#75685b", "#ea580c", "#0f766e"),
    "presentation-deck": ("#111827", "#1f2937", "#f8fafc", "#d1d5db", "#facc15", "#38bdf8"),
}

SCREENSHOTS = [
    ("live-homepage.png", "Live portfolio homepage"),
    ("github-repository-main.png", "GitHub repository main page"),
    ("github-actions-success.png", "GitHub Actions successful deployment run"),
    ("commit-history.png", "Commit history page"),
    ("development-branch.png", "Development branch or contribution branch"),
    ("pull-request.png", "Pull request page once created"),
    ("project-app-screen.png", "Project app screen, if available"),
    ("code-contribution.png", "Code contribution or changed file"),
    ("documentation-contribution.png", "README or documentation contribution"),
    ("certificate-or-proof.png", "Certificate or proof document if available"),
]


def esc(value):
    return str(value or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def pdf_escape(value):
    return str(value or "").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap_text(value, width=88):
    words = str(value).split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > width:
            if current:
                lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines or [""]


def write_simple_pdf(path, title, paragraphs):
    lines = [title, ""]
    for paragraph in paragraphs:
        if isinstance(paragraph, (list, tuple)):
            for item in paragraph:
                lines.extend(wrap_text(f"- {item}"))
        else:
            lines.extend(wrap_text(paragraph))
        lines.append("")

    pages = [lines[index : index + 42] for index in range(0, len(lines), 42)] or [[]]
    objects = []

    def add(obj):
        objects.append(obj)
        return len(objects)

    catalog_id = add("")
    pages_id = add("")
    font_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    for page in pages:
        commands = ["BT", "/F1 11 Tf", "50 780 Td", "14 TL"]
        first = True
        for line in page:
            if not first:
                commands.append("T*")
            commands.append(f"({pdf_escape(line)}) Tj")
            first = False
        commands.append("ET")
        stream = "\n".join(commands)
        content_id = add(f"<< /Length {len(stream.encode('latin-1', 'replace'))} >>\nstream\n{stream}\nendstream")
        page_id = add(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>"
        )
        page_ids.append(page_id)

    objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>"
    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{' '.join(f'{page_id} 0 R' for page_id in page_ids)}] /Count {len(page_ids)} >>"

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode())
        output.extend(obj.encode("latin-1", "replace"))
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    output.extend(b"0000000000 65535 f\n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n\n".encode())
    output.extend(f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    path.write_bytes(output)


def public_screenshots(screenshot_dir):
    if not screenshot_dir.exists():
        return []
    files = []
    for file in sorted(screenshot_dir.iterdir()):
        if file.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        lowered = file.name.lower()
        if "asset" in lowered or "evidence" in lowered:
            continue
        files.append(file)
    return files


def active_items():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    items = []
    for item in config:
        name = text(item.get("studentName"))
        username = text(item.get("githubUsername"))
        if name.lower() in {"penny", "ndaitavela"}:
            continue
        if name.lower().startswith("nambuli") or username == "studentgithub":
            continue
        items.append(item)
    return items


def build_metric_cards(item, area, pattern_label):
    repo_url = f"https://github.com/{item['githubUsername']}/{item['repoName']}"
    live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
    return f"""
      <div class="metric"><span>Role</span><strong>{esc(area['role'])}</strong></div>
      <div class="metric"><span>Project</span><strong>SiteSpy</strong></div>
      <div class="metric"><span>GitHub</span><strong>{esc(item['githubUsername'])}</strong></div>
      <div class="metric"><span>Portfolio</span><strong>{esc(pattern_label)}</strong></div>
      <div class="metric wide"><span>Repository</span><a href="{esc(repo_url)}">{esc(item['repoName'])}</a></div>
      <div class="metric wide"><span>Live Site</span><a href="{esc(live_url)}">Published portfolio</a></div>
"""


def build_screenshot_section(item, files):
    if not files:
        return ""
    cards = []
    site_root = Path(item["portfolioPath"]) / "site"
    for file in files:
        rel = file.relative_to(site_root).as_posix()
        title = file.stem.replace("-", " ").title()
        cards.append(
            f'<article class="screen-card"><img src="{esc(rel)}" alt="{esc(title)}"><h3>{esc(title)}</h3></article>'
        )
    return f"""
    <section class="section screenshots" id="screens">
      <div class="section-heading"><span>Project Records</span><h2>Visual Work Record</h2></div>
      <div class="screen-grid">
        {''.join(cards)}
      </div>
    </section>
"""


def build_html(item, area, screenshots):
    pattern = area["pattern"]
    pattern_label = PATTERN_LABELS[pattern]
    repo_url = f"https://github.com/{item['githubUsername']}/{item['repoName']}"
    live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
    skills = "".join(f"<li>{esc(skill)}</li>" for skill in area["skills"])
    metrics = build_metric_cards(item, area, pattern_label)
    screenshot_html = build_screenshot_section(item, screenshots)
    summary = "The project demonstrates a practical Expo React Native and Firebase app for construction records, wall measurements, material estimates, and project reporting."
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(item['studentName'])} | SiteSpy Portfolio</title>
  <meta name="description" content="{esc(item['studentName'])} SiteSpy project showcase.">
  <link rel="stylesheet" href="styles.css">
</head>
<body class="pattern-{esc(pattern)}">
  <nav class="navbar" aria-label="Main navigation">
    <a class="brand" href="#top">SiteSpy Portfolio</a>
    <div class="navlinks">
      <a href="#overview">Overview</a>
      <a href="#contribution">Contribution</a>
      <a href="#reports">Reports</a>
      <a href="{esc(repo_url)}">Repository</a>
    </div>
  </nav>

  <header class="hero" id="top">
    <div class="hero-copy">
      <p class="eyebrow">{esc(pattern_label)}</p>
      <h1>{esc(item['studentName'])}</h1>
      <p class="role">{esc(area['role'])}</p>
      <p class="summary">This portfolio presents my SiteSpy contribution, learning reflection, and project report resources in a polished public showcase.</p>
      <div class="hero-actions">
        <a class="button primary" href="{esc(repo_url)}">Repository</a>
        <a class="button secondary" href="{esc(live_url)}">Live Project</a>
      </div>
    </div>
    <aside class="profile-panel" aria-label="Portfolio profile">
      {metrics}
    </aside>
  </header>

  <main>
    <section class="section overview" id="overview">
      <div class="section-heading"><span>Project Overview</span><h2>SiteSpy Construction Project Tool</h2></div>
      <p>{esc(summary)}</p>
      <div class="overview-grid">
        <article><h3>Project Focus</h3><p>SiteSpy supports structured field records, measurement review, estimate summaries, and clear project information.</p></article>
        <article><h3>Portfolio Focus</h3><p>This section presents the project area I reviewed and the way that area contributes to a complete app experience.</p></article>
        <article><h3>Outcome</h3><p>The outcome was a concise portfolio that connects individual contribution, technical learning, and final project readiness.</p></article>
      </div>
    </section>

    <section class="section contribution" id="contribution">
      <div class="section-heading"><span>My Contribution</span><h2>Focused Project Work</h2></div>
      <div class="feature-grid">
        <article class="feature-card main-card"><h3>Contribution Area</h3><p>{esc(area['contribution'])}</p></article>
        <article class="feature-card"><h3>Challenge and Solution</h3><p>{esc(area['challenge'])}</p></article>
        <article class="feature-card"><h3>Learning Reflection</h3><p>{esc(area['reflection'])}</p></article>
      </div>
    </section>

    <section class="section skills" id="skills">
      <div class="section-heading"><span>Skills and Tools</span><h2>Technical Growth</h2></div>
      <ul class="skill-list">{skills}</ul>
    </section>

    {screenshot_html}

    <section class="section reports" id="reports">
      <div class="section-heading"><span>Reports</span><h2>Portfolio Resources</h2></div>
      <div class="report-links">
        <a href="docs/presentation-guide.pdf">Presentation Report</a>
        <a href="docs/contribution-report.pdf">Contribution Report</a>
        <a href="{esc(repo_url)}">Repository</a>
        <a href="{esc(live_url)}">Live Project</a>
      </div>
    </section>
  </main>

  <footer>
    <p>{esc(item['studentName'])} | {esc(item['githubUsername'])} | SiteSpy</p>
  </footer>
  <script src="script.js" defer></script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def build_css(pattern):
    bg, surface, ink, muted, accent, accent2 = THEMES[pattern]
    layout = {
        "split-hero": ("1.05fr .95fr", "repeat(3, 1fr)", "linear-gradient(120deg, var(--accent-soft), transparent 58%)"),
        "sidebar-profile": (".78fr 1.22fr", "repeat(2, 1fr)", "linear-gradient(90deg, var(--accent-soft), transparent 55%)"),
        "terminal-code": ("1.1fr .9fr", "repeat(3, 1fr)", "linear-gradient(135deg, rgba(34,197,94,.18), transparent 48%)"),
        "dashboard-cards": ("1fr 1fr", "repeat(3, 1fr)", "linear-gradient(135deg, var(--accent-soft), var(--accent2-soft))"),
        "mobile-case": ("1.15fr .85fr", "repeat(3, 1fr)", "linear-gradient(110deg, var(--accent2-soft), transparent 50%)"),
        "academic-report": ("1fr .92fr", "repeat(2, 1fr)", "linear-gradient(180deg, var(--accent-soft), transparent 44%)"),
        "product-landing": ("1.2fr .8fr", "repeat(3, 1fr)", "linear-gradient(120deg, var(--accent-soft), var(--accent2-soft))"),
        "cybersecurity-dark": ("1fr .9fr", "repeat(2, 1fr)", "linear-gradient(135deg, rgba(239,68,68,.16), transparent 48%)"),
        "data-analytics": ("1.1fr .9fr", "repeat(4, 1fr)", "linear-gradient(120deg, var(--accent-soft), transparent 60%)"),
        "github-contribution": ("1fr 1fr", "repeat(3, 1fr)", "linear-gradient(135deg, var(--accent-soft), transparent 50%)"),
        "minimal-monochrome": ("1.25fr .75fr", "repeat(2, 1fr)", "linear-gradient(90deg, rgba(0,0,0,.05), transparent 50%)"),
        "soft-glass": ("1.05fr .95fr", "repeat(3, 1fr)", "linear-gradient(135deg, var(--accent-soft), var(--accent2-soft))"),
        "engineering-blueprint": ("1fr 1fr", "repeat(3, 1fr)", "linear-gradient(135deg, var(--accent-soft), transparent 52%)"),
        "clean-documentation": ("1.22fr .78fr", "repeat(2, 1fr)", "linear-gradient(180deg, rgba(71,85,105,.08), transparent 45%)"),
        "modern-saas": ("1.1fr .9fr", "repeat(4, 1fr)", "linear-gradient(135deg, var(--accent-soft), var(--accent2-soft))"),
        "portfolio-magazine": (".95fr 1.05fr", "repeat(2, 1fr)", "linear-gradient(90deg, var(--accent-soft), transparent 58%)"),
        "presentation-deck": ("1.08fr .92fr", "repeat(3, 1fr)", "linear-gradient(135deg, rgba(250,204,21,.16), transparent 50%)"),
    }[pattern]
    hero_cols, overview_cols, backdrop = layout
    mono = "Consolas, 'SFMono-Regular', Menlo, monospace" if pattern in {"terminal-code", "cybersecurity-dark"} else "Inter, Segoe UI, Arial, sans-serif"
    return f""":root {{
  --bg: {bg};
  --surface: {surface};
  --ink: {ink};
  --muted: {muted};
  --accent: {accent};
  --accent2: {accent2};
  --accent-soft: color-mix(in srgb, var(--accent) 14%, transparent);
  --accent2-soft: color-mix(in srgb, var(--accent2) 12%, transparent);
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background: var(--bg);
  font-family: {mono};
  line-height: 1.55;
}}
body::before {{
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  background: {backdrop};
}}
a {{ color: inherit; }}
.navbar {{
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  max-width: 1140px;
  margin: 0 auto;
  padding: 14px 20px;
  background: color-mix(in srgb, var(--bg) 84%, transparent);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 18%, transparent);
}}
.brand {{ font-weight: 800; text-decoration: none; letter-spacing: .01em; }}
.navlinks {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.navlinks a {{
  text-decoration: none;
  color: var(--muted);
  padding: 7px 10px;
  border-radius: 8px;
  font-size: 14px;
}}
.navlinks a:hover {{ color: var(--ink); background: var(--accent-soft); }}
.hero {{
  max-width: 1140px;
  margin: 0 auto;
  padding: 58px 20px 34px;
  display: grid;
  grid-template-columns: {hero_cols};
  gap: 24px;
  align-items: center;
}}
.hero-copy {{
  padding: 4px 0;
}}
.eyebrow {{
  margin: 0 0 10px;
  color: var(--accent);
  font-size: 13px;
  text-transform: uppercase;
  font-weight: 800;
  letter-spacing: .08em;
}}
h1 {{
  margin: 0;
  font-size: clamp(32px, 6vw, 56px);
  line-height: 1.02;
  letter-spacing: 0;
}}
.role {{
  margin: 12px 0 0;
  font-size: clamp(17px, 2.2vw, 22px);
  color: var(--accent2);
  font-weight: 750;
}}
.summary {{
  max-width: 660px;
  margin: 14px 0 0;
  color: var(--muted);
  font-size: 17px;
}}
.hero-actions, .report-links {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}}
.button, .report-links a {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 9px 13px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 800;
  border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent);
}}
.primary, .report-links a:first-child {{ color: var(--surface); background: var(--accent); }}
.secondary, .report-links a:nth-child(2) {{ color: var(--surface); background: var(--accent2); }}
.profile-panel {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  padding: 18px;
  border: 1px solid color-mix(in srgb, var(--accent) 24%, transparent);
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 18px 46px rgba(0,0,0,.10);
}}
.metric {{
  min-width: 0;
  padding: 12px;
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent) 7%, var(--surface));
}}
.metric.wide {{ grid-column: 1 / -1; }}
.metric span {{
  display: block;
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 800;
  letter-spacing: .06em;
}}
.metric strong, .metric a {{
  display: block;
  margin-top: 4px;
  overflow-wrap: anywhere;
  text-decoration: none;
  font-weight: 800;
}}
main {{ max-width: 1140px; margin: 0 auto; padding: 8px 20px 58px; }}
.section {{
  margin-top: 22px;
  padding: 24px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid color-mix(in srgb, var(--accent) 16%, transparent);
}}
.section-heading span {{
  display: block;
  color: var(--accent);
  font-size: 12px;
  font-weight: 850;
  text-transform: uppercase;
  letter-spacing: .08em;
  margin-bottom: 4px;
}}
h2 {{ margin: 0 0 12px; font-size: clamp(23px, 3.5vw, 34px); line-height: 1.1; }}
h3 {{ margin: 0 0 7px; font-size: 18px; }}
.overview-grid {{
  display: grid;
  grid-template-columns: {overview_cols};
  gap: 12px;
  margin-top: 16px;
}}
.overview-grid article, .feature-card {{
  padding: 16px;
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent) 6%, var(--surface));
  border: 1px solid color-mix(in srgb, var(--accent) 14%, transparent);
}}
.feature-grid {{
  display: grid;
  grid-template-columns: 1.1fr .95fr .95fr;
  gap: 12px;
}}
.main-card {{
  border-left: 5px solid var(--accent);
}}
.skill-list {{
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
}}
.skill-list li {{
  padding: 8px 11px;
  border-radius: 8px;
  color: var(--ink);
  background: color-mix(in srgb, var(--accent2) 10%, var(--surface));
  border: 1px solid color-mix(in srgb, var(--accent2) 20%, transparent);
  font-weight: 750;
}}
.screen-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}}
.screen-card {{
  overflow: hidden;
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent) 6%, var(--surface));
}}
.screen-card img {{
  display: block;
  width: 100%;
  height: 170px;
  object-fit: cover;
}}
.screen-card h3 {{ padding: 12px; font-size: 16px; }}
.reports {{
  background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 10%, var(--surface)), var(--surface));
}}
footer {{
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 20px 28px;
  color: var(--muted);
  text-align: center;
}}
@media (max-width: 860px) {{
  .navbar {{ position: static; align-items: flex-start; flex-direction: column; }}
  .hero, .feature-grid, .overview-grid {{ grid-template-columns: 1fr; }}
  .hero {{ padding-top: 34px; }}
  .profile-panel {{ grid-template-columns: 1fr; }}
  .section {{ padding: 18px; }}
}}
"""


def build_script():
    return """document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
"""


def build_guides(item, area):
    repo_url = f"https://github.com/{item['githubUsername']}/{item['repoName']}"
    live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
    presentation = f"""# {item['studentName']} Presentation Report

## Portfolio Details

- GitHub username: {item['githubUsername']}
- Repository: {item['repoName']}
- Live portfolio: {live_url}
- Project: SiteSpy

## Project Summary

SiteSpy is a mobile-focused project tool built with Expo React Native and Firebase. It supports construction project records, measurement review, estimate summaries, and clear project reporting.

## Contribution Summary

{area['contribution']}

## Challenge and Solution

{area['challenge']}

## Learning Reflection

{area['reflection']}

## Presentation Notes

- Explain what SiteSpy does for a user.
- Describe the assigned project area.
- Connect the public portfolio to the GitHub repository.
- Discuss GitHub Pages deployment and team collaboration.
- Refer to real screenshots only after they have been captured from the student's own repository or project work.
"""
    report = f"""# {item['studentName']} Contribution Report

## Student Details

- GitHub username: {item['githubUsername']}
- Repository: {item['repoName']}
- Live portfolio: {live_url}
- Project: SiteSpy

## Contribution Area

{area['contribution']}

## Project Context

SiteSpy is a construction support app that keeps project records, helps with wall measurements and material estimation, and prepares information for later review.

## Challenge and Solution

{area['challenge']}

## Learning Reflection

{area['reflection']}

## Repository Links

- Repository: {repo_url}
- Live portfolio: {live_url}
"""
    screenshot_guide = f"""# {item['studentName']} Screenshot Capture Guide

Capture only real screenshots from the student's own repository, live portfolio, project work, and GitHub workflow. Add files to `site/assets/screenshots/` using clear names.

## Required Screenshots

"""
    for filename, description in SCREENSHOTS:
        screenshot_guide += f"- `{filename}` - {description}\n"
    screenshot_guide += f"""
## After Capturing Screenshots

```bash
git checkout -b evidence-update
git add site/assets/screenshots docs
git commit -m "docs: add portfolio evidence screenshots"
git push -u origin evidence-update
```

## Portfolio

- Repository: {repo_url}
- Live portfolio: {live_url}
"""
    return presentation, report, screenshot_guide


def main():
    rows = []
    pdf_failures = []
    checklist = [
        "# SiteSpy Student Screenshot Checklist",
        "",
        "Capture only real evidence. Do not add screenshots that do not belong to the student or repository.",
        "",
    ]

    for item in active_items():
        student = item["studentName"]
        area = AREAS[student]
        portfolio = Path(item["portfolioPath"])
        site = portfolio / "site"
        docs = portfolio / "docs"
        site_docs = site / "docs"
        screenshots_dir = site / "assets" / "screenshots"
        docs.mkdir(parents=True, exist_ok=True)
        site_docs.mkdir(parents=True, exist_ok=True)
        site.mkdir(parents=True, exist_ok=True)
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        screenshots = public_screenshots(screenshots_dir)
        (site / "index.html").write_text(build_html(item, area, screenshots), encoding="utf-8")
        (site / "styles.css").write_text(build_css(area["pattern"]), encoding="utf-8")
        (site / "script.js").write_text(build_script(), encoding="utf-8")
        (site / "evidence.json").write_text(json.dumps([file.name for file in screenshots], indent=2) + "\n", encoding="utf-8")

        presentation, report, screenshot_guide = build_guides(item, area)
        (docs / "presentation-guide.md").write_text(presentation, encoding="utf-8")
        (docs / "contribution-report.md").write_text(report, encoding="utf-8")
        (docs / "screenshot-capture-guide.md").write_text(screenshot_guide, encoding="utf-8")

        try:
            write_simple_pdf(docs / "presentation-guide.pdf", f"{student} Presentation Report", presentation.split("\n\n"))
            write_simple_pdf(docs / "contribution-report.pdf", f"{student} Contribution Report", report.split("\n\n"))
            shutil.copyfile(docs / "presentation-guide.pdf", site_docs / "presentation-guide.pdf")
            shutil.copyfile(docs / "contribution-report.pdf", site_docs / "contribution-report.pdf")
            pdf_status = "created"
        except Exception as exc:
            pdf_status = f"failed: {exc}"
            pdf_failures.append({"studentName": student, "error": str(exc)})

        repo = f"{item['githubUsername']}/{item['repoName']}"
        live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
        checklist.extend(
            [
                f"## {student}",
                "",
                f"- Portfolio path: `{portfolio}`",
                f"- Repo URL: https://github.com/{repo}",
                f"- Live URL: {live_url}",
                f"- Save screenshots in: `{screenshots_dir}`",
                "",
                "| Filename | What it should show |",
                "|---|---|",
            ]
        )
        for filename, description in SCREENSHOTS:
            checklist.append(f"| `{filename}` | {description} |")
        checklist.extend(
            [
                "",
                "After adding screenshots:",
                "",
                "```bash",
                "git add site/assets/screenshots docs",
                'git commit -m "docs: add portfolio evidence screenshots"',
                "git push",
                "```",
                "",
            ]
        )

        rows.append(
            {
                "studentName": student,
                "portfolioPath": str(portfolio),
                "repo": repo,
                "liveUrl": live_url,
                "pattern": area["pattern"],
                "theme": PATTERN_LABELS[area["pattern"]],
                "publicScreenshotsShown": len(screenshots),
                "evidenceSectionHidden": len(screenshots) == 0,
                "pdfStatus": pdf_status,
                "filesChanged": [
                    "site/index.html",
                    "site/styles.css",
                    "site/script.js",
                    "site/evidence.json",
                    "docs/presentation-guide.md",
                    "docs/contribution-report.md",
                    "docs/screenshot-capture-guide.md",
                    "docs/presentation-guide.pdf",
                    "docs/contribution-report.pdf",
                    "site/docs/presentation-guide.pdf",
                    "site/docs/contribution-report.pdf",
                ],
            }
        )

    (ROOT / "portfolio-batch" / "STUDENT_SCREENSHOT_CHECKLIST.md").write_text("\n".join(checklist), encoding="utf-8")
    report_data = {
        "generatedAt": datetime.now().isoformat(),
        "portfoliosProcessed": len(rows),
        "skipped": ["Penny", "Ndaitavela", "Nambuli"],
        "publicInstructionalContentRemoved": True,
        "pdfFailures": pdf_failures,
        "portfolios": rows,
        "manualScreenshotWorkLocation": "portfolio-batch/STUDENT_SCREENSHOT_CHECKLIST.md",
    }
    (ROOT / "portfolio-batch" / "portfolio-visual-upgrade-report.json").write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    lines = [
        "# Portfolio Visual Upgrade Report",
        "",
        f"- Portfolios processed: {len(rows)}",
        "- Public pages use showcase/report copy only.",
        "- Public screenshot sections are hidden when real screenshots are not present.",
        "",
        "## Design Patterns",
    ]
    lines.extend(f"- {row['studentName']}: {row['theme']}" for row in rows)
    lines.extend(
        [
            "",
            "## PDF Status",
            "- All report PDFs created." if not pdf_failures else "- Some PDFs failed; see JSON report.",
            "",
            "## Remaining Screenshot Work",
            "- See `portfolio-batch/STUDENT_SCREENSHOT_CHECKLIST.md`.",
        ]
    )
    (ROOT / "portfolio-batch" / "portfolio-visual-upgrade-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Processed {len(rows)} active portfolios")
    print(f"PDF failures: {len(pdf_failures)}")


if __name__ == "__main__":
    main()
