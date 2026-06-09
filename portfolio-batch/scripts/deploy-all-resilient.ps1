param(
  [string]$ConfigPath = "portfolio-batch/deployment-config.local.json",
  [switch]$Watch
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
  param([Parameter(Mandatory=$true)][string]$Path)

  if ([System.IO.Path]::IsPathRooted($Path)) {
    return $Path
  }

  return (Join-Path (Get-Location).Path $Path)
}

function New-Result {
  param(
    [object]$Item,
    [string]$Status,
    [string]$Reason,
    [string]$LiveUrl
  )

  [PSCustomObject]@{
    studentName = [string]$Item.studentName
    githubUsername = [string]$Item.githubUsername
    studentEmail = [string]$Item.studentEmail
    repoName = [string]$Item.repoName
    portfolioPath = [string]$Item.portfolioPath
    tokenEnvironmentVariable = [string]$Item.tokenEnvironmentVariable
    status = $Status
    reason = $Reason
    expectedLiveUrl = $LiveUrl
    completedAt = (Get-Date).ToString("o")
  }
}

function Add-LogLine {
  param(
    [System.Collections.Generic.List[string]]$Lines,
    [string]$Text
  )

  $Lines.Add($Text) | Out-Null
}

$scriptRoot = $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $scriptRoot "..\..")).Path
$configFullPath = Resolve-RepoPath $ConfigPath
$examplePath = Join-Path $repoRoot "portfolio-batch\deployment-config.local.json.example"
$deployScript = Join-Path $scriptRoot "deploy-portfolio.ps1"
$logsDir = Join-Path $repoRoot "portfolio-batch\logs"

if (!(Test-Path -LiteralPath $configFullPath)) {
  if (!(Test-Path -LiteralPath $examplePath)) {
    throw "Config file is missing and example file was not found: $examplePath"
  }

  Copy-Item -LiteralPath $examplePath -Destination $configFullPath -Force
  Write-Host "Created local deployment config: $configFullPath"
  Write-Host "Edit portfolio-batch/deployment-config.local.json first, set token environment variables, then rerun this script."
  exit 1
}

if (!(Test-Path -LiteralPath $deployScript)) {
  throw "Deploy script not found: $deployScript"
}

$configText = Get-Content -Raw -LiteralPath $configFullPath
try {
  $parsedConfig = $configText | ConvertFrom-Json
} catch {
  Write-Host "Invalid JSON config: $configFullPath"
  Write-Host $_.Exception.Message
  exit 1
}

$config = @()
foreach ($entry in $parsedConfig) {
  $config += $entry
}

if ($config.Count -eq 0) {
  Write-Host "Deployment config has no portfolio entries: $configFullPath"
  exit 1
}

New-Item -ItemType Directory -Force -Path $logsDir | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$markdownLog = Join-Path $logsDir "deployment-run-$timestamp.md"
$jsonLog = Join-Path $logsDir "deployment-run-$timestamp.json"
$lines = [System.Collections.Generic.List[string]]::new()
$results = [System.Collections.Generic.List[object]]::new()

Add-LogLine $lines "# SiteSpy Portfolio Deployment Run"
Add-LogLine $lines ""
Add-LogLine $lines "- Started: $(Get-Date -Format o)"
Add-LogLine $lines "- Config: `$ConfigPath`"
Add-LogLine $lines "- Watch: $([bool]$Watch)"
Add-LogLine $lines ""
Add-LogLine $lines "## Results"
Add-LogLine $lines ""
Add-LogLine $lines "| Student | Repo | Status | Reason | Expected Live URL |"
Add-LogLine $lines "|---|---|---|---|---|"

