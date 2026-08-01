from telegram import Update
from telegram.ext import ContextTypes

from config import ALLOWED_TELEGRAM_ID
from database import get_or_create_user


def is_allowed(telegram_id: int) -> bool:
    """Phase 1-6 gate: only you can use the bot. Unset ALLOWED_TELEGRAM_ID
    in .env later to open it up - no code change needed."""
    if ALLOWED_TELEGRAM_ID is None:
        return True
    return telegram_id == ALLOWED_TELEGRAM_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not is_allowed(user.id):
        await update.message.reply_text(
            "This bot is currently in private testing. Ask the owner for access."
        )
        return

    get_or_create_user(user.id, user.username, user.first_name)

    await update.message.reply_text(
        f"Hey {user.first_name} 👋 I'm your Remote Job Agent.\n\n"
        "Here's the build plan:\n"
        "1️⃣ Telegram bot (you're talking to it right now ✅)\n"
        "2️⃣ Profile / CV upload - your truth store (next)\n"
        "3️⃣ Search legitimate remote job boards\n"
        "4️⃣ Rank jobs by your real odds of getting hired\n"
        "5️⃣ Draft tailored, 100% truthful CVs + cover letters\n"
        "6️⃣ Track applications + coach you for interviews\n\n"
        "Right now all I can do is register you and say hi. "
        "Send /status anytime to see what's live."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_allowed(user.id):
        return

    await update.message.reply_text(
        "Available commands:\n"
        "/start - register and get the intro\n"
        "/help - show this message\n"
        "/status - see which phases are built so far"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_allowed(user.id):
        return

    row = get_or_create_user(user.id, user.username, user.first_name)
    profile_state = "✅ complete" if row["profile_complete"] else "⏳ Phase 2 - not built yet"

    await update.message.reply_text(
        f"Registered since: {row['created_at'][:10]}\n\n"
        f"1️⃣ Telegram bot: ✅ live\n"
        f"2️⃣ Profile / truth store: {profile_state}\n"
        f"3️⃣ Job search: ⏳ Phase 3 - not built yet\n"
        f"4️⃣ Ranking: ⏳ Phase 4 - not built yet\n"
        f"5️⃣ CV + cover letter generation: ⏳ Phase 5 - not built yet\n"
        f"6️⃣ Application tracker + interview coach: ⏳ Phase 6 - not built yet"
    )
