# Git Workflow

Each contributor works from `main`, uses their own Git identity, and opens a pull request for review.

## Setup

```bash
git fetch origin
git checkout main
git pull
npm install
npm run check
```

## Branch Examples

```bash
git checkout -b mobile/<student-task>
git checkout -b firebase/<student-task>
```

## Commit Rules

- Commit only your own work.
- Do not commit `.env`, passwords, tokens, PATs, Firebase keys, or raw collaborator files.
- Keep Firebase values in local `.env` only.
- Run `npm run check` before pushing.

## Push

```bash
git push -u origin <branch-name>
```
