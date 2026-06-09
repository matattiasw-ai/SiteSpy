import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "portfolio-batch" / "deployment-config.active.json"


def esc(value):
    return str(value or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def pdf_escape(value):
    return str(value or "").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap_text(text, width=88):
    words = str(text).split()
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
    for para in paragraphs:
        if isinstance(para, (list, tuple)):
            for item in para:
                lines.extend(wrap_text(f"- {item}"))
        else:
            lines.extend(wrap_text(para))
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


AREAS = {
    "Valentina Correia": ("Data/reporting workspace", "BOQ report summary and cost cards", ["Report data flow", "Cost card review", "Summary presentation"]),
    "Haipumbu Beatha NP": ("Calculation lab", "Estimation formulas and save workflow", ["Calculation review", "Estimate summary", "Save workflow"]),
    "Hamberera Karl PM": ("Database systems board", "Firestore data model documentation and indexes", ["Data model review", "Index planning", "Record structure"]),
    "Hamukwaya NP Petrus": ("Access control console", "Authentication and user profile rules", ["Auth flow review", "Profile rules", "Access control"]),
    "Martha Heita": ("Interface quality desk", "Validation and loading/error feedback", ["Input validation", "Friendly errors", "Loading states"]),
    "Hilda Iita": ("Quality pipeline view", "Project checks, CI, and testing documentation", ["Project checks", "Testing notes", "Workflow review"]),
    "Mathias Jonas": ("Project workflow map", "Project history and detail workflow", ["History screen", "Detail workflow", "Project records"]),
    "Klaudia Kambowe": ("Service operations panel", "Project CRUD service and create/edit screens", ["Project service", "Create flow", "Edit flow"]),
    "Tunacky Kandere": ("Mobile app showcase", "Landing, splash, dashboard navigation shell", ["Navigation shell", "Dashboard cards", "Mobile layout"]),
    "Johannes M Kandjeke": ("Academic computing brief", "Responsive testing documentation and typography/spacing checks", ["Responsive notes", "Spacing review", "Documentation"]),
    "Amalia Mangundu": ("Product settings case study", "Profile, settings, and reusable buttons", ["Profile screen", "Settings screen", "Reusable controls"]),
    "Washington Matattias": ("Release coordination dashboard", "Integration review, package scripts, and final coordination docs", ["Final integration", "Build readiness", "Team coordination"]),
    "Kavakuru Metarere": ("Sign-in flow case study", "Authentication screens and auth service integration", ["Login screen", "Register flow", "Forgot password flow"]),
    "Emilly Ndapuka": ("Field form builder", "Project creation and manual estimate forms", ["Project form", "Manual estimate", "Field validation"]),
    "Shikongo Linus TK": ("Deployment engineering log", "Deployment documentation and EAS readiness", ["EAS profile", "Release notes", "Deployment checklist"]),
    "Hilma Shuumbwa": ("Runtime configuration map", "Firebase configuration and Expo environment loading", ["Firebase config", "Expo config", "Runtime diagnostics"]),
    "Tjatindi Michael Kazundire": ("Security review console", "Security rules and Firebase access documentation", ["Firestore rules", "Storage rules", "Security notes"]),
}

THEMES = [
    ("reporting", "#f5f7fb", "#fff", "#172033", "#596274", "#2563eb", "#0f766e", "Arial, Helvetica, sans-serif"),
    ("calculation", "#fbfaf7", "#fff", "#1f2933", "#667085", "#b45309", "#0e7490", "Georgia, Arial, sans-serif"),
    ("database", "#f2f7f5", "#fff", "#12221c", "#50635b", "#047857", "#334155", "Trebuchet MS, Arial, sans-serif"),
    ("access", "#0f172a", "#172033", "#f8fafc", "#cbd5e1", "#38bdf8", "#f59e0b", "Consolas, Arial, sans-serif"),
    ("quality", "#f8fafc", "#fff", "#1e293b", "#64748b", "#db2777", "#4f46e5", "Segoe UI, Arial, sans-serif"),
    ("pipeline", "#111827", "#1f2937", "#f9fafb", "#d1d5db", "#22c55e", "#60a5fa", "Verdana, Arial, sans-serif"),
    ("workflow", "#f6f3ff", "#fff", "#211735", "#6b5d7b", "#7c3aed", "#0891b2", "Arial, Helvetica, sans-serif"),
    ("operations", "#f1f5f9", "#fff", "#0f172a", "#475569", "#0f766e", "#ea580c", "Tahoma, Arial, sans-serif"),
    ("mobile", "#eef6ff", "#fff", "#102033", "#5a6b7c", "#0284c7", "#16a34a", "Segoe UI, Arial, sans-serif"),
    ("academic", "#fffaf0", "#fff", "#2b2118", "#6f6254", "#92400e", "#2563eb", "Georgia, Times New Roman, serif"),
    ("product", "#f7fbff", "#fff", "#132238", "#536579", "#0ea5e9", "#9333ea", "Arial, Helvetica, sans-serif"),
    ("release", "#0b1220", "#111c2f", "#f8fafc", "#cbd5e1", "#facc15", "#38bdf8", "Arial, Helvetica, sans-serif"),
    ("signin", "#f5f3ff", "#fff", "#1f1b2d", "#625a70", "#6d28d9", "#0d9488", "Segoe UI, Arial, sans-serif"),
    ("forms", "#f7fee7", "#fff", "#17220f", "#59664e", "#65a30d", "#0f766e", "Trebuchet MS, Arial, sans-serif"),
    ("deployment", "#101827", "#182235", "#f8fafc", "#cbd5e1", "#fb923c", "#22d3ee", "Consolas, Arial, sans-serif"),
    ("runtime", "#f0fdfa", "#fff", "#0f2d2a", "#55706b", "#0f766e", "#2563eb", "Arial, Helvetica, sans-serif"),
    ("security", "#111", "#1d1d1d", "#f5f5f5", "#c4c4c4", "#ef4444", "#22c55e", "Consolas, Arial, sans-serif"),
]

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


def public_evidence_files(screenshot_dir):
    if not screenshot_dir.exists():
        return []
    files = []
    for file in screenshot_dir.iterdir():
        if file.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        name = file.name.lower()
        if "asset" in name or "evidence" in name:
            continue
        files.append(file)
    return files


def build_html(item, theme, contribution, focus, evidence_files):
    key, bg, surface, ink, muted, accent, accent2, font = theme
    student = item["studentName"]
    repo = f"{item['githubUsername']}/{item['repoName']}"
    repo_url = f"https://github.com/{repo}"
    live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
    guide_link = "docs/presentation-guide.pdf"
    report_link = "docs/contribution-report.pdf"
    checklist_link = "docs/screenshot-capture-guide.md"
    if evidence_files:
        cards = []
        for file in evidence_files:
            rel = file.relative_to(Path(item["portfolioPath"]) / "site").as_posix()
            title = file.stem.replace("-", " ").title()
            cards.append(f'<article class="evidence-card"><img src="{esc(rel)}" alt="{esc(title)}"><div><h3>{esc(title)}</h3><p>Student-specific evidence file.</p></div></article>')
        evidence_html = '<div class="evidence-grid">' + "\n".join(cards) + "</div>"
    else:
        evidence_html = '<p class="evidence-note">Evidence to be added after manual capture. The checklist explains each required screenshot.</p>'

    panels = [
        ("Project Summary", "SiteSpy is an Expo React Native and Firebase app for construction records, wall measurements, material estimates, and report-ready summaries."),
        ("Personal Contribution", f"{contribution}. Focus areas: {', '.join(focus)}."),
        ("Skills Learned", "GitHub workflow, branches, commits, pull requests, GitHub Actions, Pages deployment, evidence screenshots, and team collaboration."),
        ("Challenges and Solutions", "The main preparation challenge is connecting real evidence to the assigned project area and explaining the work clearly in a short showcase."),
        ("Presentation Prep", "Use the guide and report links to prepare answers about contribution, learning, GitHub workflow, and how the SiteSpy project works."),
    ]
    panel_html = "".join(f'<section class="panel panel-{i}"><h2>{esc(title)}</h2><p>{esc(text)}</p></section>' for i, (title, text) in enumerate(panels))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(student)} | SiteSpy Portfolio</title>
  <meta name="description" content="{esc(student)} SiteSpy portfolio for university assessment.">
  <link rel="stylesheet" href="styles.css">
