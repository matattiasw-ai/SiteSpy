import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"

ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf"}
SCREENSHOT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

LAYOUTS = [
    {
        "id": "split-timeline",
        "label": "Split Hero + Timeline",
        "font": "Segoe UI, Arial, sans-serif",
        "bg": "#f5f7fb",
        "surface": "#ffffff",
        "ink": "#172033",
        "muted": "#596579",
        "accent": "#2563eb",
        "accent2": "#0f766e",
        "shape": "8px",
        "icon": "◆",
    },
    {
        "id": "sidebar-profile",
        "label": "Sidebar Profile",
        "font": "Trebuchet MS, Arial, sans-serif",
        "bg": "#f8f3eb",
        "surface": "#fffdf8",
        "ink": "#241d18",
        "muted": "#6a5f55",
        "accent": "#b45309",
        "accent2": "#0f766e",
        "shape": "14px",
        "icon": "▣",
    },
    {
        "id": "terminal-console",
        "label": "Terminal Console",
        "font": "Consolas, Menlo, monospace",
        "bg": "#080d18",
        "surface": "#111827",
        "ink": "#f8fafc",
        "muted": "#b8c2d1",
        "accent": "#22c55e",
        "accent2": "#38bdf8",
        "shape": "6px",
        "icon": "▸",
    },
    {
        "id": "mobile-case-study",
        "label": "Mobile App Case Study",
        "font": "Segoe UI, Arial, sans-serif",
        "bg": "#eef7ff",
        "surface": "#ffffff",
        "ink": "#102a43",
        "muted": "#5c7188",
        "accent": "#0284c7",
        "accent2": "#16a34a",
        "shape": "20px",
        "icon": "▰",
    },
    {
        "id": "analytics-dashboard",
        "label": "Dashboard Analytics",
        "font": "Arial, Helvetica, sans-serif",
        "bg": "#f4f6fb",
        "surface": "#ffffff",
        "ink": "#14213d",
        "muted": "#5b6680",
        "accent": "#4f46e5",
        "accent2": "#0891b2",
        "shape": "10px",
        "icon": "◈",
    },
    {
        "id": "academic-report",
        "label": "Academic Report",
        "font": "Georgia, Times New Roman, serif",
        "bg": "#fffaf2",
        "surface": "#ffffff",
        "ink": "#2c241c",
        "muted": "#685f55",
        "accent": "#92400e",
        "accent2": "#2563eb",
        "shape": "4px",
        "icon": "§",
    },
    {
        "id": "product-landing",
        "label": "Product Landing",
        "font": "Inter, Segoe UI, Arial, sans-serif",
        "bg": "#f4fbf8",
        "surface": "#ffffff",
        "ink": "#10261f",
        "muted": "#596f68",
        "accent": "#059669",
        "accent2": "#7c3aed",
        "shape": "16px",
        "icon": "●",
    },
    {
        "id": "security-interface",
        "label": "Cybersecurity Dark Interface",
        "font": "Segoe UI, Arial, sans-serif",
        "bg": "#0d1117",
        "surface": "#171b24",
        "ink": "#f5f7fb",
        "muted": "#bac3d1",
        "accent": "#ef4444",
        "accent2": "#22c55e",
        "shape": "8px",
        "icon": "⬡",
    },
    {
        "id": "data-chart-cards",
        "label": "Data Cards + Chart",
        "font": "Arial, Helvetica, sans-serif",
        "bg": "#f5f8ff",
        "surface": "#ffffff",
        "ink": "#152033",
        "muted": "#5c667a",
        "accent": "#2563eb",
        "accent2": "#14b8a6",
        "shape": "12px",
        "icon": "▥",
    },
    {
        "id": "github-contribution",
        "label": "GitHub Contribution",
        "font": "Verdana, Arial, sans-serif",
        "bg": "#f6fbf7",
        "surface": "#ffffff",
        "ink": "#18221b",
        "muted": "#526055",
        "accent": "#16a34a",
        "accent2": "#334155",
        "shape": "7px",
        "icon": "■",
    },
    {
        "id": "minimal-editorial",
        "label": "Minimal Editorial",
        "font": "Helvetica Neue, Arial, sans-serif",
        "bg": "#f7f7f7",
        "surface": "#ffffff",
        "ink": "#111111",
        "muted": "#666666",
        "accent": "#111111",
        "accent2": "#525252",
        "shape": "2px",
        "icon": "—",
    },
    {
        "id": "soft-glass",
        "label": "Soft Glassmorphism",
        "font": "Segoe UI, Arial, sans-serif",
        "bg": "#f8f5ff",
        "surface": "rgba(255,255,255,.84)",
        "ink": "#231b34",
        "muted": "#6d647a",
        "accent": "#db2777",
        "accent2": "#6366f1",
        "shape": "18px",
        "icon": "◇",
    },
    {
        "id": "engineering-blueprint",
        "label": "Engineering Blueprint",
        "font": "Trebuchet MS, Arial, sans-serif",
        "bg": "#edf6ff",
        "surface": "#ffffff",
        "ink": "#102236",
        "muted": "#57708a",
        "accent": "#0369a1",
        "accent2": "#ca8a04",
        "shape": "6px",
        "icon": "⊞",
    },
    {
        "id": "documentation-style",
        "label": "Documentation Style",
        "font": "Arial, Helvetica, sans-serif",
        "bg": "#f8fafc",
        "surface": "#ffffff",
        "ink": "#172033",
        "muted": "#64748b",
        "accent": "#475569",
        "accent2": "#0f766e",
        "shape": "8px",
        "icon": "¶",
    },
    {
        "id": "modern-saas",
        "label": "Modern SaaS Landing",
        "font": "Inter, Segoe UI, Arial, sans-serif",
        "bg": "#f5f7fb",
        "surface": "#ffffff",
        "ink": "#131c2b",
        "muted": "#5e6b7f",
        "accent": "#7c3aed",
        "accent2": "#0ea5e9",
        "shape": "14px",
        "icon": "✦",
    },
    {
        "id": "magazine-feature",
        "label": "Magazine Profile Feature",
        "font": "Georgia, Times New Roman, serif",
        "bg": "#fff7ed",
        "surface": "#ffffff",
        "ink": "#261b12",
        "muted": "#75685b",
        "accent": "#ea580c",
        "accent2": "#0f766e",
        "shape": "3px",
        "icon": "◆",
    },
    {
        "id": "presentation-deck",
        "label": "Presentation Deck",
        "font": "Segoe UI, Arial, sans-serif",
        "bg": "#111827",
        "surface": "#1f2937",
        "ink": "#f8fafc",
        "muted": "#d1d5db",
        "accent": "#facc15",
        "accent2": "#38bdf8",
        "shape": "12px",
        "icon": "▣",
    },
]

