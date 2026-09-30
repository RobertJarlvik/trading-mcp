# trading-mcp

Detta repository används som lokal MCP-datakälla för GitHub Copilot CLI. Repos struktur:

- pdfs/      — PDF-dokument (kopierade från C:\tmp\trading)
- scripts/   — hjälpskript (indexering och server)
- data/      — genererad index (index.json)

Använd scripts/run_index.ps1 för att skapa ett virtuellt env och indexera PDF-filerna (behöver Python).

Notera: Python-scripts (scripts/index_pdfs.py och scripts/run_index.ps1) behålls i repot för att möjliggöra omindexering av data. requirements.txt listar Python-beroenden (PyPDF2).

Starta MCP-servern med C#-servern (rekommenderat). Efter att index.json är skapat kör scripts\run_dotnet_server.ps1 för att bygga och köra på http://127.0.0.1:8000 (kräver .NET 7 SDK).

Endpoints (C#-servern implementerar följande API):
- GET /          — grundinfo
- GET /documents — lista dokument (id, filename)
- GET /document/<id> — hämta dokumenttext
- GET /search?q=... — sök i indexet, returnerar snippet och score

C#-servern finns i dotnet/ (TradingMcp.csproj, Program.cs). Kör scripts\run_dotnet_server.ps1 för att bygga och köra på http://127.0.0.1:8000.

Empirisk indexstatistik

Denna MCP-server använder nu ett noggrant genererat index baserat på PDF-samlingen i C:\tmp\trading. Indexet innehåller 38 dokument och totalt 10 957 sidor (extraherade och bearbetade). Det innebär att servern har tillgång till över tiotusen sidor tradingmaterial — en omfattning och djup som gör sökningar och sammanfattningar både statistiskt meningsfulla och praktiskt användbara. Indexet kan återskapas med scripts/run_index.ps1 när nya dokument läggs till.