foreach ($item in $config) {
  $studentName = [string]$item.studentName
  $repoName = [string]$item.repoName
  $githubUsername = [string]$item.githubUsername
  $studentEmail = [string]$item.studentEmail
  $portfolioPath = [string]$item.portfolioPath
  $tokenEnvironmentVariable = [string]$item.tokenEnvironmentVariable
  $liveUrl = if ($githubUsername -and $repoName) { "https://$githubUsername.github.io/$repoName/" } else { "" }

  Write-Host ""
  Write-Host "Student: $studentName"
  Write-Host "Repo: $repoName"

  $skipReason = $null
  if ([string]::IsNullOrWhiteSpace($portfolioPath)) {
    $skipReason = "portfolioPath is missing from config"
  } elseif (!(Test-Path -LiteralPath $portfolioPath)) {
    $skipReason = "PortfolioPath does not exist"
  } elseif (!(Test-Path -LiteralPath (Join-Path $portfolioPath "site\index.html"))) {
    $skipReason = "site/index.html is missing"
  } elseif ([string]::IsNullOrWhiteSpace($tokenEnvironmentVariable)) {
    $skipReason = "tokenEnvironmentVariable is missing from config"
  } elseif ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($tokenEnvironmentVariable))) {
    $skipReason = "token environment variable is missing"
  }

  if ($skipReason) {
    Write-Host "SKIP: $skipReason"
    $result = New-Result -Item $item -Status "SKIPPED" -Reason $skipReason -LiveUrl $liveUrl
    $results.Add($result) | Out-Null
    Add-LogLine $lines "| $studentName | $repoName | SKIPPED | $skipReason | $liveUrl |"
    continue
  }

  try {
    $arguments = @{
      PortfolioPath = $portfolioPath
      StudentName = $studentName
      GithubUsername = $githubUsername
      StudentEmail = $studentEmail
      RepoName = $repoName
      TokenEnvironmentVariable = $tokenEnvironmentVariable
    }

    & $deployScript @arguments -Watch:$Watch
    if ($LASTEXITCODE -ne 0) {
      throw "deploy-portfolio.ps1 exited with code $LASTEXITCODE"
    }

    Write-Host "SUCCESS: $liveUrl"
    $result = New-Result -Item $item -Status "SUCCESS" -Reason "" -LiveUrl $liveUrl
    $results.Add($result) | Out-Null
    Add-LogLine $lines "| $studentName | $repoName | SUCCESS |  | $liveUrl |"
  } catch {
    $message = $_.Exception.Message
    Write-Host "FAILED: $message"
    $result = New-Result -Item $item -Status "FAILED" -Reason $message -LiveUrl $liveUrl
    $results.Add($result) | Out-Null
    Add-LogLine $lines "| $studentName | $repoName | FAILED | $message | $liveUrl |"
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
    continue
  }
}

$successful = @($results | Where-Object { $_.status -eq "SUCCESS" })
$missingToken = @($results | Where-Object { $_.status -eq "SKIPPED" -and $_.reason -eq "token environment variable is missing" })
$missingFiles = @($results | Where-Object { $_.status -eq "SKIPPED" -and ($_.reason -ne "token environment variable is missing") })
$failed = @($results | Where-Object { $_.status -eq "FAILED" })

Add-LogLine $lines ""
Add-LogLine $lines "## Summary"
Add-LogLine $lines ""
Add-LogLine $lines "- Total portfolios: $($results.Count)"
Add-LogLine $lines "- Successful deployments: $($successful.Count)"
Add-LogLine $lines "- Skipped due to missing token: $($missingToken.Count)"
Add-LogLine $lines "- Skipped due to missing files/config: $($missingFiles.Count)"
Add-LogLine $lines "- Failed deployments: $($failed.Count)"
Add-LogLine $lines ""
Add-LogLine $lines "## Expected Live URLs"
Add-LogLine $lines ""
foreach ($result in $results) {
  if (![string]::IsNullOrWhiteSpace($result.expectedLiveUrl)) {
    Add-LogLine $lines "- $($result.studentName): $($result.expectedLiveUrl)"
  }
}

$summary = [PSCustomObject]@{
  startedAt = $timestamp
  totalPortfolios = $results.Count
  successfulDeployments = $successful.Count
  skippedDueToMissingToken = $missingToken.Count
  skippedDueToMissingFiles = $missingFiles.Count
  failedDeployments = $failed.Count
  results = @($results)
}

$lines | Set-Content -LiteralPath $markdownLog -Encoding UTF8
$summary | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $jsonLog -Encoding UTF8

Write-Host ""
Write-Host "Summary"
Write-Host "Total portfolios: $($results.Count)"
Write-Host "Successful deployments: $($successful.Count)"
Write-Host "Skipped due to missing token: $($missingToken.Count)"
Write-Host "Skipped due to missing files/config: $($missingFiles.Count)"
Write-Host "Failed deployments: $($failed.Count)"
Write-Host "Markdown log: $markdownLog"
Write-Host "JSON log: $jsonLog"
Write-Host ""
Write-Host "Expected live URLs:"
foreach ($result in $results) {
  if (![string]::IsNullOrWhiteSpace($result.expectedLiveUrl)) {
    Write-Host "- $($result.studentName): $($result.expectedLiveUrl)"
  }
}
