Python index scripts

Files:
- index_pdfs.py        — older indexer that extracts text and writes data/index.json
- reindex_trading.py   — canonical reindex script (argparse, accepts --source and --outdir)

Usage examples:
- From PowerShell (uses repo venv):
    & .\venv\Scripts\python.exe .\scripts\reindex_trading.py -s "C:\tmp\trading" -o ".\data"

- Using run_index.ps1 (creates venv and runs index_pdfs.py):
    .\scripts\run_index.ps1

Requirements: PyPDF2 (see requirements.txt)

Notes:
- reindex_trading.py also writes data/index_stats.json with keys {documents, pages}.
- Keep these scripts for reproducibility and reindexing when new PDFs are added.
