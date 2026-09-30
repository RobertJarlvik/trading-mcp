# trading-mcp

Detta repository används som lokal MCP-datakälla för GitHub Copilot CLI. Repos struktur:

- pdfs/      — PDF-dokument (kopierade från C:\tmp\trading)
- scripts/   — hjälpskript (indexering och server)
- data/      — genererad index (index.json)

Använd scripts/run_index.ps1 för att skapa ett virtuellt env och indexera PDF-filerna.
Starta MCP-servern med antingen Python- eller C#-servern. Efter att index.json är skapat (scripts/run_index.ps1) kan du starta:

- Python (snabb test): scripts\run_server.ps1
- C# (rekommenderat, produktionskvalitet): scripts\run_dotnet_server.ps1  (kräver .NET 7 SDK)

Endpoints (både Python- och C#-servern implementerar samma API):
- GET /          — grundinfo
- GET /documents — lista dokument (id, filename)
- GET /document/<id> — hämta dokumenttext
- GET /search?q=... — sök i indexet, returnerar snippet och score

C#-servern finns i dotnet/ (TradingMcp.csproj, Program.cs). Kör scripts\run_dotnet_server.ps1 för att bygga och köra på http://127.0.0.1:8000.
