"""
Reindex trading PDFs into index.json and index_stats.json.
Usage:
  python reindex_trading.py --source "C:\tmp\trading" --outdir "C:\src\trading-mcp\data"

Produces:
  - index.json : list of {filename, path, pages, text}
  - index_stats.json : {documents, pages}

Requires: PyPDF2
"""
import os
import json
import argparse
from PyPDF2 import PdfReader


def extract_text_and_pages(path):
    reader = PdfReader(path)
    pages = len(reader.pages)
    parts = []
    for p in reader.pages:
        try:
            parts.append(p.extract_text() or "")
        except Exception:
            parts.append("")
    return pages, "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Reindex PDFs into JSON index")
    parser.add_argument('--source', '-s', default=r'C:\tmp\trading', help='Source folder with PDFs')
    parser.add_argument('--outdir', '-o', default=r'C:\src\trading-mcp\data', help='Output folder for index.json')
    parser.add_argument('--pattern', '-p', default='*.pdf', help='Filename glob pattern')
    args = parser.parse_args()

    src = os.path.abspath(args.source)
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    files = sorted([f for f in os.listdir(src) if f.lower().endswith('.pdf')])
    index = []
    total_pages = 0

    for fname in files:
        path = os.path.join(src, fname)
        try:
            pages, text = extract_text_and_pages(path)
            index.append({'filename': fname, 'path': path, 'pages': pages, 'text': text})
            total_pages += pages
            print(f"Indexed: {fname} ({pages} pages)")
        except Exception as e:
            print(f"Warning: failed to read {fname}: {e}")

    outpath = os.path.join(outdir, 'index.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    stats = {'documents': len(index), 'pages': total_pages}
    with open(os.path.join(outdir, 'index_stats.json'), 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"Wrote index with {len(index)} documents and {total_pages} total pages to {outpath}")


if __name__ == '__main__':
    main()
