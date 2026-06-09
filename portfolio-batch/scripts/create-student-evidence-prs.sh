#!/usr/bin/env bash
set +e

CONFIG_PATH="portfolio-batch/deployment-config.active.json"
SINGLE_STUDENT=""
BRANCH_NAME="evidence-update"
COMMIT_MESSAGE="docs: add portfolio evidence notes"
OPEN_PULL_REQUEST=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config-path|-c)
      CONFIG_PATH="$2"
      shift 2
      ;;
    --single-student|-s)
      SINGLE_STUDENT="$2"
      shift 2
      ;;
    --branch-name|-b)
      BRANCH_NAME="$2"
      shift 2
      ;;
    --commit-message|-m)
      COMMIT_MESSAGE="$2"
      shift 2
      ;;
    --open-pull-request)
      OPEN_PULL_REQUEST=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if ! command -v git >/dev/null 2>&1; then
  echo "git is required." >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI is required." >&2
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "python is required to read the JSON config." >&2
  exit 1
fi

if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "Config file not found: $CONFIG_PATH" >&2
  exit 1
fi

redact_text() {
  local text="$1"
  local token="$2"
  if [[ -n "$token" ]]; then
    text="${text//$token/[REDACTED_TOKEN]}"
  fi
  printf '%s' "$text"
}

clean_identity() {
  printf '%s' "$1" | tr '\r\n' '  ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//'
}

