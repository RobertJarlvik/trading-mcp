import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INDEX_PATH = os.path.join(REPO_ROOT, 'data', 'index.json')

print('Loading index from', INDEX_PATH)
try:
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        INDEX = json.load(f)
except Exception as e:
    print('Failed to load index.json:', e)
    INDEX = []

# assign integer ids
for i, d in enumerate(INDEX):
    d.setdefault('id', i)

@app.route('/')
def info():
    return jsonify({
        'name': 'trading-mcp',
        'documents': len(INDEX)
    })

@app.route('/documents')
def list_docs():
    return jsonify([{'id': d.get('id'), 'filename': d.get('filename')} for d in INDEX])

@app.route('/document/<int:doc_id>')
def get_doc(doc_id):
    doc = next((d for d in INDEX if d.get('id') == doc_id), None)
    if not doc:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'id': doc.get('id'), 'filename': doc.get('filename'), 'text': doc.get('text', '')})

def snippet(text, q, radius=120):
    idx = text.lower().find(q.lower())
    if idx == -1:
        return text[:radius*2] + ('...' if len(text) > radius*2 else '')
    start = max(0, idx - radius)
    end = min(len(text), idx + len(q) + radius)
    prefix = '...' if start > 0 else ''
    suffix = '...' if end < len(text) else ''
    return prefix + text[start:end].strip() + suffix

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    results = []
    for d in INDEX:
        txt = d.get('text', '') or ''
        if q.lower() in txt.lower():
            count = txt.lower().count(q.lower())
            results.append({'id': d.get('id'), 'filename': d.get('filename'), 'score': count, 'snippet': snippet(txt, q)})
    results.sort(key=lambda r: r['score'], reverse=True)
    limit = int(request.args.get('limit', 10))
    return jsonify(results[:limit])

if __name__ == '__main__':
    host = os.environ.get('MCP_HOST', '127.0.0.1')
    port = int(os.environ.get('MCP_PORT', '8000'))
    print(f'Starting server on {host}:{port} ...')
    app.run(host=host, port=port)
