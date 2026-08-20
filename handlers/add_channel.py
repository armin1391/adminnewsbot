# ==========================
# Add Channel Handler
# Version 1.1.1
# ==========================

from bale import Message

from client import bot
from states import set_state, get_state, clear_state
from keyboards import back_menu
from users import add_channel
from handlers.channel import show_channels

BTN_ADD_CHANNEL = "➕ افزودن کانال جدید"


@bot.event
async def on_message(message: Message):

    if message.from_user is None:
        return

    user_id = message.from_user.id

    # دریافت آیدی کانال
    if get_state(user_id)["state"] == "add_channel":

        channel = message.content.strip()

        if not channel.startswith("@"):
            await message.reply(
                "❌ آیدی کانال باید با @ شروع شود.",
                components=back_menu()
            )
            return

        result = add_channel(
            user_id,
            channel
        )

        if not result:
            await message.reply(
                "❌ این کانال قبلاً ثبت شده یا سقف ۳ کانال پر شده است.",
                components=back_menu()
            )
            return

        clear_state(user_id)

        await message.reply(
            "✅ کانال با موفقیت ثبت شد."
        )

        await show_channels(message)

        return


    # شروع ثبت کانال
    if message.content != BTN_ADD_CHANNEL:
        return

    set_state(
    user_id,
    "add_channel",
    {}
)

    await message.reply(
        "📢 لطفاً آیدی کانال خود را ارسال کنید.\nآیدی کانال شما باید با @ شروع شود.",
        components=back_menu()
    )