</head>
<body class="theme-{key}">
  <header class="hero" id="top">
    <nav class="topbar"><a class="brand" href="#top">{esc(student)}</a><div class="links"><a href="#work">Work</a><a href="#evidence">Evidence</a><a href="#guides">Guides</a><a href="{esc(repo_url)}">GitHub</a></div></nav>
    <div class="hero-grid">
      <div class="hero-copy">
        <p class="kicker">{esc(AREAS[student][0])}</p>
        <h1>{esc(student)}</h1>
        <p class="lead">{esc(contribution)}</p>
        <div class="identity"><span>{esc(item['githubUsername'])}</span><span>{esc(item['studentEmail'])}</span><span>{esc(item['repoName'])}</span></div>
      </div>
      <aside class="hero-card"><strong>SiteSpy</strong><span>Static GitHub Pages portfolio</span><span>{esc(key.title())} direction</span><a href="{esc(live_url)}">Live portfolio</a></aside>
    </div>
  </header>
  <main id="work" class="content">
    <section class="summary"><h2>Portfolio Overview</h2><p>This page presents {esc(student)}'s SiteSpy preparation area, practical GitHub workflow, and evidence path for final review.</p><div class="quick-grid"><div><b>Project</b><span>SiteSpy</span></div><div><b>Repository</b><span>{esc(repo)}</span></div><div><b>Theme</b><span>{esc(key.title())}</span></div></div></section>
    <div class="section-stack">{panel_html}</div>
    <section id="evidence" class="evidence-section"><h2>Evidence</h2>{evidence_html}<a class="text-link" href="{checklist_link}">Screenshot checklist</a></section>
    <section id="guides" class="guide-strip"><h2>Presentation Materials</h2><a class="button" href="{guide_link}">Presentation guide</a><a class="button secondary" href="{report_link}">Contribution report</a><a class="button ghost" href="{esc(repo_url)}">GitHub repository</a></section>
  </main>
  <footer><p>{esc(student)} | SiteSpy showcase | {esc(item['githubUsername'])}</p></footer>
  <script src="script.js" defer></script>
