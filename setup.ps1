# One-time setup for Ascension AI native on Windows.
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
if (-not $env:ASCENSION_MODEL_PROFILE) { $env:ASCENSION_MODEL_PROFILE = 'pro_v19' }

# Create a Python virtual environment if it does not exist
$venvPath = Join-Path $repo '.venv'
if (-not (Test-Path $venvPath)) {
  Write-Host "Creating virtual environment..."
  python -m venv $venvPath
}

# Install Python dependencies
$pip = Join-Path $venvPath 'Scripts\pip.exe'
Write-Host "Installing Python requirements..."
& $pip install -r (Join-Path $repo 'requirements.txt')

# Install Windows control dependencies
Write-Host "Installing Windows control dependencies..."
& $pip install pyautogui

# Install desktop and credential support
Write-Host "Installing desktop and credential support..."
& $pip install pywebview keyring

# Download the default local model (pro_v19)
Write-Host "Downloading the v19 merged model (this may take a while)..."
$python = Join-Path $venvPath 'Scripts\python.exe'
& $python (Join-Path $repo 'scripts\download_model.py')

Write-Host "Setup complete. Run start.ps1 to launch."
