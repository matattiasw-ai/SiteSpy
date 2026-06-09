# SiteSpy Portfolio Deployment

Use these scripts to deploy student portfolio repositories in a repeatable way without exposing tokens.

## Configure Deployment

The local config is:

```powershell
portfolio-batch\deployment-config.local.json
```

If it does not exist, either deployment helper will copy:

```powershell
portfolio-batch\deployment-config.local.json.example
```

Edit `deployment-config.local.json` before deploying. Confirm each entry has:

- `portfolioPath`
- `studentName`
- `githubUsername`
- `studentEmail`
- `repoName`
- `tokenEnvironmentVariable`

Do not put token values in the JSON file.

## Set Tokens

Show missing token variables:

```powershell
.\portfolio-batch\scripts\show-missing-tokens.ps1
```

Set missing tokens in the current PowerShell session:

```powershell
$env:GH_TOKEN_VALENTINA_CORREIA="paste_token_here"
```

Use the token variable names printed by the helper script. Do not commit tokens and do not write token values to files.

## Deploy One Portfolio

Run the existing single-portfolio deploy script with one config entry's values:

```powershell
.\portfolio-batch\scripts\deploy-portfolio.ps1 `
  -PortfolioPath "D:\Documents\Jobs\SiteSpy\portfolios\correia-vp-sitespy-portfolio" `
  -StudentName "Valentina Correia" `
  -GithubUsername "Valentina-Correia" `
  -StudentEmail "penneckyvalentina@gmail.com" `
  -RepoName "ValentinaCorreiaPortfolio" `
  -TokenEnvironmentVariable "GH_TOKEN_VALENTINA_CORREIA" `
  -Watch
```

The deploy script is idempotent: it initializes Git if needed, reuses the repo if it already exists, commits only when local changes exist, pushes to `main`, and configures GitHub Pages workflow mode.

## Deploy All Portfolios Resiliently

Run all configured deployments and keep going after skips or failures:

```powershell
.\portfolio-batch\scripts\deploy-all-resilient.ps1 -Watch
```

The resilient runner checks each portfolio before deployment:

- portfolio path exists
- `site/index.html` exists
- token environment variable name exists
- token value exists in the current environment

Missing tokens or files are skipped, not fatal. Failed deployments are logged and the batch continues.

## Re-run Failed Or Skipped Deployments

After fixing a missing token, missing portfolio path, missing `site/index.html`, or failed GitHub issue, rerun:

```powershell
.\portfolio-batch\scripts\deploy-all-resilient.ps1 -Watch
```

The scripts are designed to be safe to rerun. Existing repositories are reused and no-change commits do not fail the batch.

## Deployment Logs

Each resilient run writes:

```powershell
portfolio-batch\logs\deployment-run-YYYYMMDD-HHMMSS.md
portfolio-batch\logs\deployment-run-YYYYMMDD-HHMMSS.json
```

The logs include:

- total portfolios
- successful deployments
- skipped deployments due to missing token
- skipped deployments due to missing files/config
- failed deployments
- expected live URLs

## Check GitHub Actions

For a deployed portfolio repository:

```powershell
gh run list --repo GitHubUsername/RepoName
gh run view --repo GitHubUsername/RepoName --log-failed
```

With `-Watch`, the deployment script watches the workflow and prints failed logs when a workflow fails.

## Check Live URLs

Expected portfolio URLs use:

```text
https://GitHubUsername.github.io/RepoName/
```

Example:

```text
https://Valentina-Correia.github.io/ValentinaCorreiaPortfolio/
```

GitHub Pages can take a few minutes after the workflow completes.
