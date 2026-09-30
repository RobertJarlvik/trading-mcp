$repo = 'C:\src\trading-mcp'
$venv = Join-Path $repo 'venv'
$py = Join-Path $venv 'Scripts\python.exe'

if (-not (Test-Path $py)) {
    Write-Output 'venv python not found; run scripts\run_index.ps1 first to create venv and install dependencies.'
    exit 1
}

Write-Output 'Starting MCP Flask server (host 127.0.0.1:8000)...'
& $py (Join-Path $repo 'scripts\server.py')
