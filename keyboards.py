# ==============================
# AdMarketBot - keyboards.py
# ==============================


# ==============================
# 🏠 Main Menu
# ==============================

def main_menu():

    return {
        "keyboard": [
            [
                {"text": "📢 تبلیغات"},
                {"text": "📺 کانال‌های من"}
            ],
            [
                {"text": "🪙 کیف پول"},
                {"text": "🎁 کسب سکه"}
            ],
            [
                {"text": "🎡 گردونه روزانه"},
                {"text": "🔗 دعوت دوستان"}
            ],
            [
                {"text": "👤 حساب من"}
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


# ==============================
# ❌ Remove Keyboard
# ==============================

def remove_keyboard():

    return {
        "remove_keyboard": True
    }


# ==============================
# 🎡 Daily Wheel
# ==============================

def daily_wheel_menu():

    return {
        "inline_keyboard": [
            [
                {
                    "text": "🎡 چرخاندن!",
                    "callback_data": "wheel_spin"
                }
            ],
            [
                {
                    "text": "🔙 برگشت",
                    "callback_data": "wheel_back"
                }
            ]
        ]
    }


# ==============================
# 📺 My Channels - Empty
# ==============================

def my_channels_empty_keyboard():

    return {
        "inline_keyboard": [
            [
                {
                    "text": "➕ افزودن کانال",
                    "callback_data": "add_channel"
                }
            ],
            [
                {
                    "text": "🔙 برگشت",
                    "callback_data": "channels_back"
                }
            ]
        ]
    }


# ==============================
# 📺 My Channels List
# ==============================

def my_channels_keyboard(channels):

    keyboard = []

    for channel in channels:

        # sqlite3.Row → استفاده از [] به جای .get()
        username = (
            channel["channel_username"]
            or channel["channel_name"]
            or "کانال بدون نام"
        )

        if (
            username.startswith("@")
            or username == "کانال بدون نام"
        ):
            button_text = f"📺 {username}"
        else:
            button_text = f"📺 @{username}"

        keyboard.append([
            {
                "text": button_text,
                "callback_data": (
                    f"channel:{channel['channel_id']}"
                )
            }
        ])

    keyboard.append([
        {
            "text": "➕ افزودن کانال",
            "callback_data": "add_channel"
        }
    ])

    keyboard.append([
        {
            "text": "🔙 برگشت",
            "callback_data": "channels_back"
        }
    ])

    return {
        "inline_keyboard": keyboard
    }


# ==============================
# ⚙️ Channel Management
# ==============================

def channel_management_keyboard(channel_id):

    return {
        "inline_keyboard": [
            [
                {
                    "text": "💰 تعیین قیمت تبلیغ",
                    "callback_data": (
                        f"set_price:{channel_id}"
                    )
                }
            ],
            [
                {
                    "text": "🗑 حذف کانال",
                    "callback_data": (
                        f"delete_channel:{channel_id}"
                    )
                }
            ],
            [
                {
                    "text": "🔙 برگشت به کانال‌ها",
                    "callback_data": "back_channels"
                }
            ]
        ]
    }


# ==============================
# 🗑 Delete Channel Confirmation
# ==============================

def delete_channel_keyboard(channel_id):

    return {
        "inline_keyboard": [
            [
                {
                    "text": "✅ بله، حذف شود",
                    "callback_data": (
                        f"confirm_delete:{channel_id}"
                    )
                },
                {
                    "text": "❌ لغو",
                    "callback_data": (
                        f"cancel_delete:{channel_id}"
                    )
                }
            ]
        ]
    }


# ==============================
# 💰 Channel Price
# ==============================

def channel_price_keyboard(channel_id):

    return {
        "inline_keyboard": [
            [
                {
                    "text": "💰 تعیین قیمت تبلیغ",
                    "callback_data": (
                        f"set_price:{channel_id}"
                    )
                }
            ],
            [
                {
                    "text": "🗑 حذف کانال",
                    "callback_data": (
                        f"delete_channel:{channel_id}"
                    )
                }
            ],
            [
                {
                    "text": "🔙 برگشت",
                    "callback_data": "back_channels"
                }
            ]
        ]
    }


# ==============================
# 👨‍💼 Admin Price Request
# ==============================

def admin_price_keyboard(
    channel_id,
    owner_id
):

    return {
        "inline_keyboard": [
            [
                {
                    "text": "❌ رد قیمت",
                    "callback_data": (
                        f"reject_price:"
                        f"{channel_id}:"
                        f"{owner_id}"
                    )
                }
            ],
            [
                {
                    "text": "💬 پیام به کاربر",
                    "callback_data": (
                        f"message_owner:"
                        f"{channel_id}:"
                        f"{owner_id}"
                    )
                }
            ],
            [
                {
                    "text": "✅ تایید مبلغ",
                    "callback_data": (
                        f"approve_price:"
                        f"{channel_id}:"
                        f"{owner_id}"
                    )
                }
            ]
        ]
    }


# ==============================
# 📢 Advertising Channels
# ==============================

def advertising_channels_keyboard(channels):

    keyboard = []

    for channel in channels:

        # sqlite3.Row → استفاده از [] به جای .get()
        username = (
            channel["channel_username"]
            or channel["channel_name"]
            or "کانال بدون نام"
        )

        if (
            username.startswith("@")
            or username == "کانال بدون نام"
        ):
            button_text = f"📺 {username}"
        else:
            button_text = f"📺 @{username}"

        keyboard.append([
            {
                "text": button_text,
                "callback_data": (
                    f"advertise_channel:"
                    f"{channel['channel_id']}"
                )
            }
        ])

    keyboard.append([
        {
            "text": "🔙 برگشت",
            "callback_data": "ads_back"
        }
    ])

    return {
        "inline_keyboard": keyboard
                }
