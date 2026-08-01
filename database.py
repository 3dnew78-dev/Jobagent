import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from config import DB_PATH

# NOTE ON SCHEMA DESIGN:
# Even though only one person uses this bot right now, every table is keyed off
# `users.id`, not hardcoded to "you". That's the only thing that matters for
# scaling later - the schema doesn't change when Phase 2+ adds more users,
# only the ALLOWED_TELEGRAM_ID gate in config.py goes away.

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id     INTEGER UNIQUE NOT NULL,
    username        TEXT,
    first_name      TEXT,
    created_at      TEXT NOT NULL,
    profile_complete INTEGER NOT NULL DEFAULT 0
);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def get_or_create_user(telegram_id: int, username, first_name) -> sqlite3.Row:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        if row:
            return row

        conn.execute(
            """
            INSERT INTO users (telegram_id, username, first_name, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, username, first_name, datetime.now(timezone.utc).isoformat()),
        )
        return conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
