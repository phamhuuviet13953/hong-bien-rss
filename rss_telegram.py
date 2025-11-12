# rss_telegram.py
# RSS (WordPress) -> Telegram, chạy liên tục, chống trùng lặp, dùng ETag/Last-Modified.
# Yêu cầu: pip install feedparser httpx tenacity python-dotenv aiosqlite

import asyncio
import os
import time
import hashlib
import logging
from typing import Optional, Tuple, List
import feedparser
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt
from contextlib import asynccontextmanager
import aiosqlite

# ================== CẤU HÌNH ==================
# (1) Telegram — đã gắn sẵn token & chat_id của bạn
BOT_TOKEN = "8012634282:AAESreFtJToDID3HyptNtcy_rQdFFm4Jo30"
CHAT_ID   = "-5026178584"   # nhóm "Hóng biến - RSS" (lưu ý dấu âm)

# (2) Danh sách RSS WordPress (thêm của bạn vào đây)
FEEDS: List[str] = [
    "https://honghot.click/feed/",
]

# (3) Chu kỳ quét (giây)
POLL_INTERVAL = 90

# (4) DB lưu trạng thái đã gửi
DB_PATH = "rss_state.sqlite3"

# (5) Định dạng thông báo
def format_message(title: str, url: str, source: str) -> str:
    safe_title = (
        title.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .strip()
    )
    return f"📰 <b><a href=\"{url}\">{safe_title}</a></b>\n📌 Nguồn: <i>{source}</i>"

# ================== LOGGING ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ================== VALIDATION ==================
def validate_config():
    if not BOT_TOKEN or ":" not in BOT_TOKEN:
        raise SystemExit("Thiếu/sai BOT_TOKEN.")
    if not CHAT_ID:
        raise SystemExit("Thiếu CHAT_ID.")
    # Cảnh báo nhầm chat_id = id của bot
    bot_id_from_token = BOT_TOKEN.split(":", 1)[0]
    if CHAT_ID == bot_id_from_token:
        raise SystemExit(
            f"CHAT_ID đang là ID BOT ({CHAT_ID}). Hãy dùng ID nhóm/kênh (thường -100...) hoặc @username kênh."
        )
validate_config()

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ================== DB ==================
INIT_SQL = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS seen_items (
    feed_url TEXT NOT NULL,
    entry_id TEXT NOT NULL,
    first_seen_ts INTEGER NOT NULL,
    PRIMARY KEY (feed_url, entry_id)
);
CREATE TABLE IF NOT EXISTS feed_state (
    feed_url TEXT PRIMARY KEY,
    etag TEXT,
    modified TEXT
);
"""

@asynccontextmanager
async def open_db():
    db = await aiosqlite.connect(DB_PATH)
    await db.executescript(INIT_SQL)
    await db.commit()
    try:
        yield db
    finally:
        await db.close()

async def get_seen(db, feed_url: str, entry_id: str) -> bool:
    async with db.execute(
        "SELECT 1 FROM seen_items WHERE feed_url=? AND entry_id=?",
        (feed_url, entry_id),
    ) as cur:
        return await cur.fetchone() is not None

async def mark_seen(db, feed_url: str, entry_id: str):
    ts = int(time.time())
    await db.execute(
        "INSERT OR IGNORE INTO seen_items(feed_url, entry_id, first_seen_ts) VALUES (?,?,?)",
        (feed_url, entry_id, ts),
    )

async def get_feed_state(db, feed_url: str) -> Tuple[Optional[str], Optional[str]]:
    async with db.execute(
        "SELECT etag, modified FROM feed_state WHERE feed_url=?",
        (feed_url,),
    ) as cur:
        row = await cur.fetchone()
        if row:
            return row[0], row[1]
        return None, None

async def set_feed_state(db, feed_url: str, etag: Optional[str], modified: Optional[str]):
    await db.execute(
        "INSERT INTO feed_state(feed_url, etag, modified) VALUES (?,?,?) "
        "ON CONFLICT(feed_url) DO UPDATE SET etag=excluded.etag, modified=excluded.modified",
        (feed_url, etag, modified),
    )

def entry_identity(entry) -> str:
    if getattr(entry, "id", None):
        return entry.id
    if getattr(entry, "guid", None):
        return entry.guid
    if getattr(entry, "link", None):
        return entry.link
    key = (getattr(entry, "title", "") + "|" + getattr(entry, "published", "")).encode("utf-8", "ignore")
    return hashlib.sha1(key).hexdigest()

def get_source(feed_url: str, parsed) -> str:
    if getattr(parsed, "feed", None) and getattr(parsed.feed, "title", None):
        return parsed.feed.title
    try:
        return feed_url.split("/")[2]
    except Exception:
        return feed_url

@retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(5))
async def telegram_send(session: httpx.AsyncClient, text: str):
    resp = await session.post(
        TELEGRAM_API,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=30.0,
    )
    resp.raise_for_status()

async def fetch_and_parse_feed(session: httpx.AsyncClient, url: str, etag: Optional[str], modified: Optional[str]):
    headers = {}
    if etag:
        headers["If-None-Match"] = etag
    if modified:
        headers["If-Modified-Since"] = modified

    resp = await session.get(url, headers=headers, timeout=30.0)
    if resp.status_code == 304:
        return None, etag, modified

    resp.raise_for_status()
    content = resp.content

    parsed = feedparser.parse(content)
    new_etag = resp.headers.get("ETag") or getattr(parsed, "etag", None)
    new_modified = resp.headers.get("Last-Modified") or getattr(parsed, "modified", None)

    return parsed, new_etag, new_modified

async def process_feed(db, session: httpx.AsyncClient, feed_url: str):
    try:
        etag, modified = await get_feed_state(db, feed_url)
        result = await fetch_and_parse_feed(session, feed_url, etag, modified)

        if result is None:
            logging.info(f"[{feed_url}] 304 Not Modified")
            return

        parsed, new_etag, new_modified = result
        if parsed is None:
            logging.info(f"[{feed_url}] No content")
            return

        source_name = get_source(feed_url, parsed)
        entries = parsed.entries or []

        def entry_ts(e):
            return getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None) or time.gmtime(0)
        entries.sort(key=entry_ts)

        new_count = 0
        for e in entries:
            entry_id = entry_identity(e)
            if await get_seen(db, feed_url, entry_id):
                continue

            title = getattr(e, "title", "(Không có tiêu đề)").strip()
            link = getattr(e, "link", "").strip()
            if not link:
                await mark_seen(db, feed_url, entry_id)
                continue

            msg = format_message(title, link, source_name)
            await telegram_send(session, msg)
            await mark_seen(db, feed_url, entry_id)
            new_count += 1

        await set_feed_state(db, feed_url, new_etag, new_modified)
        await db.commit()
        logging.info(f"[{feed_url}] sent: {new_count} new")
    except Exception as exc:
        logging.exception(f"[{feed_url}] ERROR: {exc}")

async def main():
    logging.info("Starting RSS → Telegram worker...")
    async with open_db() as db:
        async with httpx.AsyncClient(follow_redirects=True, headers={"User-Agent": "rss-telegram/1.0"}) as session:
            while True:
                tasks = [process_feed(db, session, url) for url in FEEDS]
                await asyncio.gather(*tasks)
                await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
