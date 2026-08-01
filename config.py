import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Single-user MVP gate ---
# During Phase 1-6 you're the only user, so we only respond to your Telegram
# numeric ID. To open the bot to more people later, just delete ALLOWED_TELEGRAM_ID
# from your .env (or set it blank) — is_allowed() in handlers.py already treats
# "unset" as "open to everyone", no code change needed.
_raw_allowed_id = os.getenv("ALLOWED_TELEGRAM_ID")
ALLOWED_TELEGRAM_ID = int(_raw_allowed_id) if _raw_allowed_id else None

DB_PATH = os.getenv("DB_PATH", "job_agent.db")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Copy .env.example to .env and fill in your bot token."
    )
