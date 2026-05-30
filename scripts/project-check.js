const fs = require("node:fs");
const path = require("node:path");

const root = process.cwd();
const requiredPaths = [
  "package.json",
  "app.json",
  "app.config.js",
  "eas.json",
  "firebase.json",
  "firestore.rules",
  "storage.rules",
  "firestore.indexes.json",
  "src/navigation",
  "src/screens",
  "src/services",
  "src/utils",
  "README.md"
];

const blockedPatterns = [
  /(^|[\\/])\.env($|\.)/i,
  /collaborators\.txt$/i,
  /thatfile\.txt$/i,
  /docs[\\/]collaborators\.json$/i,
  /(^|[\\/]).*credentials.*\.(json|txt|env)$/i,
  /(^|[\\/]).*secret.*\.(json|txt|env)$/i,
  /(^|[\\/]).*token.*\.(json|txt|env)$/i,
  /(^|[\\/]).*pat.*\.(json|txt|env)$/i,
  /express/i
];

const allowedFiles = new Set([".env.example"]);

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if ([".git", "node_modules", ".expo"].includes(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(fullPath, files);
    } else {
      files.push(path.relative(root, fullPath));
    }
  }
  return files;
}

const missing = requiredPaths.filter((item) => !fs.existsSync(path.join(root, item)));
if (missing.length) {
  console.error(`Missing required project files:\n${missing.join("\n")}`);
  process.exit(1);
}

function trackedFiles() {
  try {
    const output = require("node:child_process").execFileSync("git", ["ls-files"], { encoding: "utf8" });
    return output.split(/\r?\n/).filter(Boolean);
  } catch {
    return walk(root);
  }
}

const blockedFiles = trackedFiles().filter((file) => {
  const normalized = file.replace(/\\/g, "/");
  return !allowedFiles.has(normalized) && blockedPatterns.some((pattern) => pattern.test(normalized));
});
if (blockedFiles.length) {
  console.error(`Blocked private or wrong-stack files:\n${blockedFiles.join("\n")}`);
  process.exit(1);
}

const staged = (() => {
  try {
    const output = require("node:child_process").execFileSync("git", ["diff", "--cached", "--name-only"], { encoding: "utf8" });
    return output.split(/\r?\n/).filter(Boolean);
  } catch {
    return [];
  }
})();

const blockedStaged = staged.filter((file) => {
  const normalized = file.replace(/\\/g, "/");
  return !allowedFiles.has(normalized) && blockedPatterns.some((pattern) => pattern.test(normalized));
});

if (blockedStaged.length) {
  console.error(`Blocked staged private files:\n${blockedStaged.join("\n")}`);
  process.exit(1);
}

console.log("SiteSpy project check passed.");
