param(
  [string]$ConfigPath = "portfolio-batch/deployment-config.local.json",
  [switch]$Watch
)

$ErrorActionPreference = "Stop"
if (!(Test-Path -LiteralPath $ConfigPath)) { throw "Config file not found: $ConfigPath" }
$items = Get-Content -Raw -LiteralPath $ConfigPath | ConvertFrom-Json
foreach ($item in $items) {
  & "$PSScriptRoot/deploy-portfolio.ps1" `
    -PortfolioPath $item.portfolioPath `
    -StudentName $item.studentName `
    -GithubUsername $item.githubUsername `
    -StudentEmail $item.studentEmail `
    -RepoName $item.repoName `
    -TokenEnvironmentVariable $item.tokenEnvironmentVariable `
    -Watch:$Watch
}