ASSIGNMENTS = {
    "Valentina Correia": ("data-chart-cards", "Reporting and cost summary reviewer", "reviewing report-ready cost summaries, BOQ-style presentation, and how project totals are communicated clearly", "keeping technical estimate information readable", "presenting totals, categories, and project context in a compact reporting structure", ["Cost reporting", "BOQ summaries", "GitHub Pages", "HTML", "CSS", "Project records"]),
    "Haipumbu Beatha NP": ("engineering-blueprint", "Estimation workflow reviewer", "the calculation workflow that connects measurements, saved estimates, and clear construction project outputs", "explaining calculations without overloading the reader", "using a technical layout with concise result blocks and measurement context", ["Measurement flow", "Estimates", "Technical writing", "Git", "CSS", "Construction context"]),
    "Hamberera Karl PM": ("documentation-style", "Data model documentation reviewer", "documenting how project records are organised and how reliable data structure supports the SiteSpy workflow", "turning data structure notes into a readable public showcase", "using a documentation-first layout with clear review sections", ["Data structure", "Documentation", "Static sites", "GitHub", "Review notes", "Project planning"]),
    "Hamukwaya NP Petrus": ("security-interface", "Access and profile workflow reviewer", "sign-in, user profile flow, and the importance of controlled access in a team project tool", "presenting access-related work without exposing sensitive implementation details", "using a restrained access-control interface that focuses on project value", ["Access control", "Profile flow", "Security review", "GitHub", "Expo context", "Team workflow"]),
    "Martha Heita": ("soft-glass", "Interface quality reviewer", "form feedback, validation states, loading states, and the quality of the app experience during everyday use", "describing interface quality as practical project work", "using polished product-quality sections that connect feedback to user trust", ["UI quality", "Validation", "Loading states", "CSS", "Static portfolio", "Review writing"]),
    "Hilda Iita": ("github-contribution", "Quality and workflow reviewer", "project checks, workflow review, and documenting how the team keeps the project organised", "linking quality work to visible project value", "using a contribution-log layout that connects checks, records, and delivery", ["Project checks", "GitHub workflow", "Documentation", "Static hosting", "Quality notes", "Team review"]),
    "Mathias Jonas": ("analytics-dashboard", "Project history workflow reviewer", "how project history and detail views help users return to earlier work and understand saved records", "making workflow history feel concrete", "using a dashboard layout with focused record and progress cards", ["Project history", "Detail views", "Dashboard layout", "HTML", "CSS", "Git"]),
    "Klaudia Kambowe": ("modern-saas", "Project service workflow reviewer", "create, edit, and project service workflows that keep SiteSpy useful for repeated project work", "presenting service workflow as a user-facing outcome", "using a modern product layout that frames workflow as reliable app value", ["Project services", "CRUD flow", "Forms", "GitHub Pages", "CSS", "Workflow review"]),
    "Tunacky Kandere": ("mobile-case-study", "Mobile navigation and dashboard reviewer", "the landing experience, splash flow, dashboard structure, and how users move through the app", "capturing mobile flow on a static page", "using a mobile case-study layout with compact device-style sections", ["Mobile layout", "Navigation", "Dashboard", "Expo context", "CSS", "Git workflow"]),
    "Johannes M Kandjeke": ("academic-report", "Responsive documentation reviewer", "responsive layout review, spacing, typography, and documentation that supports final presentation", "making review work easy to assess", "using an academic report format with clear evidence-neutral sections", ["Responsive design", "Typography", "Documentation", "Portfolio review", "HTML", "CSS"]),
    "Amalia Mangundu": ("product-landing", "Settings and reusable controls reviewer", "profile, settings, and reusable controls that help the app feel consistent across screens", "connecting reusable interface work to visible project value", "using a product landing structure that highlights consistency and app confidence", ["Settings", "Reusable controls", "Profile flow", "Product UI", "Git", "CSS"]),
    "Washington Matattias": ("presentation-deck", "Release coordination and integration reviewer", "final integration, build readiness, portfolio coordination, and keeping the project aligned for delivery", "coordinating many moving parts into a coherent final package", "using a presentation-deck structure that shows readiness, reports, and project links", ["Release readiness", "Integration", "GitHub", "Portfolio coordination", "Expo", "Firebase context"]),
    "Kavakuru Metarere": ("split-timeline", "Authentication screen reviewer", "the authentication screens and the flow between login, registration, and password recovery", "presenting authentication flow without implementation clutter", "using a split timeline layout that keeps entry flow clear and concise", ["Authentication flow", "Login screens", "Register flow", "CSS", "Git", "Static pages"]),
    "Emilly Ndapuka": ("sidebar-profile", "Field form and estimate reviewer", "project creation, field input structure, and manual estimate forms for construction project records", "making forms feel like field work instead of abstract data entry", "using a profile-and-process layout that highlights field recording value", ["Field forms", "Project creation", "Estimate forms", "HTML", "CSS", "GitHub workflow"]),
    "Shikongo Linus TK": ("terminal-console", "Deployment readiness reviewer", "deployment notes, release readiness, and the steps that help a project become presentable online", "making deployment work visible without turning the public page into a command list", "using a compact code-themed report that focuses on delivery outcomes", ["Deployment", "GitHub Actions", "Pages", "Release notes", "Scripts", "Static hosting"]),
    "Hilma Shuumbwa": ("minimal-editorial", "Runtime configuration reviewer", "configuration loading, environment awareness, and the checks that help the app start reliably", "explaining runtime configuration without exposing private values", "using a minimal technical report layout that keeps attention on reliability", ["Runtime config", "Expo", "Firebase context", "Diagnostics", "Git", "Documentation"]),
    "Tjatindi Michael Kazundire": ("magazine-feature", "Security rules and access documentation reviewer", "security rules, access notes, and how project records can be protected in a Firebase-backed app", "communicating security work clearly", "using an editorial portfolio layout with concise report sections", ["Security rules", "Access review", "Firebase context", "Documentation", "GitHub", "CSS"]),
}


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def esc(value):
    return str(value or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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


def layout_for(layout_id):
    return next(layout for layout in LAYOUTS if layout["id"] == layout_id)


def is_generic_screenshot(path):
    lowered = path.name.lower()
    return "asset" in lowered or "evidence" in lowered


def discover_screenshots(site):
    screenshot_dir = site / "assets" / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    return [
        file
        for file in sorted(screenshot_dir.iterdir())
        if file.is_file() and file.suffix.lower() in SCREENSHOT_EXTENSIONS and not is_generic_screenshot(file)
    ]


def discover_certificates(portfolio, site):
    cert_dir = site / "assets" / "certificates"
    cert_dir.mkdir(parents=True, exist_ok=True)
    (cert_dir / ".gitkeep").write_text("", encoding="utf-8")
    search_dirs = [
        portfolio / "certificates",
        portfolio / "Certificates",
        portfolio / "docs" / "certificates",
        cert_dir,
    ]
    found = []
    for directory in search_dirs:
        if not directory.exists():
            continue
        for file in sorted(directory.iterdir()):
            if not file.is_file() or file.suffix.lower() not in ASSET_EXTENSIONS:
                continue
            destination = cert_dir / file.name
            if file.resolve() != destination.resolve():
                shutil.copyfile(file, destination)
            if destination not in found:
                found.append(destination)
    return found


def copy_reports(portfolio, site):
    site_docs = site / "docs"
    site_docs.mkdir(parents=True, exist_ok=True)
    linked = []
    for name in ["presentation-guide.pdf", "contribution-report.pdf"]:
        source = portfolio / "docs" / name
        destination = site_docs / name
        if source.exists():
            shutil.copyfile(source, destination)
            linked.append(destination)
    return linked


def report_card(title, description, href, icon):
    return f"""
      <a class="document-card" href="{esc(href)}">
        <span class="doc-icon">{svg_icon(icon)}</span>
        <strong>{esc(title)}</strong>
        <em>{esc(description)}</em>
      </a>"""


def svg_icon(symbol):
    return f"""<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"></circle><text x="12" y="15" text-anchor="middle">{esc(symbol)}</text></svg>"""


def certificates_section(site, certificates, icon):
    if not certificates:
        return ""
    cards = []
    for certificate in certificates:
        rel = certificate.relative_to(site).as_posix()
        title = certificate.stem.replace("-", " ").replace("_", " ").title()
        if certificate.suffix.lower() == ".pdf":
            cards.append(
                f"""<a class="certificate-card pdf-card" href="{esc(rel)}"><span>{svg_icon(icon)}</span><strong>{esc(title)}</strong><em>Open Certificate</em></a>"""
            )
        else:
            cards.append(
                f"""<a class="certificate-card image-card" href="{esc(rel)}"><img src="{esc(rel)}" alt="{esc(title)} certificate"><strong>{esc(title)}</strong></a>"""
            )
    return f"""
    <section class="section certificate-section" id="certificates">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Certificates</h2></div>
      <div class="certificate-grid">{''.join(cards)}</div>
    </section>"""


def evidence_section(site, screenshots, icon):
    if not screenshots:
        return ""
    cards = []
    for screenshot in screenshots:
        rel = screenshot.relative_to(site).as_posix()
        title = screenshot.stem.replace("-", " ").replace("_", " ").title()
        cards.append(
            f"""<article class="evidence-card"><img src="{esc(rel)}" alt="{esc(title)}"><h3>{esc(title)}</h3></article>"""
        )
    return f"""
    <section class="section evidence-section" id="work-record">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Project Evidence</h2></div>
      <div class="evidence-grid">{''.join(cards)}</div>
    </section>"""


def layout_blocks(layout_id, item, assignment, layout, reports_html, cert_html, evidence_html):
    student = item["studentName"]
    username = item["githubUsername"]
    repo = item["repoName"]
    repo_url = f"https://github.com/{username}/{repo}"
    live_url = f"https://{username}.github.io/{repo}/"
    icon = layout["icon"]
    skills = "".join(f"<li>{esc(skill)}</li>" for skill in assignment["skills"])
    project_text = "SiteSpy is an Expo React Native and Firebase construction support app for project records, wall measurements, material estimates, and report-ready summaries."
    contribution = f"My contribution focused on {assignment['contribution']}."
    challenge = f"The main challenge was {assignment['challenge']}. The solution was {assignment['solution']}."
    reflection = "I strengthened my understanding of GitHub workflow, static portfolio deployment, project communication, and how focused technical work contributes to a complete app."

    common_sections = f"""
    <section class="section overview" id="overview">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Project Overview</h2></div>
      <p>{esc(project_text)}</p>
    </section>
    <section class="section contribution" id="contribution">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>My Contribution</h2></div>
      <p>{esc(contribution)}</p>
    </section>
    <section class="section work-area">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Key Work Area</h2></div>
      <p>This portfolio presents a focused project area, practical learning, and the public report resources connected to my SiteSpy role.</p>
    </section>
    <section class="section skills" id="skills">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Skills and Tools</h2></div>
      <ul class="skill-list">{skills}</ul>
    </section>
    <section class="section challenge">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Challenge and Solution</h2></div>
      <p>{esc(challenge)}</p>
    </section>
    <section class="section reflection">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Learning Reflection</h2></div>
      <p>{esc(reflection)}</p>
    </section>
    {cert_html}
    {evidence_html}
    <section class="section reports" id="reports">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Reports</h2></div>
      <div class="document-grid">{reports_html}</div>
    </section>
    <section class="section links" id="links">
      <div class="section-title"><span>{svg_icon(icon)}</span><h2>Repository and Live Links</h2></div>
      <div class="link-row"><a href="{esc(repo_url)}">Repository</a><a href="{esc(live_url)}">Live Project</a></div>
    </section>"""

    if layout_id == "sidebar-profile":
        return f"""
  <div class="layout-shell sidebar-shell">
    <header class="profile-rail">
      <p class="eyebrow">{esc(layout['label'])}</p>
      <h1>{esc(student)}</h1>
      <p class="role">{esc(assignment['role'])}</p>
      <div class="profile-stack"><span>{esc(username)}</span><span>SiteSpy</span><span>{esc(repo)}</span></div>
    </header>
    <main>{common_sections}</main>
  </div>"""
    if layout_id == "terminal-console":
        return f"""
  <main class="terminal-shell">
    <header class="terminal-hero"><div class="terminal-bar"><span></span><span></span><span></span></div><p class="eyebrow">{esc(layout['label'])}</p><h1>{esc(student)}</h1><p class="role">$ {esc(assignment['role'])}</p></header>
    <div class="console-grid">{common_sections}</div>
  </main>"""
    if layout_id == "mobile-case-study":
        return f"""
  <main class="mobile-shell">
    <header class="phone-hero"><div class="phone-frame"><span>SiteSpy</span><h1>{esc(student)}</h1><p>{esc(assignment['role'])}</p></div><div><p class="eyebrow">{esc(layout['label'])}</p><h2>Mobile project showcase</h2><p>{esc(contribution)}</p></div></header>
    {common_sections}
  </main>"""
    if layout_id == "academic-report":
        return f"""
  <main class="report-shell">
    <header class="report-cover"><p class="eyebrow">{esc(layout['label'])}</p><h1>{esc(student)}</h1><p>{esc(assignment['role'])}</p></header>
    <div class="report-columns">{common_sections}</div>
  </main>"""
    if layout_id == "presentation-deck":
        return f"""
  <main class="deck-shell">
    <header class="slide hero-slide"><p class="eyebrow">{esc(layout['label'])}</p><h1>{esc(student)}</h1><p>{esc(assignment['role'])}</p></header>
    <div class="slide-grid">{common_sections}</div>
  </main>"""
    if layout_id == "magazine-feature":
        return f"""
  <main class="magazine-shell">
    <header class="magazine-cover"><p class="eyebrow">{esc(layout['label'])}</p><h1>{esc(student)}</h1><p class="role">{esc(assignment['role'])}</p><p>{esc(contribution)}</p></header>
    <div class="magazine-flow">{common_sections}</div>
  </main>"""
    if layout_id == "minimal-editorial":
        return f"""
  <main class="editorial-shell">
    <header class="editorial-hero"><p>{esc(username)}</p><h1>{esc(student)}</h1><h2>{esc(assignment['role'])}</h2></header>
    {common_sections}
  </main>"""
    return f"""
  <main class="showcase-shell">
    <header class="hero">
      <div><p class="eyebrow">{esc(layout['label'])}</p><h1>{esc(student)}</h1><p class="role">{esc(assignment['role'])}</p><p class="lead">{esc(contribution)}</p></div>
      <aside class="hero-panel"><strong>{esc(username)}</strong><span>SiteSpy portfolio</span><span>{esc(repo)}</span><a href="{esc(repo_url)}">Repository</a></aside>
    </header>
    <div class="content-grid">{common_sections}</div>
  </main>"""


def build_html(item, layout, assignment, reports, certificates, screenshots):
    student = item["studentName"]
    username = item["githubUsername"]
    repo = item["repoName"]
    repo_url = f"https://github.com/{username}/{repo}"
    live_url = f"https://{username}.github.io/{repo}/"
    reports_html = ""
    if any(path.name == "presentation-guide.pdf" for path in reports):
        reports_html += report_card("Presentation Guide", "A concise preparation report for the project showcase.", "docs/presentation-guide.pdf", layout["icon"])
    if any(path.name == "contribution-report.pdf" for path in reports):
        reports_html += report_card("Contribution Report", "A summary of project contribution, tools, challenges, and learning.", "docs/contribution-report.pdf", layout["icon"])
    cert_html = certificates_section(Path(item["portfolioPath"]) / "site", certificates, layout["icon"])
    evidence_html = evidence_section(Path(item["portfolioPath"]) / "site", screenshots, layout["icon"])
    body = layout_blocks(layout["id"], item, assignment, layout, reports_html, cert_html, evidence_html)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(student)} | SiteSpy Portfolio</title>
  <meta name="description" content="{esc(student)} SiteSpy project showcase.">
  <link rel="stylesheet" href="styles.css">
