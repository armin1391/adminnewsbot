# ==========================
# Admin Panel
# Version 1.0.0
# ==========================

from bale import Message

from client import bot
from keyboards import admin_menu


@bot.event
async def on_message(message: Message):

    if message.from_user is None:
        return

    if message.content != "🛠 پنل مدیریت":
        return

    await message.reply(
        "🛠 پنل مدیریت\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید.",
        components=admin_menu()
    )	