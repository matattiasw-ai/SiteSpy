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

function Invoke-Checked {
  param(
    [Parameter(Mandatory=$true)][string]$Command,
    [Parameter(Mandatory=$true)][string[]]$Arguments,
    [string]$FailureMessage
  )

  $output = & $Command @Arguments 2>&1
  $exitCode = $LASTEXITCODE
  if ($exitCode -ne 0) {
    $details = ($output | Out-String).Trim()
    if ([string]::IsNullOrWhiteSpace($details)) {
      $details = "exit code $exitCode"
    }

    if ([string]::IsNullOrWhiteSpace($FailureMessage)) {
      throw $details
    }

    throw "$FailureMessage $details"
  }

  return $output
}

function Invoke-Status {
  param(
    [Parameter(Mandatory=$true)][string]$Command,
    [Parameter(Mandatory=$true)][string[]]$Arguments
  )

  $output = & $Command @Arguments 2>&1
  [PSCustomObject]@{
    ExitCode = $LASTEXITCODE
    Output = ($output | Out-String).Trim()
  }
}

if (!(Test-Path -LiteralPath $PortfolioPath)) { throw "PortfolioPath does not exist." }
$resolved = (Resolve-Path -LiteralPath $PortfolioPath).Path
if (!(Test-Path -LiteralPath (Join-Path $resolved "site/index.html"))) { throw "site/index.html is missing." }
if (!(Get-Command git -ErrorAction SilentlyContinue)) { throw "git is required." }
if (!(Get-Command gh -ErrorAction SilentlyContinue)) { throw "GitHub CLI is required." }

$token = [Environment]::GetEnvironmentVariable($TokenEnvironmentVariable)
if ([string]::IsNullOrWhiteSpace($token)) {
  throw "Token environment variable is missing. Set it locally. Do not commit tokens."
}

$repo = "$GithubUsername/$RepoName"
$liveUrl = "https://$GithubUsername.github.io/$RepoName/"
$env:GH_TOKEN = $token

try {
  $tokenOwner = (Invoke-Checked -Command "gh" -Arguments @("api", "user", "--jq", ".login") -FailureMessage "Could not validate GitHub token owner.").Trim()
  if ($tokenOwner.ToLowerInvariant() -ne $GithubUsername.ToLowerInvariant()) {
    throw "Token belongs to $tokenOwner, but config expects $GithubUsername. Use the correct student token or fix config."
  }
  Write-Output "[deploy-event] token_owner_verified=$tokenOwner"

  Push-Location $resolved
  try {
    $ignore = ".gitignore"
    $protected = @("private-docs/", ".env", ".env.local", "*.token", "tokens.txt", "gittoken.txt", "token.txt")
    if (!(Test-Path $ignore)) { New-Item -ItemType File -Path $ignore | Out-Null }
    $existing = @(Get-Content $ignore -ErrorAction SilentlyContinue)
    foreach ($line in $protected) {
      if ($existing -notcontains $line) { Add-Content -Path $ignore -Value $line }
    }

    if (!(Test-Path ".git")) {
      Invoke-Checked -Command "git" -Arguments @("init") -FailureMessage "git init failed." | Out-Null
    }

    Invoke-Checked -Command "git" -Arguments @("config", "user.name", $StudentName) -FailureMessage "git config user.name failed." | Out-Null
    Invoke-Checked -Command "git" -Arguments @("config", "user.email", $StudentEmail) -FailureMessage "git config user.email failed." | Out-Null
    Invoke-Checked -Command "git" -Arguments @("branch", "-M", "main") -FailureMessage "git branch setup failed." | Out-Null
    Invoke-Checked -Command "git" -Arguments @("add", ".") -FailureMessage "git add failed." | Out-Null

    $status = (Invoke-Checked -Command "git" -Arguments @("status", "--porcelain") -FailureMessage "git status failed." | Out-String).Trim()
    if ($status.Length -gt 0) {
      Invoke-Checked -Command "git" -Arguments @("commit", "-m", $CommitMessage) -FailureMessage "git commit failed." | Out-Null
      Write-Output "[deploy-event] committed"
    } else {
      Write-Output "[deploy-event] no_local_changes"
    }

    $repoExists = $false
    gh repo view $repo *> $null
    if ($LASTEXITCODE -eq 0) {
      $repoExists = $true
      Write-Output "[deploy-event] repo_exists=$repo"
      Write-Output "[deploy-event] repo_existed"
    } else {
      Write-Output "[deploy-event] repo_missing=$repo"
    }

    if (-not $repoExists) {
      Write-Output "[deploy-event] creating_repo=$repo"
      gh repo create $repo --public --source . --remote origin --push
      if ($LASTEXITCODE -ne 0) { throw "Failed to create repo $repo" }
      Write-Output "[deploy-event] repo_created"
      Write-Output "[deploy-event] pushed"
    } else {
      git remote remove origin 2>$null
      git remote add origin "https://github.com/$repo.git"
      $authHeader = "AUTHORIZATION: bearer $token"
      git -c "http.https://github.com/.extraheader=$authHeader" push -u origin main
      if ($LASTEXITCODE -ne 0) { throw "Failed to push repo $repo" }
      Write-Output "[deploy-event] pushed"
    }

    $pagesPost = Invoke-Status -Command "gh" -Arguments @("api", "--method", "POST", "repos/$repo/pages", "-f", "build_type=workflow")
    if ($pagesPost.ExitCode -eq 0) {
      Write-Output "[deploy-event] pages_enabled"
    } else {
      Invoke-Checked -Command "gh" -Arguments @("api", "--method", "PUT", "repos/$repo/pages", "-f", "build_type=workflow") -FailureMessage "GitHub Pages setup failed." | Out-Null
      Write-Output "[deploy-event] pages_confirmed"
    }

    Invoke-Checked -Command "gh" -Arguments @("workflow", "run", "Deploy Portfolio to GitHub Pages", "--repo", $repo, "--ref", "main") -FailureMessage "Workflow trigger failed." | Out-Null
    Write-Output "[deploy-event] workflow_triggered"

    if ($Watch) {
      $watchResult = Invoke-Status -Command "gh" -Arguments @("run", "watch", "--repo", $repo)
      if ($watchResult.ExitCode -ne 0) {
        Invoke-Status -Command "gh" -Arguments @("run", "view", "--repo", $repo, "--log-failed") | Out-Null
        Write-Output "[deploy-event] workflow_failed"
        throw "Workflow failed. Review GitHub Actions logs for $repo."
      }
      Write-Output "[deploy-event] workflow_success"
    }

    Write-Output "Expected live URL: $liveUrl"
  } finally {
    Pop-Location
  }
} finally {
  Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
