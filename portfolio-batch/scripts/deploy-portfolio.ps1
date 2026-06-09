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

$ErrorActionPreference = "Continue"

function Stop-Deploy([string]$Message) {
  Write-Error $Message
  exit 1
}

function Clean-Identity([string]$Value) {
  return (($Value -replace "[\r\n]+", " ") -replace "\s+", " ").Trim()
}

function Redact-Text([string]$Text, [string]$Token) {
  if ([string]::IsNullOrEmpty($Text) -or [string]::IsNullOrEmpty($Token)) {
    return $Text
  }
  return $Text.Replace($Token, "[REDACTED_TOKEN]")
}

function Invoke-GitChecked {
  param(
    [Parameter(Mandatory=$true)][string]$RepoPath,
    [Parameter(Mandatory=$true)][string[]]$Arguments,
    [Parameter(Mandatory=$true)][string]$FailureMessage
  )

  $output = (& git -C $RepoPath @Arguments 2>&1)
  $exitCode = $LASTEXITCODE
  Write-Host "[deploy-event] git_exit=$($Arguments -join ' ') code=$exitCode"
  if ($exitCode -ne 0) {
    $text = (($output | Out-String).Trim())
    Stop-Deploy "$FailureMessage in $RepoPath`: $text"
  }
  return $output
}

if (!(Get-Command git -ErrorAction SilentlyContinue)) {
  Stop-Deploy "git is required."
}

if (!(Get-Command gh -ErrorAction SilentlyContinue)) {
  Stop-Deploy "GitHub CLI is required."
}

if (!(Test-Path -LiteralPath $PortfolioPath -PathType Container)) {
  Stop-Deploy "PortfolioPath does not exist: $PortfolioPath"
}

$repoPath = (Resolve-Path -LiteralPath $PortfolioPath).Path
$indexPath = Join-Path $repoPath "site/index.html"
if (!(Test-Path -LiteralPath $indexPath -PathType Leaf)) {
  Stop-Deploy "site/index.html is missing in $repoPath"
}

$token = [Environment]::GetEnvironmentVariable($TokenEnvironmentVariable, "Process")
if ([string]::IsNullOrWhiteSpace($token)) {
  Stop-Deploy "Token environment variable is missing: $TokenEnvironmentVariable"
}

$repo = "$GithubUsername/$RepoName"
$oldGhToken = [Environment]::GetEnvironmentVariable("GH_TOKEN", "Process")
$env:GH_TOKEN = $token