</body>
</html>
"""


def build_css(index, theme):
    key, bg, surface, ink, muted, accent, accent2, font = theme
    radius = "999px" if index % 3 == 0 else "8px"
    hero_cols = "1.2fr .8fr" if index % 2 == 0 else ".82fr 1.18fr"
    panel_cols = "1fr 1fr" if index % 3 else "1.15fr .85fr"
    return f""":root {{ --bg:{bg}; --surface:{surface}; --ink:{ink}; --muted:{muted}; --accent:{accent}; --accent2:{accent2}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:{font}; color:var(--ink); background:var(--bg); line-height:1.58; }}
body::before {{ content:""; position:fixed; inset:0; pointer-events:none; background:linear-gradient(135deg, color-mix(in srgb, var(--accent) 12%, transparent), transparent 38%), radial-gradient(circle at 80% 10%, color-mix(in srgb, var(--accent2) 14%, transparent), transparent 32%); z-index:-1; }}
a {{ color:inherit; }}
.topbar {{ max-width:1120px; margin:0 auto; padding:22px 18px; display:flex; justify-content:space-between; gap:16px; align-items:center; }}
.brand {{ font-weight:800; text-decoration:none; letter-spacing:.02em; }}
.links {{ display:flex; flex-wrap:wrap; gap:10px; }}
.links a {{ text-decoration:none; border:1px solid color-mix(in srgb, var(--accent) 35%, transparent); padding:8px 12px; border-radius:{radius}; color:var(--muted); background:color-mix(in srgb, var(--surface) 82%, transparent); }}
.hero {{ min-height:{'86vh' if index % 4 == 0 else '68vh'}; padding-bottom:34px; }}
.hero-grid {{ max-width:1120px; margin:0 auto; padding:44px 18px; display:grid; grid-template-columns:{hero_cols}; gap:{24 + (index % 5)*4}px; align-items:center; }}
.hero-copy {{ {'order:2;' if index % 2 else ''} }}
.kicker {{ color:var(--accent); text-transform:uppercase; font-size:13px; font-weight:800; letter-spacing:.08em; margin:0 0 12px; }}
h1 {{ font-size:clamp({34 + index % 5}px, 7vw, {58 + index % 7}px); line-height:1.02; margin:0 0 16px; max-width:760px; }}
h2 {{ font-size:clamp(24px, 4vw, 34px); margin:0 0 12px; }}
.lead {{ color:var(--muted); font-size:clamp(17px, 2.4vw, 22px); max-width:720px; }}
.identity {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:22px; }}
.identity span {{ border:1px solid color-mix(in srgb, var(--accent) 45%, transparent); background:color-mix(in srgb, var(--surface) 86%, transparent); padding:8px 12px; border-radius:8px; overflow-wrap:anywhere; }}
.hero-card {{ min-height:{220 + (index % 4)*20}px; background:var(--surface); border:1px solid color-mix(in srgb, var(--accent) 35%, transparent); border-radius:{8 + (index % 3)*4}px; box-shadow:0 24px 70px rgba(0,0,0,.14); padding:{24 + (index % 4)*4}px; display:grid; align-content:center; gap:14px; }}
.hero-card strong {{ font-size:28px; color:var(--accent); }}
.hero-card a {{ color:var(--accent2); font-weight:800; }}
.content {{ max-width:1120px; margin:0 auto; padding:22px 18px 54px; }}
.summary {{ background:var(--surface); border-radius:8px; padding:28px; border-left:{6 + index % 4}px solid var(--accent); box-shadow:0 18px 46px rgba(0,0,0,.08); }}
.quick-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin-top:18px; }}
.quick-grid div {{ display:grid; gap:4px; padding:14px; background:color-mix(in srgb, var(--accent) 8%, var(--surface)); border-radius:8px; }}
.quick-grid span {{ color:var(--muted); overflow-wrap:anywhere; }}
.section-stack {{ margin-top:28px; display:grid; grid-template-columns:{panel_cols}; gap:{16 + index % 4 * 3}px; }}
.panel {{ background:var(--surface); padding:{20 + index % 5 * 3}px; border:1px solid color-mix(in srgb, var(--accent) 22%, transparent); border-radius:8px; }}
.panel:nth-child({2 + index % 3}) {{ grid-row:span 2; background:color-mix(in srgb, var(--accent) 10%, var(--surface)); }}
.evidence-section, .guide-strip {{ margin-top:28px; background:var(--surface); border:1px solid color-mix(in srgb, var(--accent2) 28%, transparent); border-radius:8px; padding:26px; }}
.evidence-note {{ color:var(--muted); padding:14px 16px; border-left:4px solid var(--accent2); background:color-mix(in srgb, var(--accent2) 10%, var(--surface)); }}
.evidence-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; }}
.evidence-card {{ background:color-mix(in srgb, var(--accent) 7%, var(--surface)); border-radius:8px; overflow:hidden; }}
.evidence-card img {{ display:block; width:100%; height:180px; object-fit:cover; }}
.evidence-card div {{ padding:14px; }}
.button, .text-link {{ display:inline-flex; margin:8px 8px 0 0; text-decoration:none; color:var(--surface); background:var(--accent); padding:10px 14px; border-radius:{radius}; font-weight:800; }}
.button.secondary {{ background:var(--accent2); }}
.button.ghost, .text-link {{ color:var(--accent); background:transparent; border:1px solid var(--accent); }}
footer {{ padding:28px 18px; text-align:center; color:var(--muted); }}
@media (max-width: 820px) {{ .hero-grid, .section-stack, .quick-grid {{ grid-template-columns:1fr; }} .hero-copy {{ order:initial; }} .topbar {{ align-items:flex-start; flex-direction:column; }} }}
"""


def build_guides(item, contribution):
    student = item["studentName"]
    live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
    presentation = f"""# {student} Presentation Guide

