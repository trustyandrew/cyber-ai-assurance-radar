"""Local dashboard server: static files + feedback + on-demand newsletter.

  GET  /feedback.json  -> current votes (data/feedback.json)
  POST /feedback       -> {"id","vote":"up"|"down"|"none","item":{...}} updates votes
  POST /newsletter     -> {"range":"since_last"|"week"|"month"|"quarter"}
                          builds a copy/paste newsletter from 👍 picks in that range

Votes store {vote, at, item-snapshot} so the newsletter can include picks even after
they age out of the feeds. Ranges filter by up-vote time. "since_last" uses the
last-built time in data/newsletter_state.json and advances it only when that range is
built. Local-only (127.0.0.1). Run via the 'dashboard' launch config, or:
    python src/serve_dashboard.py
"""
from __future__ import annotations

import json
import os
from datetime import timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import radar_common as rc
import render_newsletter

PORT = int(os.environ.get("RADAR_PORT", "4178"))
RANGE_DAYS = {"week": 7, "month": 30, "quarter": 90}


def _votes() -> dict:
    return rc.load_json(rc.FEEDBACK_FILE, {})


def _nl_state() -> dict:
    return rc.load_json(rc.NEWSLETTER_STATE, {"last_newsletter_at": None})


def _selected_ups(range_key: str) -> list:
    """Up-voted item snapshots whose up-vote time falls in the requested range."""
    if range_key in RANGE_DAYS:
        cutoff = (rc.now() - timedelta(days=RANGE_DAYS[range_key])).isoformat()
    else:  # since_last
        cutoff = _nl_state().get("last_newsletter_at") or ""
    out = []
    for rec in _votes().values():
        if not isinstance(rec, dict) or rec.get("vote") != "up":
            continue
        at = rec.get("at", "")
        if cutoff and at and at < cutoff:
            continue
        if rec.get("item"):
            out.append(rec["item"])
    return out


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(rc.DASHBOARD), **k)

    def end_headers(self):  # no-store so the browser never serves stale JS
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code: int, obj) -> None:
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):  # noqa: N802
        if self.path.rstrip("/") in ("/feedback", "/feedback.json"):
            self._json(200, _votes())
            return
        return super().do_GET()

    def do_POST(self):  # noqa: N802
        path = self.path.rstrip("/")
        try:
            req = self._body()
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "bad request"})
            return
        if path == "/feedback":
            self._feedback(req)
        elif path == "/newsletter":
            self._newsletter(req)
        else:
            self._json(404, {"error": "not found"})

    def _feedback(self, req: dict) -> None:
        iid, vote, item = req.get("id"), req.get("vote"), req.get("item")
        votes = _votes()
        if vote in ("up", "down") and iid:
            rec = {"vote": vote, "at": rc.now_iso()}
            if vote == "up" and item:
                rec["item"] = item
            votes[iid] = rec
        elif iid in votes:
            del votes[iid]
        rc.save_json(rc.FEEDBACK_FILE, votes)
        self._json(200, {"ok": True, "id": iid, "vote": vote, "count": len(votes)})

    def _newsletter(self, req: dict) -> None:
        range_key = req.get("range", "since_last")
        items = _selected_ups(range_key)
        md, theme = render_newsletter.compose_newsletter(items, rc.today_str())
        if range_key == "since_last":
            st = _nl_state()
            st["last_newsletter_at"] = rc.now_iso()
            rc.save_json(rc.NEWSLETTER_STATE, st)
        self._json(200, {"md": md, "count": len(items), "theme": theme, "range": range_key})

    def log_message(self, *a):  # quiet
        pass


if __name__ == "__main__":
    ThreadingHTTPServer.allow_reuse_address = True
    with ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"Radar dashboard on http://localhost:{PORT}/  (feedback + newsletter)")
        srv.serve_forever()