write_student_docs() {
  local docs_path="$1"
  local student="$2"
  local github_username="$3"
  local email="$4"
  local repo_name="$5"
  local repo_url="https://github.com/$github_username/$repo_name"
  local live_url="https://$github_username.github.io/$repo_name/"

  mkdir -p "$docs_path"

  cat > "$docs_path/evidence-update-notes.md" <<EOF
# $student Evidence Update Notes

## Student Details

- Name: $student
- Email: $email
- GitHub username: $github_username
- Repository: $repo_url
- Live portfolio: $live_url

## Evidence Purpose

This branch is for adding real screenshots and short notes that connect the portfolio to the student's SiteSpy contribution and GitHub workflow.

## Evidence Rules

- Use only screenshots from the student's own repository, live page, branch, commits, pull request, or SiteSpy work.
- Do not add private credentials.
- Keep screenshots readable and named clearly.
- Add screenshots under \`site/assets/screenshots/\`.

## Suggested Commit Flow

\`\`\`bash
git checkout -b evidence-update
git add docs site/assets/screenshots
git commit -m "docs: add portfolio evidence screenshots"
git push -u origin evidence-update
\`\`\`
EOF

  cat > "$docs_path/screenshot-capture-guide.md" <<EOF
# $student Screenshot Capture Guide

Capture only real evidence. The public portfolio will show screenshots only after they exist in \`site/assets/screenshots/\`.

| Filename | What it should show |
|---|---|
| \`live-homepage.png\` | Live portfolio homepage |
| \`github-repository-main.png\` | GitHub repository main page |
| \`github-actions-success.png\` | GitHub Actions successful deployment run |
| \`commit-history.png\` | Commit history page |
| \`development-branch.png\` | Development branch or contribution branch |
| \`pull-request.png\` | Pull request page once created |
| \`project-app-screen.png\` | Project app screen, if available |
| \`code-contribution.png\` | Code contribution or changed file |
| \`documentation-contribution.png\` | README or documentation contribution |
| \`certificate-or-proof.png\` | Certificate or proof document if available |

After adding files, commit them on the evidence branch and open a pull request to \`main\`.
EOF
}

mapfile -t ITEMS < <(python - "$CONFIG_PATH" "$SINGLE_STUDENT" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
single = sys.argv[2]
data = json.loads(path.read_text(encoding="utf-8-sig"))
for item in data:
    if single and item.get("studentName") != single:
        continue
    fields = [
        item.get("studentName", ""),
        item.get("githubUsername", ""),
        item.get("studentEmail", ""),
        item.get("repoName", ""),
        item.get("portfolioPath", ""),
        item.get("tokenEnvironmentVariable", ""),
    ]
    print("\t".join(str(field).replace("\t", " ") for field in fields))
PY
)

total=0
success=0
skipped=0
failed=0
old_gh_token="${GH_TOKEN-}"

for row in "${ITEMS[@]}"; do
  IFS=$'\t' read -r student github_username email repo_name portfolio_path token_env <<< "$row"
  repo="$github_username/$repo_name"
  total=$((total + 1))

  echo
  echo "Student: $student"
  echo "Repo: $repo"

  if [[ "$student" =~ Penny|Ndaitavela|Nambuli || "$github_username" == "studentgithub" ]]; then
    echo "SKIP: excluded from active evidence automation"
    skipped=$((skipped + 1))
    continue
  fi

  token="${!token_env}"
  if [[ -z "$token" ]]; then
    echo "SKIP: missing token environment variable $token_env"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ ! -d "$portfolio_path" ]]; then
    echo "SKIP: portfolio path missing"
    skipped=$((skipped + 1))
    continue
  fi

  export GH_TOKEN="$token"
  login="$(gh api user --jq .login 2>&1)"
  exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    echo "FAILED: Could not verify token owner: $(redact_text "$login" "$token")"
    failed=$((failed + 1))
    continue
  fi
  login="$(clean_identity "$login")"
  if [[ "$login" != "$github_username" ]]; then
    echo "FAILED: Token belongs to $login, but config expects $github_username. Use the correct student token or fix config."
    failed=$((failed + 1))
    continue
  fi

  [[ -d "$portfolio_path/.git" ]] || git -C "$portfolio_path" init >/dev/null 2>&1
  if [[ $? -ne 0 ]]; then
    echo "FAILED: git init failed in $portfolio_path"
    failed=$((failed + 1))
    continue
  fi

  safe_name="$(clean_identity "$student")"
  [[ -n "$safe_name" ]] || safe_name="$github_username"
  email="$(clean_identity "$email")"
  [[ "$email" == *"@"* ]] || email="$github_username@users.noreply.github.com"

  git -C "$portfolio_path" branch -M main >/dev/null 2>&1
  git -C "$portfolio_path" config user.name "$safe_name" 2>/tmp/sitespy-git-name.err
  if [[ $? -ne 0 ]]; then
    echo "FAILED: Failed to set git user.name in $portfolio_path: $(cat /tmp/sitespy-git-name.err)"
    failed=$((failed + 1))
    continue
  fi
  git -C "$portfolio_path" config user.email "$email" 2>/tmp/sitespy-git-email.err
  if [[ $? -ne 0 ]]; then
    echo "FAILED: Failed to set git user.email in $portfolio_path: $(cat /tmp/sitespy-git-email.err)"
    failed=$((failed + 1))
    continue
  fi

  git -C "$portfolio_path" checkout -B "$BRANCH_NAME" >/dev/null 2>&1
  if [[ $? -ne 0 ]]; then
    echo "FAILED: Failed to create branch $BRANCH_NAME in $portfolio_path"
    failed=$((failed + 1))
    continue
  fi

  write_student_docs "$portfolio_path/docs" "$student" "$github_username" "$email" "$repo_name"
  git -C "$portfolio_path" add docs >/dev/null 2>&1
  if [[ $? -ne 0 ]]; then
    echo "FAILED: git add docs failed in $portfolio_path"
    failed=$((failed + 1))
    continue
  fi

  status="$(git -C "$portfolio_path" status --porcelain)"
  if [[ -n "$status" ]]; then
    commit_output="$(git -C "$portfolio_path" commit -m "$COMMIT_MESSAGE" 2>&1)"
    if [[ $? -ne 0 ]]; then
      echo "FAILED: git commit failed in $portfolio_path: $(redact_text "$commit_output" "$token")"
      failed=$((failed + 1))
      continue
    fi
    echo "[evidence-event] committed=$repo"
  else
    echo "[evidence-event] no_local_changes=$repo"
  fi

  push_url="https://x-access-token:$token@github.com/$repo.git"
  push_output="$(git -C "$portfolio_path" push -u "$push_url" "$BRANCH_NAME" 2>&1)"
  if [[ $? -ne 0 ]]; then
    echo "FAILED: git push failed for $repo: $(redact_text "$push_output" "$token")"
    failed=$((failed + 1))
    continue
  fi
  echo "[evidence-event] pushed=$repo branch=$BRANCH_NAME"

  if [[ $OPEN_PULL_REQUEST -eq 1 ]]; then
    pr_output="$(gh pr create --repo "$repo" --base main --head "$github_username:$BRANCH_NAME" --title "Add portfolio evidence notes" --body "Adds student evidence notes and screenshot capture guidance for the SiteSpy portfolio." 2>&1)"
    if [[ $? -eq 0 ]]; then
      echo "[evidence-event] pull_request_created=$pr_output"
    else
      existing="$(gh pr view "$BRANCH_NAME" --repo "$repo" --json url --jq .url 2>&1)"
      if [[ $? -eq 0 ]]; then
        echo "[evidence-event] pull_request_exists=$existing"
      else
        echo "FAILED: PR creation failed for $repo: $(redact_text "$pr_output" "$token")"
        failed=$((failed + 1))
        continue
      fi
    fi
  fi

  success=$((success + 1))
done

if [[ -n "$old_gh_token" ]]; then
  export GH_TOKEN="$old_gh_token"
else
  unset GH_TOKEN
fi

echo
echo "Evidence PR Summary"
echo "Total: $total"
echo "Success: $success"
echo "Skipped: $skipped"
echo "Failed: $failed"

if [[ $failed -gt 0 ]]; then
  exit 1
fi