## Portfolio Details

- GitHub username: {item['githubUsername']}
- Repository: {item['repoName']}
- Live portfolio: {live_url}
- Project: SiteSpy

## Project Summary

SiteSpy is a mobile-focused project tool built with Expo React Native and Firebase. It helps users keep project records, review measurements, estimate materials, and prepare clear summaries.

## My Contribution Summary

My assigned preparation area is: {contribution}.

## What I Should Explain

- What SiteSpy does for a user.
- Which part of the project I reviewed or prepared.
- How my portfolio is deployed with GitHub Pages.
- How my evidence screenshots connect to my contribution area.
- What I learned about Git, GitHub, and team collaboration.

## Programming Concepts To Understand

- HTML, CSS, and JavaScript static site structure.
- Git commits and commit messages.
- Branches and pull requests.
- GitHub Actions and GitHub Pages deployment.
- Evidence screenshots and teamwork.

## Q&A Preparation

### What did I contribute?

I prepared and reviewed work around {contribution}.

### What did I learn?

I learned how project work is organised with GitHub, how static portfolios are deployed, and how evidence should be connected to real tasks.

### What challenge did I face?

A key challenge is making sure the portfolio shows only real evidence and explains the contribution clearly.

### What would I improve next?

I would add stronger real evidence screenshots and keep improving the explanation of my assigned project area.
"""
    report = f"""# {student} Contribution Report

