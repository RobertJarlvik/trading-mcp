import os
import json
from PyPDF2 import PdfReader


def extract_text_from_pdf(path):
    try:
        reader = PdfReader(path)
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    except Exception as e:
        print(f"Warning: failed to read {path}: {e}")
        return ""


def main():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pdfs'))
    outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(outdir, exist_ok=True)
    index = []

    if not os.path.isdir(base):
        print(f"PDF folder not found: {base}")
        return

    for fname in sorted(os.listdir(base)):
        if not fname.lower().endswith('.pdf'):
            continue
        path = os.path.join(base, fname)
        print(f"Indexing: {fname}")
        text = extract_text_from_pdf(path)
        index.append({
            'filename': fname,
            'path': path,
            'text': text
        })

    outpath = os.path.join(outdir, 'index.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Wrote index with {len(index)} documents to {outpath}")


if __name__ == '__main__':
    main()
