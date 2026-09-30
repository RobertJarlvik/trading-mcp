$repo = 'C:\src\trading-mcp'
$venv = Join-Path $repo 'venv'

if (-not (Test-Path $venv)) {
    python -m venv $venv
}

$pip = Join-Path $venv 'Scripts\pip.exe'
$py = Join-Path $venv 'Scripts\python.exe'

& $pip install --upgrade pip
& $pip install -r (Join-Path $repo 'requirements.txt')
& $py (Join-Path $repo 'scripts\index_pdfs.py')