## Student Details

- GitHub username: {item['githubUsername']}
- Repository: {item['repoName']}
- Live portfolio: {live_url}
- Project: SiteSpy

## Contribution Area

{contribution}

## SiteSpy Project Context

SiteSpy is a construction support app that keeps project records, helps with wall measurements and material estimation, and prepares information for later review.

## Work I Should Be Able To Explain

- The purpose of my assigned area.
- The files, screens, or documentation connected to my area.
- How the portfolio was deployed.
- How evidence screenshots prove the work.
- How GitHub supports a team workflow.

## Current Evidence Status

Evidence screenshots must be captured manually and added only when they are real and student-specific. Missing evidence is not displayed as a public card.

## Next Steps

- Capture the screenshots listed in the central checklist.
- Add them to the local portfolio folder.
- Create an evidence branch.
- Commit the evidence files.
- Open a pull request if required.
- Confirm the GitHub Pages deployment succeeds.
"""
    screenshot_guide = f"""# {student} Screenshot Capture Guide

Capture only real screenshots from your own repository, live portfolio, project work, and GitHub workflow. Add files to `site/assets/screenshots/` using clear names.

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

- Repository: https://github.com/{item['githubUsername']}/{item['repoName']}
- Live portfolio: {live_url}
"""
    return presentation, report, screenshot_guide


def main():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    active = []
    for item in config:
        name = item["studentName"].strip()
        if name.lower() in {"penny", "ndaitavela"}:
            continue
        if name.lower().startswith("nambuli") or item.get("githubUsername") == "studentgithub":
            continue
        active.append(item)

    checklist = ["# SiteSpy Student Screenshot Checklist", "", "Capture only real evidence. Do not add screenshots that do not belong to the student or repository.", ""]
    rows = []
    pdf_failures = []

    for index, item in enumerate(active):
        student = item["studentName"]
        portfolio = Path(item["portfolioPath"])
        site = portfolio / "site"
        docs = portfolio / "docs"
        screenshots = site / "assets" / "screenshots"
        docs.mkdir(parents=True, exist_ok=True)
        screenshots.mkdir(parents=True, exist_ok=True)

        theme = THEMES[index % len(THEMES)]
        theme_name, contribution, focus = AREAS[student]
        evidence_files = public_evidence_files(screenshots)

        (site / "index.html").write_text(build_html(item, theme, contribution, focus, evidence_files), encoding="utf-8")
        (site / "styles.css").write_text(build_css(index, theme), encoding="utf-8")
        (site / "script.js").write_text(
            "document.querySelectorAll('a[href^=\"#\"]').forEach((link)=>{link.addEventListener('click',(event)=>{const target=document.querySelector(link.getAttribute('href'));if(!target)return;event.preventDefault();target.scrollIntoView({behavior:'smooth',block:'start'});});});\n",
            encoding="utf-8",
        )
        (site / "evidence.json").write_text("[]\n", encoding="utf-8")

        presentation, report, screenshot_guide = build_guides(item, contribution)
        (docs / "presentation-guide.md").write_text(presentation, encoding="utf-8")
        (docs / "contribution-report.md").write_text(report, encoding="utf-8")
        (docs / "screenshot-capture-guide.md").write_text(screenshot_guide, encoding="utf-8")
        try:
            write_simple_pdf(docs / "presentation-guide.pdf", f"{student} Presentation Guide", presentation.split("\n\n"))
            write_simple_pdf(docs / "contribution-report.pdf", f"{student} Contribution Report", report.split("\n\n"))
            pdf_status = "created"
        except Exception as exc:
            pdf_status = f"failed: {exc}"
            pdf_failures.append({"studentName": student, "error": str(exc)})

        repo = f"{item['githubUsername']}/{item['repoName']}"
        repo_url = f"https://github.com/{repo}"
        live_url = f"https://{item['githubUsername']}.github.io/{item['repoName']}/"
        checklist.extend([f"## {student}", "", f"- Portfolio path: `{portfolio}`", f"- Repo URL: {repo_url}", f"- Live URL: {live_url}", f"- Save screenshots in: `{screenshots}`", "", "| Filename | What it should show |", "|---|---|"])
        for filename, description in SCREENSHOTS:
            checklist.append(f"| `{filename}` | {description} |")
        checklist.extend(["", "After adding screenshots:", "", "```bash", "git add site/assets/screenshots docs", 'git commit -m "docs: add portfolio evidence screenshots"', "git push", "```", ""])

        rows.append({
            "studentName": student,
            "portfolioPath": str(portfolio),
            "repo": repo,
            "liveUrl": live_url,
            "theme": theme_name,
            "filesChanged": ["site/index.html", "site/styles.css", "site/script.js", "site/evidence.json", "docs/presentation-guide.md", "docs/contribution-report.md", "docs/screenshot-capture-guide.md", "docs/presentation-guide.pdf", "docs/contribution-report.pdf"],
            "evidenceShown": len(evidence_files),
            "evidenceHidden": len(evidence_files) == 0,
            "pdfStatus": pdf_status,
            "screenshotsStillRequired": [item[0] for item in SCREENSHOTS],
            "deploymentStatus": "pending rerun",
            "nextManualActions": ["Capture real screenshots", "Run evidence PR script", "Verify GitHub Actions deployment"],
        })

    (ROOT / "portfolio-batch" / "STUDENT_SCREENSHOT_CHECKLIST.md").write_text("\n".join(checklist), encoding="utf-8")

    report_data = {
        "generatedAt": datetime.now().isoformat(),
        "portfoliosProcessed": len(rows),
        "skipped": ["Penny", "Ndaitavela", "Nambuli"],
        "scriptsCreated": ["portfolio-batch/scripts/create-student-evidence-prs.ps1", "portfolio-batch/scripts/create-student-evidence-prs.sh"],
        "pdfFailures": pdf_failures,
        "portfolios": rows,
        "nextManualActions": ["Capture real screenshots", "Run student evidence PR automation", "Redeploy after evidence is added"],
    }
    (ROOT / "portfolio-batch" / "portfolio-visual-upgrade-report.json").write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    md = ["# Portfolio Visual Upgrade Report", "", f"- Portfolios processed: {len(rows)}", "- Evidence policy: public pages show real student-specific screenshots only.", "- Deployment status: pending rerun.", "", "## Themes"]
    md.extend(f"- {row['studentName']}: {row['theme']}" for row in rows)
    md.extend(["", "## PDF Status", "- All presentation and contribution PDFs created." if not pdf_failures else "- Some PDFs failed; see JSON report.", "", "## Screenshots Still Required", "See `portfolio-batch/STUDENT_SCREENSHOT_CHECKLIST.md`.", "", "## Next Manual Actions", "- Capture real screenshots.", "- Run student evidence PR automation from each student account.", "- Redeploy after screenshots are committed."])
    (ROOT / "portfolio-batch" / "portfolio-visual-upgrade-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Processed {len(rows)} active portfolios")
    print(f"PDF failures: {len(pdf_failures)}")


if __name__ == "__main__":
    main()
