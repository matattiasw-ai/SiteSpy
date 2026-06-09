param(
  [string]$ConfigPath = "portfolio-batch/deployment-config.local.json"
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
  param([Parameter(Mandatory=$true)][string]$Path)

  if ([System.IO.Path]::IsPathRooted($Path)) {
    return $Path
  }

  return (Join-Path (Get-Location).Path $Path)
}

$scriptRoot = $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $scriptRoot "..\..")).Path
$configFullPath = Resolve-RepoPath $ConfigPath
$examplePath = Join-Path $repoRoot "portfolio-batch\deployment-config.local.json.example"

if (!(Test-Path -LiteralPath $configFullPath)) {
  if (Test-Path -LiteralPath $examplePath) {
    Copy-Item -LiteralPath $examplePath -Destination $configFullPath -Force
    Write-Host "Created local deployment config: $configFullPath"
  } else {
    throw "Config file is missing and example file was not found: $examplePath"
  }

  Write-Host "Edit portfolio-batch/deployment-config.local.json first, then rerun this script."
  exit 1
}

try {
  $parsedConfig = Get-Content -Raw -LiteralPath $configFullPath | ConvertFrom-Json
} catch {
  Write-Host "Invalid JSON config: $configFullPath"
  Write-Host $_.Exception.Message
  exit 1
}

$items = @()
foreach ($entry in $parsedConfig) {
  $items += $entry
}

$missing = @()
foreach ($item in $items) {
  $tokenName = [string]$item.tokenEnvironmentVariable
  if ([string]::IsNullOrWhiteSpace($tokenName)) {
    continue
  }

  if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($tokenName))) {
    $missing += [PSCustomObject]@{
      studentName = [string]$item.studentName
      repoName = [string]$item.repoName
      tokenEnvironmentVariable = $tokenName
    }
  }
}

if ($missing.Count -eq 0) {
  Write-Host "All configured token environment variables are set."
  exit 0
}

Write-Host "Missing token environment variables:"
Write-Host ""
foreach ($item in $missing) {
  Write-Host "# $($item.studentName) - $($item.repoName)"
  Write-Host "`$env:$($item.tokenEnvironmentVariable)=""paste_token_here"""
  Write-Host ""
}

Write-Host "Set these only in your local terminal. Do not save token values in files or commit them."
