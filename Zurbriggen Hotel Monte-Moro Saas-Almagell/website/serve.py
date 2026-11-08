#!/usr/bin/env python3
"""Vorschau-Server Hotel Monte-Moro (Designstudie, nur lokal). python3 serve.py [port]  →  http://127.0.0.1:8947/
Eigener Prozess, kein Zwischenspeichern, antwortet nur dem eigenen Rechner."""
import os, sys, json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8947

class H(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a): pass
    def send_error(self, code, message=None, explain=None):
        """Unbekannte Adressen bekommen die eigene Seite 404.html (Pflicht-Liste 9d, Punkt 13)."""
        if code == 404 and self.command in ('GET', 'HEAD') and os.path.exists('404.html'):
            body = open('404.html', 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers()
            if self.command == 'GET':
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)
    def do_POST(self):
        """Anfrage-Fenster (assets/js/anfrage.js): legt die Anfrage im Eingang dieser Vorschau ab, nichts geht an das Haus."""
        if self.path != '/api/anfragen':
            self.send_error(404); return
        n = min(int(self.headers.get('Content-Length') or 0), 20000)
        try:
            daten = json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            self.send_error(400); return
        os.makedirs('_dienste', exist_ok=True)
        with open(os.path.join('_dienste', 'anfragen.jsonl'), 'a', encoding='utf-8') as f:
            f.write(json.dumps(daten, ensure_ascii=False) + '\n')
        self.send_response(204); self.end_headers()

if __name__ == '__main__':
    print(f'Hotel Monte-Moro · http://127.0.0.1:{PORT}/')
    ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
