# One-click start for Ascension AI native on Windows.
param(
  [int]$Port = 8000,
  [string]$ModelProfile = $env:ASCENSION_MODEL_PROFILE
)
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot
if (-not $repo) { $repo = (Get-Location).Path }

# Load ascension.env into process-scoped environment variables
$envPath = Join-Path $repo 'ascension.env'
if (Test-Path $envPath) {
  Get-Content $envPath | ForEach-Object {
    if ($_ -match '^\s*([^#\s][^=]*)\s*=\s*(.*?)\s*$') {
      [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
  }
}

if ($ModelProfile) { $env:ASCENSION_MODEL_PROFILE = $ModelProfile }
if (-not $env:ASCENSION_MODEL_PROFILE) { $env:ASCENSION_MODEL_PROFILE = 'pro_v19' }

$python = Join-Path $repo '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
  throw "Python virtual environment not found. Run setup.ps1 first."
}

Write-Host "Starting Ascension AI ($env:ASCENSION_MODEL_PROFILE) on http://localhost:$Port"
& $python -m uvicorn src.serving.api:app --host 0.0.0.0 --port $Port
