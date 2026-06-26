"""Shared helpers for the Cyber & Responsible AI Assurance Radar pipeline.

Stdlib-only except PyYAML (see requirements.txt). Designed to run unattended in
CI and locally on Windows. All file I/O is UTF-8.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml  # PyYAML

# --- Paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
DATA = ROOT / "data"
DAILY = DATA / "daily"
WEEKLY = DATA / "weekly"
HISTORY = DATA / "history"
CACHE = DATA / "_cache"
DASHBOARD = ROOT / "dashboard"
SOURCES_YAML = ROOT / "sources.yaml"
STANDARDS_YAML = ROOT / "standards.yaml"

SEEN_FILE = DATA / "seen_items.json"
HEALTH_FILE = DATA / "source_health.json"
DASHBOARD_JSON = DATA / "dashboard.json"

TZ = ZoneInfo("Australia/Melbourne")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


# --- Time --------------------------------------------------------------------
def now() -> datetime:
    return datetime.now(TZ)


def now_iso() -> str:
    return now().replace(microsecond=0).isoformat()


def today_str() -> str:
    return now().strftime("%Y-%m-%d")


# --- IO ----------------------------------------------------------------------
def ensure_dirs() -> None:
    for d in (DATA, DAILY, WEEKLY, HISTORY, CACHE, DASHBOARD):
        d.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: Path, obj) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=False),
        encoding="utf-8",
    )


def load_yaml(path: Path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


# --- Network -----------------------------------------------------------------
def http_get(url: str, timeout: int = 20) -> bytes:
    """Fetch a URL with a browser-like UA. Raises urllib.error on failure."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": (
                "application/rss+xml,application/atom+xml,application/xml,"
                "text/html;q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "en-AU,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


# --- Identity / text ---------------------------------------------------------
def stable_id(url: str, title: str = "") -> str:
    basis = (url or title or "").strip().lower()
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def strip_html(text: str) -> str:
    if not text:
        return ""
    # unescape a few common entities, then drop tags and collapse whitespace
    import html as _html

    text = _html.unescape(text)
    text = _TAG_RE.sub(" ", text)
    return _WS_RE.sub(" ", text).strip()


def truncate(text: str, limit: int = 320) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;: ") + "…"


def parse_date(raw: str) -> str:
    """Best-effort -> YYYY-MM-DD. Returns '' if unparseable."""
    if not raw:
        return ""
    raw = raw.strip()
    # RFC822 (RSS pubDate)
    try:
        from email.utils import parsedate_to_datetime

        dt = parsedate_to_datetime(raw)
        if dt:
            return dt.date().isoformat()
    except (TypeError, ValueError, IndexError):
        pass
    # ISO 8601 (Atom)
    try:
        iso = raw.replace("Z", "+00:00")
        return datetime.fromisoformat(iso).date().isoformat()
    except ValueError:
        pass
    # Bare date
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if m:
        return m.group(0)
    return ""


def log(msg: str) -> None:
    print(f"[{now().strftime('%H:%M:%S')}] {msg}", flush=True)