</head>
<body data-layout="{esc(layout['id'])}">
  <nav class="site-nav" aria-label="Portfolio navigation">
    <a class="nav-brand" href="#top">{esc(student)}</a>
    <div>
      <a href="#overview">Overview</a>
      <a href="#contribution">Contribution</a>
      <a href="#skills">Skills</a>
      <a href="#reports">Reports</a>
    </div>
  </nav>
  <div id="top"></div>
  {body}
  <footer class="site-footer">
    <span>{esc(student)}</span>
    <span>{esc(username)}</span>
    <a href="{esc(repo_url)}">Repository</a>
    <a href="{esc(live_url)}">Live Project</a>
  </footer>
  <script src="script.js" defer></script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def build_css(layout):
    layout_id = layout["id"]
    bg = layout["bg"]
    surface = layout["surface"]
    ink = layout["ink"]
    muted = layout["muted"]
    accent = layout["accent"]
    accent2 = layout["accent2"]
    font = layout["font"]
    shape = layout["shape"]
    if layout_id == "terminal-console":
        extra = ".section{border-left:3px solid var(--accent)} .section-title h2::before{content:'./ ';color:var(--accent2)}"
    elif layout_id == "github-contribution":
        extra = """.hero{grid-template-columns:1fr;gap:12px}.hero>div{border-left:8px solid var(--accent);background:var(--surface);padding:24px;border-radius:var(--shape)}.hero-panel{grid-template-columns:repeat(4,1fr);display:grid}.content-grid{display:grid;grid-template-columns:160px 1fr;gap:0 18px}.section{grid-column:2;border-radius:8px;position:relative;margin-bottom:10px}.section::before{content:"";position:absolute;left:-26px;top:24px;width:14px;height:14px;border-radius:4px;background:var(--accent);box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 18%,transparent)}.content-grid::before{content:"";grid-column:1;grid-row:1 / span 8;border-right:3px solid color-mix(in srgb,var(--accent) 28%,transparent)}"""
    elif layout_id == "minimal-editorial":
        extra = ".section{box-shadow:none;border-width:0 0 1px 0;border-radius:0}.editorial-hero{text-align:left;border-bottom:3px solid var(--ink)}"
    elif layout_id == "presentation-deck":
        extra = ".section{min-height:220px}.slide-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.hero-slide{border:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}"
    elif layout_id == "sidebar-profile":
        extra = ".site-nav{margin-left:320px}.profile-rail{position:sticky;top:76px;align-self:start}.layout-shell{grid-template-columns:300px 1fr}"
    elif layout_id == "mobile-case-study":
        extra = ".phone-frame{max-width:280px;border:10px solid var(--ink);border-radius:32px;padding:28px 18px;background:var(--surface)}.phone-hero{display:grid;grid-template-columns:320px 1fr;gap:28px;align-items:center}"
    elif layout_id == "academic-report":
        extra = ".report-cover{border-bottom:4px double var(--accent);padding-bottom:24px}.report-columns{column-count:2;column-gap:26px}.section{break-inside:avoid}"
    elif layout_id == "magazine-feature":
        extra = ".magazine-cover h1{font-size:clamp(42px,8vw,82px)}.magazine-flow{display:block}.section{margin-bottom:18px}.section:nth-child(odd){margin-left:8vw}"
    elif layout_id == "data-chart-cards":
        extra = """.hero{grid-template-columns:.95fr 1.05fr}.hero>div{padding:26px;background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 13%,var(--surface)),var(--surface));border-radius:var(--shape);border:1px solid color-mix(in srgb,var(--accent) 22%,transparent)}.hero-panel{display:grid;grid-template-columns:repeat(2,1fr)}.hero-panel span{padding:10px;border-radius:8px;background:color-mix(in srgb,var(--accent2) 9%,var(--surface))}.content-grid{display:grid;grid-template-columns:1.1fr .9fr .9fr;gap:14px}.section{box-shadow:none}.overview{grid-column:span 3;border-top:8px solid var(--accent)}.contribution,.challenge{grid-column:span 2}.skills .skill-list{display:grid;grid-template-columns:1fr}.reports,.links{grid-column:span 3}.section-title span{border-radius:8px}"""
    elif layout_id == "analytics-dashboard":
        extra = """.hero{grid-template-columns:1fr}.hero-panel{display:grid;grid-template-columns:repeat(4,1fr)}.content-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.overview{grid-column:span 2;grid-row:span 2}.contribution{grid-column:span 2}.skills,.challenge,.reflection,.reports,.links{grid-column:span 2}.section{border:0;box-shadow:0 12px 34px rgba(79,70,229,.12)}.section-title{border-bottom:1px solid color-mix(in srgb,var(--accent) 16%,transparent);padding-bottom:9px}.section-title span{border-radius:6px}"""
    elif layout_id == "modern-saas":
        extra = """.hero{grid-template-columns:1.2fr .8fr;min-height:360px}.hero>div{align-self:center}.hero-panel{border:0;background:linear-gradient(160deg,color-mix(in srgb,var(--accent) 18%,var(--surface)),color-mix(in srgb,var(--accent2) 18%,var(--surface)));transform:rotate(1deg)}.content-grid{display:block}.section{display:grid;grid-template-columns:260px 1fr;gap:18px;align-items:start;margin-bottom:12px;border-left:6px solid var(--accent)}.section-title{margin:0}.reports .document-grid,.links .link-row{grid-column:2}.skills .skill-list{grid-column:2}.section-title span{border-radius:8px}"""
    elif layout_id == "product-landing":
        extra = """.hero{grid-template-columns:1fr;max-width:900px;margin-left:auto;margin-right:auto;text-align:center}.hero-panel{display:flex;justify-content:center;gap:16px;box-shadow:none}.content-grid{display:block;max-width:980px;margin-left:auto;margin-right:auto}.section{display:grid;grid-template-columns:80px 1fr;gap:18px;border:0;border-bottom:1px solid color-mix(in srgb,var(--accent) 18%,transparent);box-shadow:none;border-radius:0}.section-title{display:block}.section-title span{margin-bottom:8px}.skills .skill-list,.reports .document-grid,.links .link-row{grid-column:2}.overview{background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 10%,var(--surface)),var(--surface));border-radius:18px;border-bottom:0}"""
    elif layout_id == "documentation-style":
        extra = """.hero{grid-template-columns:320px 1fr}.hero-panel{order:-1;position:sticky;top:18px;align-self:start}.content-grid{display:grid;grid-template-columns:280px 1fr;gap:16px}.content-grid::before{content:"Contents\\A 01 Overview\\A 02 Contribution\\A 03 Skills\\A 04 Reports";white-space:pre-line;grid-column:1;grid-row:1 / span 8;background:var(--surface);border:1px solid color-mix(in srgb,var(--accent) 18%,transparent);border-radius:var(--shape);padding:20px;color:var(--muted);font-weight:700}.section{grid-column:2;box-shadow:none;border-radius:4px}.section-title span{border-radius:4px}"""
    elif layout_id == "engineering-blueprint":
        extra = """body{background-image:linear-gradient(rgba(3,105,161,.10) 1px,transparent 1px),linear-gradient(90deg,rgba(3,105,161,.10) 1px,transparent 1px);background-size:28px 28px}.hero{grid-template-columns:1fr;border:2px solid var(--accent);padding:18px}.hero-panel{display:flex;justify-content:space-between;box-shadow:none;border-style:dashed}.content-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.section{border-style:dashed;box-shadow:none}.overview,.reports{grid-column:span 2}.section-title span{border-radius:0}"""
    elif layout_id == "security-interface":
        extra = """.hero{grid-template-columns:1fr 1fr}.hero>div,.hero-panel,.section{background:linear-gradient(180deg,color-mix(in srgb,var(--surface) 96%,#000),var(--surface));box-shadow:0 0 0 1px rgba(239,68,68,.08),0 18px 40px rgba(0,0,0,.24)}.content-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.overview,.reports{grid-column:span 2}.section-title span{background:transparent;border:1px solid var(--accent);color:var(--accent);border-radius:8px}.skill-list li{background:rgba(239,68,68,.08)}"""
    elif layout_id == "soft-glass":
        extra = """.hero{grid-template-columns:.9fr 1.1fr}.hero>div,.hero-panel,.section{backdrop-filter:blur(18px);box-shadow:0 20px 60px rgba(99,102,241,.12)}.content-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}.overview,.contribution{grid-column:span 3}.skills{grid-column:span 2}.challenge,.reflection{grid-column:span 2}.reports,.links{grid-column:span 3}.section-title span{background:linear-gradient(135deg,var(--accent),var(--accent2))}"""
    else:
        extra = ".content-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.overview,.contribution,.reports{grid-column:span 2}.skills,.challenge,.reflection,.links{grid-column:span 1}"
    return f""":root {{
  --bg: {bg};
  --surface: {surface};
  --ink: {ink};
  --muted: {muted};
  --accent: {accent};
  --accent2: {accent2};
  --shape: {shape};
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background: radial-gradient(circle at 12% 8%, color-mix(in srgb, var(--accent) 13%, transparent), transparent 28%), var(--bg);
  font-family: {font};
  line-height: 1.55;
}}
a {{ color: inherit; }}
.site-nav {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
}}
.nav-brand {{ text-decoration: none; font-weight: 850; letter-spacing: .01em; }}
.site-nav div {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.site-nav div a {{ text-decoration: none; color: var(--muted); font-size: 14px; padding: 7px 10px; border-radius: var(--shape); }}
.site-nav div a:hover {{ background: color-mix(in srgb, var(--accent) 12%, transparent); color: var(--ink); }}
.showcase-shell,.terminal-shell,.mobile-shell,.report-shell,.deck-shell,.magazine-shell,.editorial-shell,.layout-shell {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 34px 20px 52px;
}}
.hero {{
  display: grid;
  grid-template-columns: minmax(0,1.18fr) minmax(260px,.82fr);
  gap: 22px;
  align-items: stretch;
  margin-bottom: 20px;
}}
.hero-panel,.profile-rail,.terminal-hero,.phone-hero,.report-cover,.magazine-cover,.editorial-hero,.hero-slide {{
  background: var(--surface);
  border: 1px solid color-mix(in srgb, var(--accent) 24%, transparent);
  border-radius: var(--shape);
  padding: 24px;
  box-shadow: 0 18px 48px rgba(0,0,0,.10);
}}
.hero-panel {{ display: grid; gap: 10px; align-content: center; }}
.hero-panel strong {{ font-size: 24px; color: var(--accent); overflow-wrap:anywhere; }}
.hero-panel a {{ color: var(--accent2); font-weight: 800; }}
.layout-shell {{ display: grid; gap: 22px; }}
.eyebrow {{ color: var(--accent); margin: 0 0 10px; text-transform: uppercase; font-size: 12px; font-weight: 850; letter-spacing: .09em; }}
h1 {{ margin: 0; font-size: clamp(30px, 5.6vw, 58px); line-height: 1.03; letter-spacing: 0; }}
h2 {{ margin: 0; font-size: clamp(22px, 3vw, 31px); line-height: 1.12; }}
h3 {{ margin: 0; font-size: 17px; }}
.role,.lead {{ color: var(--muted); font-size: 17px; max-width: 720px; }}
.profile-stack {{ display: grid; gap: 8px; margin-top: 18px; }}
.profile-stack span,.skill-list li,.link-row a,.document-card,.certificate-card {{
  border: 1px solid color-mix(in srgb, var(--accent) 22%, transparent);
  background: color-mix(in srgb, var(--surface) 84%, transparent);
  border-radius: var(--shape);
}}
.content-grid,.console-grid,.report-columns,.magazine-flow {{ margin-top: 18px; }}
.console-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.section {{
  background: var(--surface);
  border: 1px solid color-mix(in srgb, var(--accent) 18%, transparent);
  border-radius: var(--shape);
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 12px 30px rgba(0,0,0,.07);
}}
.section-title {{ display: flex; gap: 10px; align-items: center; margin-bottom: 10px; }}
.section-title span {{ display: inline-flex; width: 28px; height: 28px; align-items: center; justify-content: center; color: var(--surface); background: var(--accent); border-radius: 50%; font-weight: 900; }}
.section-title svg,.doc-icon svg,.certificate-card svg {{ width: 20px; height: 20px; display: block; }}
.section-title svg circle,.doc-icon svg circle,.certificate-card svg circle {{ fill: transparent; }}
.section-title svg text,.doc-icon svg text,.certificate-card svg text {{ fill: currentColor; font-size: 10px; font-family: Arial, sans-serif; font-weight: 900; }}
.section p {{ margin: 0; color: var(--muted); }}
.skill-list {{ list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 8px; }}
.skill-list li {{ padding: 8px 10px; color: var(--ink); font-weight: 750; }}
.document-grid,.certificate-grid,.evidence-grid,.link-row {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 12px; }}
.document-card,.certificate-card,.link-row a {{
  text-decoration: none;
  padding: 14px;
  display: grid;
  gap: 6px;
}}
.document-card strong,.certificate-card strong {{ color: var(--accent); }}
.document-card em,.certificate-card em {{ color: var(--muted); font-style: normal; font-size: 14px; }}
.doc-icon {{ width: 30px; height: 30px; display: inline-flex; align-items: center; justify-content: center; color: var(--surface); background: var(--accent2); border-radius: 50%; }}
.certificate-card img,.evidence-card img {{ width: 100%; height: 170px; object-fit: cover; display: block; border-radius: calc(var(--shape) - 2px); }}
.evidence-card {{ background: var(--surface); border-radius: var(--shape); overflow: hidden; border: 1px solid color-mix(in srgb,var(--accent) 18%,transparent); }}
.evidence-card h3 {{ padding: 12px; }}
.terminal-bar {{ display:flex; gap:7px; margin-bottom:16px; }}
.terminal-bar span {{ width:11px; height:11px; border-radius:50%; background:var(--accent); }}
.site-footer {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 22px 20px 34px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
  color: var(--muted);
  border-top: 1px solid color-mix(in srgb,var(--accent) 18%,transparent);
}}
.site-footer a {{ color: var(--accent); font-weight: 800; text-decoration: none; }}
{extra}
@media (max-width: 760px) {{
  .site-nav,.site-footer {{ align-items: flex-start; flex-direction: column; }}
  .site-nav {{ margin-left: auto; }}
  .hero,.layout-shell,.phone-hero,.console-grid,.content-grid,.slide-grid,.report-columns {{
    display: grid;
    grid-template-columns: 1fr;
    column-count: 1;
  }}
  .hero-panel {{ display: grid !important; grid-template-columns: 1fr !important; transform: none !important; }}
  .content-grid::before {{ display: none !important; }}
  .section {{ display: block !important; grid-column: auto !important; grid-row: auto !important; }}
  .reports .document-grid,.links .link-row,.skills .skill-list {{ grid-column: auto !important; }}
  .document-grid,.certificate-grid,.evidence-grid,.link-row {{ grid-template-columns: 1fr !important; }}
  .section,.hero-panel,.profile-rail,.terminal-hero,.phone-hero,.report-cover,.magazine-cover,.editorial-hero,.hero-slide {{ padding: 16px; }}
  .profile-rail {{ position: static; }}
  .overview,.contribution,.reports,.skills,.challenge,.reflection,.links {{ grid-column: auto; }}
  h1 {{ font-size: clamp(30px, 10vw, 44px); }}
}}
"""


