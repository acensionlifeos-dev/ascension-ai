$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\Brandon\ascension-ai'

# Check if the server is already running
$running = (Test-NetConnection -ComputerName '127.0.0.1' -Port 8000 -WarningAction SilentlyContinue).TcpTestSucceeded

if (-not $running) {
    # Start the server in a hidden background window
    Start-Process -FilePath 'powershell.exe' `
        -ArgumentList '-ExecutionPolicy', 'Bypass', '-File', "$repo\start.ps1" `
        -WorkingDirectory $repo `
        -WindowStyle Hidden

    # Wait up to 60 seconds for the health check to pass
    $ready = $false
    for ($i = 0; $i -lt 60; $i++) {
        Start-Sleep -Seconds 1
        try {
            $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/health' -UseBasicParsing -TimeoutSec 5
            if ($r.StatusCode -eq 200) { $ready = $true; break }
        } catch {}
    }

    if (-not $ready) {
        Read-Host 'The Ascension AI server did not start. Press Enter to close this window.'
        exit 1
    }
}

# Find the browser
$edge = (Get-ChildItem -Path 'C:\Program Files','C:\Program Files (x86)' -Filter 'msedge.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
$chrome = (Get-ChildItem -Path 'C:\Program Files','C:\Program Files (x86)' -Filter 'chrome.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
$browser = if ($edge) { $edge } elseif ($chrome) { $chrome } else { $null }

if (-not $browser) {
    Read-Host 'Could not find Microsoft Edge or Google Chrome. Press Enter to close.'
    exit 1
}

# Use a clean Edge profile so the UI always loads fresh
$userData = "$repo\.edge-data"
if (Test-Path $userData) { Remove-Item -Recurse -Force -Path $userData -ErrorAction SilentlyContinue }

# Open the chat in app mode (looks like a desktop app) with a cache-busting query
$cache = (Get-Date -Format 'yyyyMMddHHmmss')
Start-Process -FilePath $browser -ArgumentList "--user-data-dir=$userData", "--app=http://127.0.0.1:8000?v=$cache"