try {
  $loginOutput = (& gh api user --jq ".login" 2>&1)
  if ($LASTEXITCODE -ne 0) {
    Stop-Deploy "Could not verify GitHub token owner: $(Redact-Text (($loginOutput | Out-String).Trim()) $token)"
  }

  $login = Clean-Identity (($loginOutput | Out-String).Trim())
  if ($login -ne $GithubUsername) {
    Stop-Deploy "Token belongs to $login, but config expects $GithubUsername. Use the correct student token or fix config."
  }
  Write-Host "[deploy-event] token_owner_verified=$login"

  $gitDir = Join-Path $repoPath ".git"
  Write-Host "[deploy-event] repo_path=$repoPath"
  Write-Host "[deploy-event] git_exists=$([bool](Test-Path -LiteralPath $gitDir -PathType Container))"

  if (!(Test-Path -LiteralPath $gitDir -PathType Container)) {
    Invoke-GitChecked -RepoPath $repoPath -Arguments @("init") -FailureMessage "git init failed" | Out-Null
    Write-Host "[deploy-event] git_initialized=$repoPath"
  }

  Invoke-GitChecked -RepoPath $repoPath -Arguments @("branch", "-M", "main") -FailureMessage "Failed to set branch main" | Out-Null

  $safeName = Clean-Identity $StudentName
  if ([string]::IsNullOrWhiteSpace($safeName)) {
    $safeName = $GithubUsername
  }

  $safeEmail = Clean-Identity $StudentEmail
  if ([string]::IsNullOrWhiteSpace($safeEmail) -or $safeEmail -notmatch "@") {
    $safeEmail = "$GithubUsername@users.noreply.github.com"
  }

  Write-Host "[deploy-event] intended_git_user_name=$safeName"
  Write-Host "[deploy-event] intended_git_user_email=$safeEmail"

  Invoke-GitChecked -RepoPath $repoPath -Arguments @("config", "user.name", $safeName) -FailureMessage "Failed to set git user.name" | Out-Null
  Invoke-GitChecked -RepoPath $repoPath -Arguments @("config", "user.email", $safeEmail) -FailureMessage "Failed to set git user.email" | Out-Null
  Write-Host "[deploy-event] git_identity_set=$repoPath"

  $ignorePath = Join-Path $repoPath ".gitignore"
  if (!(Test-Path -LiteralPath $ignorePath -PathType Leaf)) {
    New-Item -ItemType File -Path $ignorePath | Out-Null
  }

  $ignoreLines = @(
    "private-docs/",
    ".env",
    ".env.local",
    "*.token",
    "tokens.txt",
    "gittoken.txt",
    "token.txt",
    ".venv/",
    "__pycache__/",
    "build/",
    "dist/"
  )
  $existingIgnore = @(Get-Content -LiteralPath $ignorePath -ErrorAction SilentlyContinue)
  foreach ($line in $ignoreLines) {
    if ($existingIgnore -notcontains $line) {
      Add-Content -LiteralPath $ignorePath -Value $line
    }
  }

  Invoke-GitChecked -RepoPath $repoPath -Arguments @("add", ".") -FailureMessage "git add failed" | Out-Null
  $status = (& git -C $repoPath status --porcelain)
  if ($status) {
    Invoke-GitChecked -RepoPath $repoPath -Arguments @("commit", "-m", $CommitMessage) -FailureMessage "git commit failed" | Out-Null
    Write-Host "[deploy-event] committed=$repo"
  } else {
    Write-Host "[deploy-event] no_local_changes=$repo"
  }

  $repoExists = $false
  gh repo view $repo *> $null
  if ($LASTEXITCODE -eq 0) {
    $repoExists = $true
    Write-Host "[deploy-event] repo_exists=$repo"
  } else {
    Write-Host "[deploy-event] repo_missing=$repo"
  }

  if (-not $repoExists) {
    Write-Host "[deploy-event] creating_repo=$repo"
    $createOutput = (& gh repo create $repo --public 2>&1)
    if ($LASTEXITCODE -ne 0) {
      Stop-Deploy "Failed to create repo $repo`: $(Redact-Text (($createOutput | Out-String).Trim()) $token)"
    }
    Write-Host "[deploy-event] repo_created=$repo"
  }

  & git -C $repoPath remote remove origin 2>$null
  Invoke-GitChecked -RepoPath $repoPath -Arguments @("remote", "add", "origin", "https://github.com/$repo.git") -FailureMessage "Failed to set origin" | Out-Null

  $pushUrl = "https://x-access-token:$token@github.com/$repo.git"
  $pushOutput = (& git -C $repoPath push -u $pushUrl main 2>&1)
  if ($LASTEXITCODE -ne 0) {
    Stop-Deploy "Failed to push repo $repo`: $(Redact-Text (($pushOutput | Out-String).Trim()) $token)"
  }
  Write-Host "[deploy-event] pushed=$repo"

  $pagesOutput = (& gh api --method POST "repos/$repo/pages" -f build_type=workflow 2>&1)
  if ($LASTEXITCODE -eq 0) {
    Write-Host "[deploy-event] pages_enabled=$repo"
  } else {
    $pagesText = (($pagesOutput | Out-String).Trim())
    if ($pagesText -match "already exists" -or $pagesText -match "already_exists" -or $pagesText -match "409") {
      $putOutput = (& gh api --method PUT "repos/$repo/pages" -f build_type=workflow 2>&1)
      if ($LASTEXITCODE -ne 0) {
        Stop-Deploy "Pages update failed for $repo`: $(Redact-Text (($putOutput | Out-String).Trim()) $token)"
      }
      Write-Host "[deploy-event] pages_updated=$repo"
    } else {
      Stop-Deploy "Pages setup failed for $repo`: $(Redact-Text $pagesText $token)"
    }
  }

  $workflowOutput = (& gh workflow run "Deploy Portfolio to GitHub Pages" --repo $repo --ref main 2>&1)
  if ($LASTEXITCODE -ne 0) {
    $workflowOutput = (& gh workflow run "deploy-pages.yml" --repo $repo --ref main 2>&1)
    if ($LASTEXITCODE -ne 0) {
      Stop-Deploy "workflow trigger failed for $repo`: $(Redact-Text (($workflowOutput | Out-String).Trim()) $token)"
    }
  }
  Write-Host "[deploy-event] workflow_triggered=$repo"

  if ($Watch) {
    $watchOutput = (& gh run watch --repo $repo 2>&1)
    if ($LASTEXITCODE -ne 0) {
      & gh run view --repo $repo --log-failed
      Stop-Deploy "workflow failed for $repo`: $(Redact-Text (($watchOutput | Out-String).Trim()) $token)"
    }
    Write-Host "[deploy-event] workflow_success=$repo"
  }

  Write-Host "Expected live URL: https://$GithubUsername.github.io/$RepoName/"
  exit 0
}
finally {
  if ([string]::IsNullOrWhiteSpace($oldGhToken)) {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
  } else {
    $env:GH_TOKEN = $oldGhToken
  }
}
