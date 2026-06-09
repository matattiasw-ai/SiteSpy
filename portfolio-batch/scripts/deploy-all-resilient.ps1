param(
  [string]$ConfigPath = "portfolio-batch/deployment-config.local.json",
  [string]$SingleStudent = "",
  [switch]$Watch
)

$ErrorActionPreference = "Continue"

$root = (Get-Location).Path
$configFullPath = Join-Path $root $ConfigPath
$script = Join-Path $root "portfolio-batch/scripts/deploy-portfolio.ps1"

if (!(Test-Path -LiteralPath $configFullPath -PathType Leaf)) {
  Write-Error "Config file not found: $ConfigPath"
  exit 1
}

if (!(Test-Path -LiteralPath $script -PathType Leaf)) {
  Write-Error "Deploy script not found: $script"
  exit 1
}

$config = Get-Content -LiteralPath $configFullPath -Raw | ConvertFrom-Json

if (![string]::IsNullOrWhiteSpace($SingleStudent)) {
  $config = @($config | Where-Object { $_.studentName -eq $SingleStudent })
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logDir = Join-Path $root "portfolio-batch/logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$mdLog = Join-Path $logDir "deployment-run-$stamp.md"
$jsonLog = Join-Path $logDir "deployment-run-$stamp.json"

$results = @()

foreach ($item in $config) {
  $student = [string]$item.studentName
  $repoName = [string]$item.repoName
  $ghUser = [string]$item.githubUsername
  $email = [string]$item.studentEmail
  $portfolioPath = [string]$item.portfolioPath
  $tokenEnv = [string]$item.tokenEnvironmentVariable
  $repo = "$ghUser/$repoName"

  Write-Host ""
  Write-Host "Student: $student"
  Write-Host "Repo: $repoName"

  $record = [ordered]@{
    studentName = $student
    repo = $repo
    status = "pending"
    reason = ""
    liveUrl = "https://$ghUser.github.io/$repoName/"
    events = @()
  }

  if ([string]::IsNullOrWhiteSpace($tokenEnv) -or [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($tokenEnv, "Process"))) {
    Write-Host "SKIP: token environment variable is missing"
    $record.status = "skipped"
    $record.reason = "token missing: $tokenEnv"
    $results += [pscustomobject]$record
    continue
  }

  if ([string]::IsNullOrWhiteSpace($portfolioPath) -or !(Test-Path -LiteralPath $portfolioPath -PathType Container)) {
    Write-Host "SKIP: portfolio path missing"
    $record.status = "skipped"
    $record.reason = "portfolio path missing"
    $results += [pscustomobject]$record
    continue
  }

  if (!(Test-Path -LiteralPath (Join-Path $portfolioPath "site/index.html") -PathType Leaf)) {
    Write-Host "SKIP: site/index.html missing"
    $record.status = "skipped"
    $record.reason = "site/index.html missing"
    $results += [pscustomobject]$record
    continue
  }

  $args = @(
    "-ExecutionPolicy", "Bypass",
    "-NoProfile",
    "-File", $script,
    "-PortfolioPath", $portfolioPath,
    "-StudentName", $student,
    "-GithubUsername", $ghUser,
    "-StudentEmail", $email,
    "-RepoName", $repoName,
    "-TokenEnvironmentVariable", $tokenEnv
  )
  if ($Watch) { $args += "-Watch" }

  $output = & powershell @args 2>&1
  $exitCode = $LASTEXITCODE

  foreach ($line in $output) {
    $text = [string]$line
    Write-Host $text
    if ($text.StartsWith("[deploy-event]")) {
      $record.events += $text
    }
  }

  if ($exitCode -eq 0) {
    $record.status = "success"
    $record.reason = "deployed"
  } else {
    $record.status = "failed"
    $record.reason = (($output | Out-String).Trim())
    Write-Host "FAILED: deployment exited with code $exitCode"
  }

  $results += [pscustomobject]$record
}

$total = $results.Count
$success = @($results | Where-Object { $_.status -eq "success" }).Count
$skippedToken = @($results | Where-Object { $_.reason -like "token missing*" }).Count
$skippedFiles = @($results | Where-Object { $_.status -eq "skipped" -and $_.reason -notlike "token missing*" }).Count
$failed = @($results | Where-Object { $_.status -eq "failed" }).Count

$md = @()
$md += "# Portfolio Deployment Run - $stamp"
$md += ""
$md += "- Total portfolios: $total"
$md += "- Successful deployments: $success"
$md += "- Skipped due to missing token: $skippedToken"
$md += "- Skipped due to missing files/config: $skippedFiles"
$md += "- Failed deployments: $failed"
$md += ""
$md += "## Results"
foreach ($r in $results) {
  $md += "- $($r.studentName): $($r.status) - $($r.reason) - $($r.liveUrl)"
}
$md += ""
$md += "## Expected Live URLs"
foreach ($r in $results) {
  $md += "- $($r.studentName): $($r.liveUrl)"
}

$md | Set-Content -LiteralPath $mdLog -Encoding UTF8
$results | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $jsonLog -Encoding UTF8

Write-Host ""
Write-Host "Summary"
Write-Host "Total portfolios: $total"
Write-Host "Successful deployments: $success"
Write-Host "Skipped due to missing token: $skippedToken"
Write-Host "Skipped due to missing files/config: $skippedFiles"
Write-Host "Failed deployments: $failed"
Write-Host "Markdown log: $mdLog"
Write-Host "JSON log: $jsonLog"
Write-Host ""
Write-Host "Expected live URLs:"
foreach ($r in $results) {
  Write-Host "- $($r.studentName): $($r.liveUrl)"
}
