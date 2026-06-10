const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..", "..");
const configPath = path.join(root, "portfolio-batch", "deployment-config.active.json");
const outputRoot = path.join(root, "portfolio-batch", "visual-qa");

function slugify(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function activeItems() {
  const config = JSON.parse(fs.readFileSync(configPath, "utf8").replace(/^\uFEFF/, ""));
  return config.filter((item) => {
    const name = String(item.studentName || "").trim().toLowerCase();
    const username = String(item.githubUsername || "").trim();
    if (name === "penny" || name === "ndaitavela") return false;
    if (name.startsWith("nambuli") || username === "studentgithub") return false;
    return true;
  });
}

async function launchBrowser() {
  for (const channel of ["msedge", "chrome"]) {
    try {
      return await chromium.launch({ channel, headless: true });
    } catch (error) {
      // Try the next local browser channel before falling back.
    }
  }
  return chromium.launch({ headless: true });
}

function imageTag(student, slug, file, label) {
  return `<figure>
    <figcaption>${student} - ${label}</figcaption>
    <img src="./${slug}/${file}" alt="${student} ${label} screenshot">
  </figure>`;
}

async function captureViewport(page, url, outDir, file, width, height) {
  await page.setViewportSize({ width, height });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(outDir, file), fullPage: false });
}

async function main() {
  const items = activeItems();
  fs.mkdirSync(outputRoot, { recursive: true });

  const browser = await launchBrowser();
  const results = [];

  try {
    for (const item of items) {
      const slug = slugify(item.studentName);
      const portfolioDir = path.resolve(item.portfolioPath);
      const siteIndex = path.join(portfolioDir, "site", "index.html");
      const outDir = path.join(outputRoot, slug);
      fs.mkdirSync(outDir, { recursive: true });

      const url = pathToFileURL(siteIndex).href;
      const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
      await captureViewport(page, url, outDir, "desktop.png", 1440, 1000);
      await captureViewport(page, url, outDir, "tablet.png", 768, 1000);
      await captureViewport(page, url, outDir, "mobile.png", 390, 900);
      await page.close();

      results.push({
        studentName: item.studentName,
        githubUsername: item.githubUsername,
        repoName: item.repoName,
        slug,
        desktop: `portfolio-batch/visual-qa/${slug}/desktop.png`,
        tablet: `portfolio-batch/visual-qa/${slug}/tablet.png`,
        mobile: `portfolio-batch/visual-qa/${slug}/mobile.png`,
      });

      console.log(`[visual-qa] captured ${item.studentName}`);
    }
  } finally {
    await browser.close();
  }

  const gallery = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SiteSpy Portfolio Visual QA</title>
  <style>
    body { margin: 0; font-family: Segoe UI, Arial, sans-serif; background: #111827; color: #f8fafc; }
    header { padding: 24px; border-bottom: 1px solid #374151; position: sticky; top: 0; background: rgba(17,24,39,.94); backdrop-filter: blur(10px); z-index: 2; }
    h1 { margin: 0; font-size: 28px; }
    p { color: #cbd5e1; }
    main { padding: 18px; display: grid; gap: 20px; }
    section { background: #1f2937; border: 1px solid #374151; border-radius: 10px; padding: 14px; }
    h2 { margin: 0 0 12px; font-size: 18px; }
    .shots { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(260px, .75fr) minmax(220px, .55fr); gap: 12px; align-items: start; }
    figure { margin: 0; background: #0f172a; border: 1px solid #334155; border-radius: 8px; overflow: hidden; }
    figcaption { padding: 8px 10px; font-size: 13px; color: #cbd5e1; border-bottom: 1px solid #334155; }
    img { display: block; width: 100%; height: auto; }
    @media (max-width: 900px) { .shots { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <header>
    <h1>SiteSpy Portfolio Visual QA</h1>
    <p>${results.length} active portfolios. Desktop viewport: 1440x1000. Tablet viewport: 768x1000. Mobile viewport: 390x900.</p>
  </header>
  <main>
    ${results
      .map(
        (result) => `<section>
      <h2>${result.studentName} <small>(${result.githubUsername}/${result.repoName})</small></h2>
      <div class="shots">
        ${imageTag(result.studentName, result.slug, "desktop.png", "desktop")}
        ${imageTag(result.studentName, result.slug, "tablet.png", "tablet")}
        ${imageTag(result.studentName, result.slug, "mobile.png", "mobile")}
      </div>
    </section>`
      )
      .join("\n")}
  </main>
</body>
</html>
`;

  fs.writeFileSync(path.join(outputRoot, "visual-qa-index.html"), gallery, "utf8");
  fs.writeFileSync(path.join(outputRoot, "visual-qa-results.json"), JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 2), "utf8");
  console.log(`[visual-qa] wrote ${path.join(outputRoot, "visual-qa-index.html")}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
