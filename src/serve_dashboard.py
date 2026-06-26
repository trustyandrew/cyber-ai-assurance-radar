"""Local dashboard server with a feedback write-endpoint.

Serves the static dashboard/ folder AND lets the page persist 👍/👎 votes:
  GET  /feedback.json   -> current votes (data/feedback.json)
  POST /feedback        -> {"id": "...", "vote": "up"|"down"|"none"} updates the file

Votes are consumed by the pipeline (render_dashboard / render_newsletter): "down"
items are hidden everywhere and excluded from the newsletter; "up" items are forced
newsletter candidates. Local-only (binds 127.0.0.1). Run via the 'dashboard' launch
config or: python src/serve_dashboard.py
"""
from __future__ import annotations

import json
import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = ROOT / "dashboard"
FEEDBACK = ROOT / "data" / "feedback.json"
PORT = int(os.environ.get("RADAR_PORT", "4178"))


def _load() -> dict:
    try:
        return json.loads(FEEDBACK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(DASH), **k)

    def end_headers(self):  # no-store on every response so the browser never serves stale JS
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _send(self, code: int, body: str, ctype: str = "application/json") -> None:
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):  # noqa: N802
        if self.path.rstrip("/") in ("/feedback", "/feedback.json"):
            self._send(200, json.dumps(_load(), ensure_ascii=False))
            return
        return super().do_GET()

    def do_POST(self):  # noqa: N802
        if self.path.rstrip("/") != "/feedback":
            self._send(404, '{"error":"not found"}')
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n) or b"{}")
            iid, vote = req.get("id"), req.get("vote")
        except (ValueError, json.JSONDecodeError):
            self._send(400, '{"error":"bad request"}')
            return
        fb = _load()
        if vote in ("up", "down") and iid:
            fb[iid] = vote
        elif iid in fb:  # "none"/clear
            del fb[iid]
        FEEDBACK.parent.mkdir(parents=True, exist_ok=True)
        FEEDBACK.write_text(json.dumps(fb, indent=2, ensure_ascii=False), encoding="utf-8")
        self._send(200, json.dumps({"ok": True, "id": iid, "vote": vote, "count": len(fb)}))

    def log_message(self, *a):  # quiet
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"Radar dashboard on http://localhost:{PORT}/  (feedback enabled)")
        srv.serve_forever()
