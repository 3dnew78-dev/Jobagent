# Remote Job Agent - Phase 1: Telegram Bot

This is Phase 1 of 6. It's intentionally small: a working Telegram bot that
registers you and responds to a few commands. Nothing about jobs, CVs, or
ranking yet - that's Phases 2-6, built on top of this same skeleton.

## What's here

- `bot.py` - entry point, starts the bot
- `config.py` - loads your bot token + the single-user gate from `.env`
- `database.py` - SQLite schema (a `users` table, ready for many users later)
- `handlers.py` - `/start`, `/help`, `/status` commands
- `requirements.txt`, `.env.example`

## Setup (10 minutes)

1. **Create your bot**
   - Open Telegram, message **@BotFather**, send `/newbot`, follow the
     prompts. You'll get a token that looks like `123456789:AAExxxxxxx`.

2. **Get your numeric Telegram ID**
   - Message **@userinfobot** on Telegram - it replies with your numeric ID.

3. **Install dependencies**
   ```bash
   cd job_agent_bot
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in `BOT_TOKEN` (from step 1) and
   `ALLOWED_TELEGRAM_ID` (from step 2).

5. **Run it**
   ```bash
   python bot.py
   ```

6. **Test it** - open your bot in Telegram and send:
   - `/start` - registers you, shows the roadmap
   - `/status` - shows which phases are live (only Phase 1 for now)
   - `/help` - lists commands

If `/start` replies with the roadmap message, Phase 1 is done and verified.

## Why it's built this way

- **Single-user gate, multi-user schema.** `ALLOWED_TELEGRAM_ID` in `.env`
  is the *only* thing restricting this to you. The database schema already
  keys everything off `users.id`, not "you" specifically - so opening this
  to more people later is deleting one line from `.env`, not a rewrite.
- **SQLite, not Postgres.** Zero setup, one file, perfectly fine through
  Phase 6 for a single user. Swapping to Postgres later is a config change
  in `database.py`, not a redesign, because access already goes through
  `get_conn()` in one place.

## Next: Phase 2

Profile / CV upload - the "truth store" that every later phase (job
matching, CV tailoring, cover letters) is only ever allowed to draw facts
from, never invent beyond.
