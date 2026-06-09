param(
  [string]$ConfigPath = "portfolio-batch/deployment-config.active.json",
  [string]$SingleStudent = "",
  [string]$BranchName = "evidence-update",
  [string]$CommitMessage = "docs: add portfolio evidence notes",
  [switch]$OpenPullRequest
)

$ErrorActionPreference = "Continue"

function Resolve-RepoPath([string]$PathValue) {
  if ([System.IO.Path]::IsPathRooted($PathValue)) {
    return $PathValue
  }
  return Join-Path (Get-Location).Path $PathValue
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

function Write-StudentDocs($Item, [string]$DocsPath) {
  $student = [string]$Item.studentName
  $githubUsername = [string]$Item.githubUsername
  $repoName = [string]$Item.repoName
  $email = [string]$Item.studentEmail
  $repoUrl = "https://github.com/$githubUsername/$repoName"
  $liveUrl = "https://$githubUsername.github.io/$repoName/"

  New-Item -ItemType Directory -Force -Path $DocsPath | Out-Null

  @"
# $student Evidence Update Notes

## Student Details

- Name: $student
- Email: $email
- GitHub username: $githubUsername
- Repository: $repoUrl
- Live portfolio: $liveUrl

## Evidence Purpose

This branch is for adding real screenshots and short notes that connect the portfolio to the student's SiteSpy contribution and GitHub workflow.

## Evidence Rules

- Use only screenshots from the student's own repository, live page, branch, commits, pull request, or SiteSpy work.
- Do not add private credentials.
- Keep screenshots readable and named clearly.
- Add screenshots under `site/assets/screenshots/`.

## Suggested Commit Flow

```bash
git checkout -b evidence-update
git add docs site/assets/screenshots
git commit -m "docs: add portfolio evidence screenshots"
git push -u origin evidence-update
```
"@ | Set-Content -LiteralPath (Join-Path $DocsPath "evidence-update-notes.md") -Encoding UTF8

  @"
# $student Screenshot Capture Guide

Capture only real evidence. The public portfolio will show screenshots only after they exist in `site/assets/screenshots/`.

| Filename | What it should show |
|---|---|
| `live-homepage.png` | Live portfolio homepage |
| `github-repository-main.png` | GitHub repository main page |
| `github-actions-success.png` | GitHub Actions successful deployment run |
| `commit-history.png` | Commit history page |
| `development-branch.png` | Development branch or contribution branch |
| `pull-request.png` | Pull request page once created |
| `project-app-screen.png` | Project app screen, if available |
| `code-contribution.png` | Code contribution or changed file |
| `documentation-contribution.png` | README or documentation contribution |
| `certificate-or-proof.png` | Certificate or proof document if available |

After adding files, commit them on the evidence branch and open a pull request to `main`.
"@ | Set-Content -LiteralPath (Join-Path $DocsPath "screenshot-capture-guide.md") -Encoding UTF8
}

if (!(Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Error "git is required."
  exit 1
}

if (!(Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Error "GitHub CLI is required."
  exit 1
}

$configFullPath = Resolve-RepoPath $ConfigPath
if (!(Test-Path -LiteralPath $configFullPath -PathType Leaf)) {
  Write-Error "Config file not found: $ConfigPath"
  exit 1
}

$config = Get-Content -LiteralPath $configFullPath -Raw | ConvertFrom-Json
if (![string]::IsNullOrWhiteSpace($SingleStudent)) {
  $config = @($config | Where-Object { $_.studentName -eq $SingleStudent })
}

$results = @()
$oldGhToken = [Environment]::GetEnvironmentVariable("GH_TOKEN", "Process")

foreach ($item in $config) {
  $student = [string]$item.studentName
  $githubUsername = [string]$item.githubUsername
  $repoName = [string]$item.repoName
  $email = Clean-Identity ([string]$item.studentEmail)
  $portfolioPath = Resolve-RepoPath ([string]$item.portfolioPath)
  $tokenEnv = [string]$item.tokenEnvironmentVariable
  $repo = "$githubUsername/$repoName"
  $result = [ordered]@{ studentName = $student; repo = $repo; status = "pending"; reason = ""; pullRequest = "" }

  Write-Host ""
  Write-Host "Student: $student"
  Write-Host "Repo: $repo"

  if ($student -match "Penny|Ndaitavela|Nambuli" -or $githubUsername -eq "studentgithub") {
    Write-Host "SKIP: excluded from active evidence automation"
    $result.status = "skipped"
    $result.reason = "excluded"
    $results += [pscustomobject]$result
    continue
  }

  $token = [Environment]::GetEnvironmentVariable($tokenEnv, "Process")
  if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "SKIP: missing token environment variable $tokenEnv"
    $result.status = "skipped"
    $result.reason = "missing token"
    $results += [pscustomobject]$result
    continue
  }

  if (!(Test-Path -LiteralPath $portfolioPath -PathType Container)) {
    Write-Host "SKIP: portfolio path missing"
    $result.status = "skipped"
    $result.reason = "portfolio path missing"
    $results += [pscustomobject]$result
    continue
  }

  try {
    $env:GH_TOKEN = $token
    $login = (& gh api user --jq ".login" 2>&1)
    if ($LASTEXITCODE -ne 0) {
      throw "Could not verify token owner: $(Redact-Text (($login | Out-String).Trim()) $token)"
    }
    $login = ($login | Out-String).Trim()
    if ($login -ne $githubUsername) {
      throw "Token belongs to $login, but config expects $githubUsername. Use the correct student token or fix config."
    }

    if (!(Test-Path -LiteralPath (Join-Path $portfolioPath ".git") -PathType Container)) {
      & git -C $portfolioPath init *> $null
      if ($LASTEXITCODE -ne 0) { throw "git init failed in $portfolioPath" }
    }

    $safeName = Clean-Identity $student
    if ([string]::IsNullOrWhiteSpace($safeName)) { $safeName = $githubUsername }
    if ([string]::IsNullOrWhiteSpace($email) -or $email -notmatch "@") { $email = "$githubUsername@users.noreply.github.com" }

    & git -C $portfolioPath branch -M main *> $null
    & git -C $portfolioPath config user.name "$safeName" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Failed to set git user.name in $portfolioPath" }
    & git -C $portfolioPath config user.email "$email" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Failed to set git user.email in $portfolioPath" }

    & git -C $portfolioPath checkout -B $BranchName *> $null
    if ($LASTEXITCODE -ne 0) { throw "Failed to create branch $BranchName in $portfolioPath" }

    Write-StudentDocs $item (Join-Path $portfolioPath "docs")

    & git -C $portfolioPath add docs 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "git add docs failed in $portfolioPath" }
    $status = (& git -C $portfolioPath status --porcelain)
    if ($status) {
      $commitOutput = (& git -C $portfolioPath commit -m "$CommitMessage" 2>&1)
      if ($LASTEXITCODE -ne 0) {
        throw "git commit failed in $portfolioPath`: $(Redact-Text (($commitOutput | Out-String).Trim()) $token)"
      }
      Write-Host "[evidence-event] committed=$repo"
    } else {
      Write-Host "[evidence-event] no_local_changes=$repo"
    }

    $pushUrl = "https://x-access-token:$token@github.com/$repo.git"
    $pushOutput = (& git -C $portfolioPath push -u $pushUrl $BranchName 2>&1)
    if ($LASTEXITCODE -ne 0) {
      throw "git push failed for $repo`: $(Redact-Text (($pushOutput | Out-String).Trim()) $token)"
    }
    Write-Host "[evidence-event] pushed=$repo branch=$BranchName"

    if ($OpenPullRequest) {
      $title = "Add portfolio evidence notes"
      $body = "Adds student evidence notes and screenshot capture guidance for the SiteSpy portfolio."
      $prOutput = (& gh pr create --repo $repo --base main --head "$githubUsername`:$BranchName" --title "$title" --body "$body" 2>&1)
      if ($LASTEXITCODE -eq 0) {
        $result.pullRequest = (($prOutput | Out-String).Trim())
        Write-Host "[evidence-event] pull_request_created=$($result.pullRequest)"
      } else {
        $viewOutput = (& gh pr view "$BranchName" --repo $repo --json url --jq ".url" 2>&1)
        if ($LASTEXITCODE -eq 0) {
          $result.pullRequest = (($viewOutput | Out-String).Trim())
          Write-Host "[evidence-event] pull_request_exists=$($result.pullRequest)"
        } else {
          throw "PR creation failed for $repo`: $(Redact-Text (($prOutput | Out-String).Trim()) $token)"
        }
      }
    }

    $result.status = "success"
    $result.reason = "evidence branch pushed"
  }
  catch {
    $message = Redact-Text ([string]$_.Exception.Message) $token
    Write-Host "FAILED: $message"
    $result.status = "failed"
    $result.reason = $message
  }
  finally {
    if ([string]::IsNullOrWhiteSpace($oldGhToken)) {
      Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
    } else {
      $env:GH_TOKEN = $oldGhToken
    }
  }

  $results += [pscustomobject]$result
}

$success = @($results | Where-Object { $_.status -eq "success" }).Count
$skipped = @($results | Where-Object { $_.status -eq "skipped" }).Count
$failed = @($results | Where-Object { $_.status -eq "failed" }).Count

Write-Host ""
Write-Host "Evidence PR Summary"
Write-Host "Total: $($results.Count)"
Write-Host "Success: $success"
Write-Host "Skipped: $skipped"
Write-Host "Failed: $failed"

if ($failed -gt 0) {
  exit 1
}
