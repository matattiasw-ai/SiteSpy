param(
  [Parameter(Mandatory=$true)][string]$PortfolioPath,
  [Parameter(Mandatory=$true)][string]$StudentName,
  [Parameter(Mandatory=$true)][string]$GithubUsername,
  [Parameter(Mandatory=$true)][string]$StudentEmail,
  [Parameter(Mandatory=$true)][string]$RepoName,
  [Parameter(Mandatory=$true)][string]$TokenEnvironmentVariable,
  [string]$CommitMessage = "complete personal portfolio showcase",
  [switch]$Watch
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $PortfolioPath)) { throw "PortfolioPath does not exist." }
$resolved = (Resolve-Path -LiteralPath $PortfolioPath).Path
if (!(Test-Path -LiteralPath (Join-Path $resolved "site/index.html"))) { throw "site/index.html is missing." }
if (!(Get-Command git -ErrorAction SilentlyContinue)) { throw "git is required." }
if (!(Get-Command gh -ErrorAction SilentlyContinue)) { throw "GitHub CLI is required." }

$token = [Environment]::GetEnvironmentVariable($TokenEnvironmentVariable)
if ([string]::IsNullOrWhiteSpace($token)) {
  throw "Token environment variable is missing. Set it locally. Do not commit tokens."
}

$env:GH_TOKEN = $token
Push-Location $resolved
try {
  $ignore = ".gitignore"
  $protected = @("private-docs/", ".env", ".env.local", "*.token", "tokens.txt", "gittoken.txt", "token.txt")
  if (!(Test-Path $ignore)) { New-Item -ItemType File -Path $ignore | Out-Null }
  $existing = Get-Content $ignore -ErrorAction SilentlyContinue
  foreach ($line in $protected) {
    if ($existing -notcontains $line) { Add-Content -Path $ignore -Value $line }
  }

  if (!(Test-Path ".git")) { git init | Out-Null }
  git config user.name "$StudentName"
  git config user.email "$StudentEmail"
  git branch -M main
  git add .
  if ((git status --porcelain).Trim().Length -gt 0) {
    git commit -m "$CommitMessage"
  } else {
    Write-Host "No local changes to commit."
  }

  $repo = "$GithubUsername/$RepoName"
  gh repo view $repo *> $null
  if ($LASTEXITCODE -ne 0) {
    gh repo create $repo --public --source . --remote origin --push
  } else {
    git remote remove origin 2>$null
    git remote add origin "https://github.com/$repo.git"
    git push -u origin main
  }

  gh api --method POST "repos/$repo/pages" -f build_type=workflow 2>$null
  if ($LASTEXITCODE -ne 0) {
    gh api --method PUT "repos/$repo/pages" -f build_type=workflow
  }
  gh workflow run "Deploy Portfolio to GitHub Pages" --repo $repo --ref main
  if ($Watch) {
    gh run watch --repo $repo
    if ($LASTEXITCODE -ne 0) {
      gh run view --repo $repo --log-failed
      throw "Workflow failed. Review the failed log above."
    }
  }
  Write-Host "Expected live URL: https://$GithubUsername.github.io/$RepoName/"
} finally {
  Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
  Pop-Location
}
