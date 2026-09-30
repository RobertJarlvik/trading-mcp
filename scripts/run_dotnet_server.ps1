$project = 'C:\src\trading-mcp\dotnet'
if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Output 'dotnet SDK not found in PATH. Install .NET 7 SDK to run the C# server.'
    exit 1
}

Write-Output 'Building and running trading-mcp (C#) ...'
Push-Location $project
try {
    dotnet restore --verbosity minimal
    dotnet run --urls "http://127.0.0.1:8000" --no-launch-profile
} finally {
    Pop-Location
}
