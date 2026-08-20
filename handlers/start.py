# ==========================
# Start Handler
# Version 2.2.0
# ==========================

from bale import Message

from client import bot
from users import user_exists, add_user, get_user
from keyboards import main_menu

from force_join import (
    is_force_join_enabled,
    is_user_joined
)

from force_join_keyboard import force_join_keyboard


@bot.event
async def on_message(message: Message):

    if message.content != "/start":
        return

    user = message.from_user

    if not user_exists(user.id):
        add_user(
            user.id,
            user.first_name,
            user.username
        )

    # ==========================
    # Force Join
    # ==========================

    if is_force_join_enabled():

        if not is_user_joined(user.id):

            await message.reply(
                "⚠️ برای استفاده از ربات ابتدا در کانال زیر عضو شوید.\n\n"
                "پس از عضویت روی دکمه «✅ عضو شدم» بزنید.",
                components=force_join_keyboard()
            )

            return

    user_data = get_user(user.id)

    await message.reply(
        "🌹 به ربات AutoNewsBot خوش آمدید.\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید.",
        components=main_menu(
            is_admin=user_data.get("is_admin", False)
        )
    )