#!/usr/bin/env bash
set -euo pipefail

COMMIT_MESSAGE="complete personal portfolio showcase"
WATCH=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --portfolio-path) PORTFOLIO_PATH="$2"; shift 2 ;;
    --student-name) STUDENT_NAME="$2"; shift 2 ;;
    --github-username) GITHUB_USERNAME="$2"; shift 2 ;;
    --student-email) STUDENT_EMAIL="$2"; shift 2 ;;
    --repo-name) REPO_NAME="$2"; shift 2 ;;
    --token-env) TOKEN_ENV="$2"; shift 2 ;;
    --commit-message) COMMIT_MESSAGE="$2"; shift 2 ;;
    --watch) WATCH=1; shift ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

: "${PORTFOLIO_PATH:?Missing --portfolio-path}"
: "${STUDENT_NAME:?Missing --student-name}"
: "${GITHUB_USERNAME:?Missing --github-username}"
: "${STUDENT_EMAIL:?Missing --student-email}"
: "${REPO_NAME:?Missing --repo-name}"
: "${TOKEN_ENV:?Missing --token-env}"

[[ -d "$PORTFOLIO_PATH" ]] || { echo "PortfolioPath does not exist."; exit 1; }
[[ -f "$PORTFOLIO_PATH/site/index.html" ]] || { echo "site/index.html is missing."; exit 1; }
command -v git >/dev/null || { echo "git is required."; exit 1; }
command -v gh >/dev/null || { echo "GitHub CLI is required."; exit 1; }

TOKEN="${!TOKEN_ENV:-}"
if [[ -z "$TOKEN" ]]; then
  echo "Token environment variable is missing. Set it locally. Do not commit tokens."
  exit 1
fi

export GH_TOKEN="$TOKEN"
cd "$PORTFOLIO_PATH"
touch .gitignore
for line in "private-docs/" ".env" ".env.local" "*.token" "tokens.txt" "gittoken.txt" "token.txt"; do
  grep -qxF "$line" .gitignore || echo "$line" >> .gitignore
done

[[ -d .git ]] || git init
git config user.name "$STUDENT_NAME"
git config user.email "$STUDENT_EMAIL"
git branch -M main
git add .
if [[ -n "$(git status --porcelain)" ]]; then
  git commit -m "$COMMIT_MESSAGE"
else
  echo "No local changes to commit."
fi

REPO="$GITHUB_USERNAME/$REPO_NAME"
if gh repo view "$REPO" >/dev/null 2>&1; then
  git remote remove origin >/dev/null 2>&1 || true
  git remote add origin "https://github.com/$REPO.git"
  git push -u origin main
else
  gh repo create "$REPO" --public --source . --remote origin --push
fi

gh api --method POST "repos/$REPO/pages" -f build_type=workflow >/dev/null 2>&1 || \
  gh api --method PUT "repos/$REPO/pages" -f build_type=workflow
gh workflow run "Deploy Portfolio to GitHub Pages" --repo "$REPO" --ref main

if [[ "$WATCH" == "1" ]]; then
  if ! gh run watch --repo "$REPO"; then
    gh run view --repo "$REPO" --log-failed
    echo "Workflow failed. Review the failed log above."
    exit 1
  fi
fi

unset GH_TOKEN
echo "Expected live URL: https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
