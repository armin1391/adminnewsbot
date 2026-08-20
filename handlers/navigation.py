# ==========================
# Navigation Handler
# Version 1.1.1
# ==========================

from bale import Message

from client import bot
from keyboards import main_menu, channel_menu
from users import get_user
from states import get_state, clear_state


@bot.event
async def on_message(message: Message):

    if message.from_user is None:
        return

    user_id = message.from_user.id

    # ==========================
    # منوی اصلی
    # ==========================
    if message.content == "🏠 منوی اصلی":

        clear_state(user_id)

        await message.reply(
            "🏠 منوی اصلی\n\nلطفاً یکی از گزینه‌ها را انتخاب کنید.",
            components=main_menu()
        )

        return

    # ==========================
    # بازگشت
    # ==========================
    if message.content != "🔙 بازگشت":
        return

    state = get_state(user_id)

    # اگر داخل افزودن کانال بود
    if state.get("state") == "add_channel":

        clear_state(user_id)

        data = get_user(user_id)
        channels = data.get("channels", [])

        if not channels:

            text = (
                "📢 کانال‌های من\n\n"
                "شما هنوز هیچ کانالی ثبت نکرده‌اید.\n\n"
                "برای ثبت کانال جدید، از دکمه «➕ افزودن کانال جدید» استفاده کنید."
            )

        else:

            text = "📢 کانال‌های شما\n\n"

            for index, channel in enumerate(channels, start=1):
                text += f"{index}. {channel['id']}\n"

            text += f"\n\n📊 تعداد کانال‌ها: {len(channels)}/3"

            if len(channels) < 3:
                text += "\n\n➕ برای ثبت کانال جدید، از دکمه زیر استفاده کنید."
            else:
                text += "\n\n⚠️ شما حداکثر ۳ کانال ثبت کرده‌اید."

        await message.reply(
            text,
            components=channel_menu()
        )

        return

    # در بقیه صفحات → منوی اصلی
    clear_state(user_id)

    await message.reply(
        "🏠 منوی اصلی\n\nلطفاً یکی از گزینه‌ها را انتخاب کنید.",
        components=main_menu()
    )