def build_script():
    return """document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
"""


def main():
    rows = []
    for item in active_items():
        student = item["studentName"]
        layout_id, role, contribution, challenge, solution, skills = ASSIGNMENTS[student]
        layout = layout_for(layout_id)
        assignment = {
            "role": role,
            "contribution": contribution,
            "challenge": challenge,
            "solution": solution,
            "skills": skills,
        }
        portfolio = Path(item["portfolioPath"])
        site = portfolio / "site"
        site.mkdir(parents=True, exist_ok=True)

        screenshots = discover_screenshots(site)
        certificates = discover_certificates(portfolio, site)
        reports = copy_reports(portfolio, site)

        (site / "index.html").write_text(build_html(item, layout, assignment, reports, certificates, screenshots), encoding="utf-8")
        (site / "styles.css").write_text(build_css(layout), encoding="utf-8")
        (site / "script.js").write_text(build_script(), encoding="utf-8")
        (site / "evidence.json").write_text(json.dumps([file.name for file in screenshots], indent=2) + "\n", encoding="utf-8")
        (site / "certificates.json").write_text(json.dumps([file.name for file in certificates], indent=2) + "\n", encoding="utf-8")

        repo = f"{item['githubUsername']}/{item['repoName']}"
        live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
        row = {
            "student": student,
            "githubUsername": item["githubUsername"],
            "repo": repo,
            "liveUrl": live_url,
            "layoutFamily": layout["label"],
            "layoutId": layout["id"],
            "themeColors": {
                "background": layout["bg"],
                "surface": layout["surface"],
                "ink": layout["ink"],
                "accent": layout["accent"],
                "accent2": layout["accent2"],
            },
            "certificatesFound": len(certificates),
            "certificatesDisplayed": len(certificates) > 0,
            "evidenceFound": len(screenshots),
            "evidenceDisplayed": len(screenshots) > 0,
            "reportsLinked": [path.name for path in reports],
            "filesUpdated": [
                "site/index.html",
                "site/styles.css",
                "site/script.js",
                "site/evidence.json",
                "site/certificates.json",
                "site/docs/presentation-guide.pdf",
                "site/docs/contribution-report.pdf",
                "site/assets/certificates/",
            ],
        }
        rows.append(row)
        print(f"{student}: {layout['label']} | certificates={len(certificates)} | evidence={len(screenshots)}")

    report = {
        "generatedAt": datetime.now().isoformat(),
        "portfoliosProcessed": len(rows),
        "distinctLayoutFamilies": len({row["layoutId"] for row in rows}),
        "skipped": ["Penny", "Ndaitavela", "Nambuli"],
        "manualScreenshotWorkLocation": "portfolio-batch/STUDENT_SCREENSHOT_CHECKLIST.md",
        "portfolios": rows,
    }
    (ROOT / "portfolio-batch" / "portfolio-visual-upgrade-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Portfolio Visual Upgrade Report",
        "",
        f"- Portfolios processed: {len(rows)}",
        f"- Distinct layout families: {report['distinctLayoutFamilies']}",
        "- Public pages are polished showcase pages, not student instruction pages.",
        "- Certificate sections display only when certificate files exist.",
        "- Evidence sections display only when real student-specific screenshots exist.",
        "",
        "| Student | GitHub | Repo | Layout | Certificates | Evidence | Reports |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        reports_text = ", ".join(row["reportsLinked"]) or "None"
        lines.append(
            f"| {row['student']} | {row['githubUsername']} | {row['repo']} | {row['layoutFamily']} | {row['certificatesFound']} | {row['evidenceFound']} | {reports_text} |"
        )
    lines.extend(["", "Remaining manual screenshot work: `portfolio-batch/STUDENT_SCREENSHOT_CHECKLIST.md`.", ""])
    (ROOT / "portfolio-batch" / "portfolio-visual-upgrade-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Processed {len(rows)} active portfolios")
    print(f"Distinct layout families: {report['distinctLayoutFamilies']}")


if __name__ == "__main__":
    main()
