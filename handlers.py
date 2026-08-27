# ==============================
# AdMarketBot - handlers.py
# ==============================

from services import (
    create_user,
    get_user,
    get_coins,
    add_coins,
    spin_daily_wheel,
    get_referral_count,
    process_referral,

    add_channel,
    get_channel,
    get_user_channels,
    get_channel_for_owner,
    delete_channel,

    set_channel_ad_price,
    update_channel_status,
    get_approved_channels,

    create_advertisement,
    get_advertisement,
    approve_advertisement,
    reject_advertisement
)

from keyboards import (
    main_menu,
    daily_wheel_menu,
    my_channels_empty_keyboard,
    my_channels_keyboard,
    channel_management_keyboard,
    delete_channel_keyboard,
    admin_price_keyboard,
    advertising_channels_keyboard
)


# ==============================
# Admin
# ==============================

try:
    from config import ADMIN_IDS
except ImportError:
    try:
        from config import ADMIN_ID
        ADMIN_IDS = [ADMIN_ID]
    except ImportError:
        ADMIN_IDS = []


# ==============================
# Temporary User States
# ==============================

user_states = {}


# ==============================
# Send Message
# ==============================

def send_message(
    api_request,
    chat_id,
    text,
    reply_markup=None
):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        data["reply_markup"] = reply_markup

    return api_request(
        "sendMessage",
        data
    )


# ==============================
# Start
# ==============================

def handle_start(
    api_request,
    message
):

    user = message.get(
        "from",
        {}
    )

    chat = message.get(
        "chat",
        {}
    )

    user_id = user.get("id")
    chat_id = chat.get("id")

    if not user_id or not chat_id:
        return

    text = message.get(
        "text",
        ""
    )

    referral_id = None

    if text.startswith("/start"):

        parts = text.split(
            maxsplit=1
        )

        if len(parts) == 2:

            parameter = parts[1].strip()

            if parameter.startswith("ref_"):

                try:
                    referral_id = int(
                        parameter.replace(
                            "ref_",
                            "",
                            1
                        )
                    )
                except ValueError:
                    referral_id = None

    existing_user = get_user(
        user_id
    )

    create_user(
        user_id=user_id,
        username=user.get("username"),
        first_name=user.get("first_name"),
        referral_id=referral_id
    )

    if not existing_user and referral_id:

        inviter_id = process_referral(
            new_user_id=user_id,
            inviter_id=referral_id
        )

        if inviter_id:

            referral_count = get_referral_count(
                inviter_id
            )

            send_message(
                api_request,
                inviter_id,
                "🎉 دعوت موفق!\n\n"
                "👤 یک کاربر با لینک دعوت شما "
                "وارد ربات شد.\n\n"
                "🪙 شما ۱۰ سکه دریافت کردید!\n\n"
                f"👥 تعداد دعوت‌های موفق شما: "
                f"{referral_count}"
            )

    coins = get_coins(
        user_id
    )

    welcome_text = (
        "👋 سلام!\n\n"
        "🎯 به بازار تبلیغات خوش اومدی!\n\n"
        f"🪙 موجودی سکه: {coins:,}\n\n"
        "از منوی پایین یکی از گزینه‌ها "
        "رو انتخاب کن."
    )

    send_message(
        api_request,
        chat_id,
        welcome_text,
        reply_markup=main_menu()
    )


# ==============================
# Message Handler
# ==============================

def handle_message(
    api_request,
    message
):

    text = message.get(
        "text",
        ""
    ).strip()

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    user = message.get(
        "from",
        {}
    )

    user_id = user.get(
        "id"
    )

    if not chat_id or not user_id:
        return

    # ==========================
    # Start
    # ==========================

    if text.startswith("/start"):

        handle_start(
            api_request,
            message
        )

        return

    # ==========================
    # Current State
    # ==========================

    state = user_states.get(
        user_id
    )

    # ==========================================================
    # ADD CHANNEL
    # ==========================================================

    if state and state.get("step") == "add_channel":

        channel_username = text.strip()

        if not channel_username.startswith("@"):

            channel_username = (
                "@" +
                channel_username
            )

        if len(channel_username) < 2:

            send_message(
                api_request,
                chat_id,
                "❌ یوزرنیم کانال صحیح نیست.\n\n"
                "مثال:\n"
                "@ExampleChannel"
            )

            return

        existing_channel = get_channel(
            channel_username
        )

        if existing_channel:

            user_states.pop(
                user_id,
                None
            )

            if existing_channel["owner_id"] == user_id:

                send_message(
                    api_request,
                    chat_id,
                    "⚠️ این کانال قبلاً به حساب شما اضافه شده است."
                )

            else:

                send_message(
                    api_request,
                    chat_id,
                    "❌ این کانال قبلاً توسط کاربر دیگری ثبت شده است."
                )

            return

        channel_info = api_request(
            "getChat",
            {
                "chat_id": channel_username
            }
        )

        if not channel_info:

            send_message(
                api_request,
                chat_id,
                "❌ کانال پیدا نشد.\n\n"
                "لطفاً مطمئن شوید یوزرنیم کانال درست است."
            )

            return

        channel_type = channel_info.get(
            "type"
        )

        if channel_type != "channel":

            send_message(
                api_request,
                chat_id,
                "❌ این آیدی مربوط به کانال نیست."
            )

            return

        channel_id = channel_info.get(
            "id"
        )

        channel_name = channel_info.get(
            "title",
            "بدون نام"
        )

        saved = add_channel(
            owner_id=user_id,
            channel_id=channel_id,
            channel_username=channel_username,
            channel_name=channel_name
        )

        user_states.pop(
            user_id,
            None
        )

        if not saved:

            send_message(
                api_request,
                chat_id,
                "❌ ثبت کانال انجام نشد."
            )

            return

        send_message(
            api_request,
            chat_id,
            "✅ کانال با موفقیت اضافه شد!\n\n"
            f"📺 نام کانال: {channel_name}\n"
            f"🔗 یوزرنیم: {channel_username}\n\n"
            "حالا می‌تونی برای کانالت قیمت تبلیغ تعیین کنی."
        )

        return

    # ==========================================================
    # PRICE INPUT
    # ==========================================================

    if state and state.get("step") == "price":

        try:

            price = int(
                text.replace(
                    ",",
                    ""
                )
            )

        except ValueError:

            send_message(
                api_request,
                chat_id,
                "❌ مبلغ وارد شده صحیح نیست.\n\n"
                "مثال:\n"
                "15000"
            )

            return

        if price <= 0:

            send_message(
                api_request,
                chat_id,
                "❌ مبلغ باید بیشتر از صفر باشد."
            )

            return

        user_states[user_id] = {
            "step": "daily_views",
            "channel_id": state["channel_id"],
            "price": price
        }

        send_message(
            api_request,
            chat_id,
            "👁 ویوی تقریبی روزانه کانالت رو وارد کن.\n\n"
            "مثلاً:\n"
            "100"
        )

        return

    # ==========================================================
    # DAILY VIEWS INPUT
    # ==========================================================

    if state and state.get("step") == "daily_views":

        try:

            daily_views = int(
                text.replace(
                    ",",
                    ""
                )
            )

        except ValueError:

            send_message(
                api_request,
                chat_id,
                "❌ تعداد ویو صحیح نیست.\n\n"
                "مثال:\n"
                "100"
            )

            return

        if daily_views <= 0:

            send_message(
                api_request,
                chat_id,
                "❌ تعداد ویو باید بیشتر از صفر باشد."
            )

            return

        channel_id = state["channel_id"]
        price = state["price"]

        channel = get_channel_for_owner(
            channel_id,
            user_id
        )

        if not channel:

            user_states.pop(
                user_id,
                None
            )

            send_message(
                api_request,
                chat_id,
                "❌ کانال پیدا نشد یا متعلق به شما نیست."
            )

            return

        saved = set_channel_ad_price(
            channel_id=channel_id,
            price=price,
            daily_views=daily_views
        )

        user_states.pop(
            user_id,
            None
        )

        if not saved:

            send_message(
                api_request,
                chat_id,
                "❌ ذخیره درخواست انجام نشد."
            )

            return

        channel_username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        if (
            channel_username != "بدون یوزرنیم"
            and not channel_username.startswith("@")
        ):

            channel_username = (
                "@" +
                channel_username
            )

        username = user.get(
            "username"
        )

        requester = (
            f"@{username}"
            if username
            else str(user_id)
        )

        admin_text = (
            "📢 درخواست تعیین قیمت تبلیغ\n\n"
            f"📺 کانال:\n"
            f"{channel_username}\n\n"
            f"🆔 Channel ID:\n"
            f"{channel['channel_id']}\n\n"
            f"👤 درخواست‌دهنده:\n"
            f"{requester}\n\n"
            f"💰 قیمت پیشنهادی:\n"
            f"{price:,} سکه\n\n"
            f"👁 ویوی تقریبی روزانه:\n"
            f"{daily_views:,}\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "لطفاً کانال را بررسی کنید."
        )

        for admin_id in ADMIN_IDS:

            send_message(
                api_request,
                admin_id,
                admin_text,
                reply_markup=admin_price_keyboard(
                    channel_id,
                    user_id
                )
            )

        send_message(
            api_request,
            chat_id,
            "✅ درخواست تعیین قیمت ثبت شد!\n\n"
            f"📺 کانال: {channel_username}\n"
            f"💰 قیمت پیشنهادی: {price:,} سکه\n\n"
            "⏳ درخواست برای مدیریت ارسال شد."
        )

        return

    # ==========================================================
    # ADMIN MESSAGE STATE
    # ==========================================================

    if state and state.get("step") == "admin_message":

        owner_id = state.get(
            "owner_id"
        )

        if user_id not in ADMIN_IDS:

            user_states.pop(
                user_id,
                None
            )

            return

        if not text:

            send_message(
                api_request,
                chat_id,
                "❌ پیام نمی‌تونه خالی باشه."
            )

            return

        send_message(
            api_request,
            owner_id,
            "📩 پیام مدیریت بازار تبلیغات:\n\n"
            f"{text}"
        )

        user_states.pop(
            user_id,
            None
        )

        send_message(
            api_request,
            chat_id,
            "✅ پیام با موفقیت برای صاحب کانال ارسال شد."
        )

        return

    # ==========================================================
    # AD CONTENT
    # ==========================================================

    if state and state.get("step") == "ad_content":

        channel_id = state.get(
            "channel_id"
        )

        content = text

        if not content:

            send_message(
                api_request,
                chat_id,
                "❌ متن تبلیغ نمی‌تونه خالی باشه."
            )

            return

        channel = get_channel(
            channel_id
        )

        if not channel:

            user_states.pop(
                user_id,
                None
            )

            send_message(
                api_request,
                chat_id,
                "❌ کانال پیدا نشد."
            )

            return

        if channel["status"] != "approved":

            user_states.pop(
                user_id,
                None
            )

            send_message(
                api_request,
                chat_id,
                "❌ این کانال دیگر برای تبلیغ فعال نیست."
            )

            return

        price = channel["ad_price"]

        user_states[user_id] = {
            "step": "ad_payment",
            "channel_id": channel_id,
            "content": content,
            "price": price
        }

        coins = get_coins(
            user_id
        )

        username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        send_message(
            api_request,
            chat_id,
            "📢 پیش‌نمایش تبلیغ\n\n"
            f"📺 کانال مقصد: {username}\n\n"
            f"💰 قیمت تبلیغ: {price:,} سکه\n"
            f"🪙 موجودی شما: {coins:,} سکه\n\n"
            "━━━━━━━━━━━━━━\n\n"
            f"{content}\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "اگر متن تبلیغ صحیح است، "
            "دکمه پرداخت را بزن."
        )

        send_message(
            api_request,
            chat_id,
            "💳 پرداخت تبلیغ",
            reply_markup={
                "inline_keyboard": [
                    [
                        {
                            "text": f"💰 پرداخت {price:,} سکه",
                            "callback_data": "ad_pay"
                        }
                    ],
                    [
                        {
                            "text": "❌ لغو",
                            "callback_data": "ad_cancel"
                        }
                    ]
                ]
            }
        )

        return

    # ==========================================================
    # ADS
    # ==========================================================

    if text == "📢 تبلیغات":

        channels = get_approved_channels()

        if not channels:

            send_message(
                api_request,
                chat_id,
                "📢 تبلیغات\n\n"
                "❌ در حال حاضر هیچ کانال تاییدشده‌ای "
                "برای تبلیغ وجود ندارد."
            )

            return

        send_message(
            api_request,
            chat_id,
            "📢 خرید تبلیغات\n\n"
            "کانال موردنظر را انتخاب کنید:",
            reply_markup=advertising_channels_keyboard(
                channels
            )
        )

        return

    # ==========================================================
    # MY CHANNELS
    # ==========================================================

    if text == "📺 کانال‌های من":

        channels = get_user_channels(
            user_id
        )

        if not channels:

            send_message(
                api_request,
                chat_id,
                "📺 کانال‌های من\n\n"
                "شما هنوز هیچ کانالی ثبت نکردید.",
                reply_markup=my_channels_empty_keyboard()
            )

            return

        send_message(
            api_request,
            chat_id,
            "📺 کانال‌های من\n\n"
            "کانال موردنظر را انتخاب کنید:",
            reply_markup=my_channels_keyboard(
                channels
            )
        )

        return

    # ==========================================================
    # WALLET
    # ==========================================================

    if text == "🪙 کیف پول":

        coins = get_coins(
            user_id
        )

        send_message(
            api_request,
            chat_id,
            "🪙 کیف پول\n\n"
            f"💰 موجودی شما: {coins:,} سکه\n\n"
            "💡 با انجام مأموریت‌ها "
            "می‌تونی سکه بیشتری کسب کنی."
        )

        return

    # ==========================================================
    # EARN COINS
    # ==========================================================

    if text == "🎁 کسب سکه":

        send_message(
            api_request,
            chat_id,
            "🎁 کسب سکه\n\n"
            "از این بخش می‌تونی "
            "سکه رایگان کسب کنی."
        )

        return

    # ==========================================================
    # DAILY WHEEL
    # ==========================================================

    if text == "🎡 گردونه روزانه":

        send_message(
            api_request,
            chat_id,
            "🎡 گردونه روزانه\n\n"
            "هر کاربر روزی فقط یک بار "
            "می‌تونه گردونه رو بچرخونه.\n\n"
            "🎁 جایزه: 1 تا 100 سکه",
            reply_markup=daily_wheel_menu()
        )

        return

    # ==========================================================
    # REFERRAL
    # ==========================================================

    if text == "🔗 دعوت دوستان":

        referral_count = get_referral_count(
            user_id
        )

        bot_username = "whocheckssmebot"

        referral_link = (
            f"https://ble.ir/{bot_username}"
            f"?start=ref_{user_id}"
        )

        send_message(
            api_request,
            chat_id,
            "🔗 دعوت دوستان\n\n"
            "👥 دوستان خود را دعوت کنید "
            "و سکه رایگان بگیرید!\n\n"
            "🔗 لینک دعوت اختصاصی شما:\n\n"
            f"{referral_link}\n\n"
            "🪙 هر دعوت موفق = 10 سکه\n\n"
            f"👥 تعداد دعوت‌های موفق شما: "
            f"{referral_count}"
        )

        return

    # ==========================================================
    # PROFILE
    # ==========================================================

    if text == "👤 حساب من":

        coins = get_coins(
            user_id
        )

        referral_count = get_referral_count(
            user_id
        )

        channels = get_user_channels(
            user_id
        )

        send_message(
            api_request,
            chat_id,
            "👤 حساب کاربری\n\n"
            f"🆔 شناسه: {user_id}\n"
            f"🪙 موجودی: {coins:,} سکه\n"
            f"👥 دعوت موفق: {referral_count}\n"
            f"📺 تعداد کانال‌ها: {len(channels)}"
        )

        return


# ==============================================================
# Callback Handler
# ==============================================================

def handle_callback(
    api_request,
    callback_query
):

    callback_id = callback_query.get(
        "id"
    )

    data = callback_query.get(
        "data",
        ""
    )

    message = callback_query.get(
        "message",
        {}
    )

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    message_id = message.get(
        "message_id"
    )

    user = callback_query.get(
        "from",
        {}
    )

    user_id = user.get(
        "id"
    )

    if not callback_id or not user_id:
        return

    # ==========================================================
    # DAILY WHEEL
    # ==========================================================

    if data == "wheel_spin":

        result = spin_daily_wheel(
            user_id
        )

        if result["success"]:

            reward = result["reward"]
            balance = result["balance"]

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id
                }
            )

            api_request(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": (
                        "🎉 تبریک!\n\n"
                        f"🎡 شما {reward} سکه دریافت کردید.\n\n"
                        f"🪙 موجودی جدید: "
                        f"{balance:,} سکه\n\n"
                        "⏰ فردا دوباره می‌تونی "
                        "گردونه رو بچرخونی."
                    )
                }
            )

            return

        if result["reason"] == "already_spun":

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ امروز گردونه رو چرخوندی!",
                    "show_alert": True
                }
            )

            return

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "❌ خطایی رخ داد.",
                "show_alert": True
            }
        )

        return

    # ==========================================================
    # WHEEL BACK
    # ==========================================================

    if data == "wheel_back":

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "🏠 منوی اصلی\n\n"
                    "از منوی پایین یکی از گزینه‌ها "
                    "رو انتخاب کن."
                )
            }
        )

        return

    # ==========================================================
    # ADD CHANNEL
    # ==========================================================

    if data == "add_channel":

        user_states[user_id] = {
            "step": "add_channel"
        }

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        send_message(
            api_request,
            chat_id,
            "➕ افزودن کانال\n\n"
            "یوزرنیم کانالت رو ارسال کن.\n\n"
            "مثال:\n"
            "@ExampleChannel\n\n"
            "⚠️ مطمئن شو ربات دسترسی لازم "
            "برای بررسی کانال را دارد."
        )

        return

    # ==========================================================
    # CHANNEL SELECT
    # ==========================================================

    if data.startswith("channel:"):

        channel_id = data.split(
            ":",
            1
        )[1]

        channel = get_channel_for_owner(
            channel_id,
            user_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ این کانال متعلق به شما نیست.",
                    "show_alert": True
                }
            )

            return

        username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        status = channel["status"]

        if status == "approved":
            status_text = "✅ تایید شده"
        elif status == "price_pending":
            status_text = "⏳ در انتظار بررسی قیمت"
        elif status == "rejected":
            status_text = "❌ قیمت رد شده"
        else:
            status_text = "⏳ در انتظار بررسی"

        channel_text = (
            "📺 مدیریت کانال\n\n"
            f"📢 کانال: {username}\n"
            f"🆔 شناسه: {channel['channel_id']}\n\n"
            f"📊 وضعیت: {status_text}\n"
        )

        if channel["ad_price"] > 0:

            channel_text += (
                f"💰 قیمت تبلیغ: "
                f"{channel['ad_price']:,} سکه\n"
            )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": channel_text,
                "reply_markup": channel_management_keyboard(
                    channel_id
                )
            }
        )

        return

    # ==========================================================
    # ADVERTISING CHANNEL SELECT
    # ==========================================================

    if data.startswith("advertise_channel:"):

        channel_id = data.split(
            ":",
            1
        )[1]

        channel = get_channel(
            channel_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ کانال پیدا نشد.",
                    "show_alert": True
                }
            )

            return

        if (
            channel["status"] != "approved"
            or channel["ad_price"] <= 0
        ):

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ این کانال برای تبلیغ فعال نیست.",
                    "show_alert": True
                }
            )

            return

        username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        price = channel["ad_price"]

        user_states[user_id] = {
            "step": "ad_content",
            "channel_id": channel_id,
            "price": price
        }

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "📢 خرید تبلیغات\n\n"
                    f"📺 کانال مقصد: {username}\n\n"
                    f"💰 قیمت هر تبلیغ: "
                    f"{price:,} سکه\n\n"
                    "━━━━━━━━━━━━━━\n\n"
                    "📝 متن تبلیغ خودت رو ارسال کن.\n\n"
                    "بعد از ارسال، مبلغ و متن تبلیغ "
                    "بهت نمایش داده میشه."
                ),
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "❌ لغو",
                                "callback_data": "ad_cancel"
                            }
                        ]
                    ]
                }
            }
        )

        return

    # ==========================================================
    # AD PAYMENT
    # ==========================================================

    if data == "ad_pay":

        state = user_states.get(
            user_id
        )

        if not state or state.get("step") != "ad_payment":

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ این درخواست منقضی شده است.",
                    "show_alert": True
                }
            )

            return

        channel_id = state["channel_id"]
        content = state["content"]
        price = state["price"]

        channel = get_channel(
            channel_id
        )

        if not channel:

            user_states.pop(
                user_id,
                None
            )

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ کانال پیدا نشد.",
                    "show_alert": True
                }
            )

            return

        if (
            channel["status"] != "approved"
            or channel["ad_price"] <= 0
        ):

            user_states.pop(
                user_id,
                None
            )

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ این کانال دیگر برای تبلیغ فعال نیست.",
                    "show_alert": True
                }
            )

            return

        result = create_advertisement(
            advertiser_id=user_id,
            channel_id=channel_id,
            content=content
        )

        if not result["success"]:

            if result["reason"] == "insufficient_coins":

                api_request(
                    "answerCallbackQuery",
                    {
                        "callback_query_id": callback_id,
                        "text": "❌ سکه کافی ندارید.",
                        "show_alert": True
                    }
                )

                return

            user_states.pop(
                user_id,
                None
            )

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ پرداخت انجام نشد.",
                    "show_alert": True
                }
            )

            return

        advertisement_id = result[
            "advertisement_id"
        ]

        owner_id = result[
            "owner_id"
        ]

        new_balance = result[
            "balance"
        ]

        username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        user_states.pop(
            user_id,
            None
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "✅ پرداخت با موفقیت انجام شد."
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "✅ پرداخت با موفقیت انجام شد!\n\n"
                    f"📢 کانال مقصد: {username}\n"
                    f"💰 مبلغ پرداختی: {price:,} سکه\n"
                    f"🪙 موجودی جدید: {new_balance:,} سکه\n\n"
                    "⏳ درخواست تبلیغ برای صاحب کانال ارسال شد.\n"
                    "تا زمان تایید صاحب کانال، "
                    "تبلیغ منتشر نمی‌شود."
                )
            }
        )

        owner_text = (
            "📢 درخواست تبلیغ جدید\n\n"
            f"📺 کانال شما:\n"
            f"{username}\n\n"
            f"🆔 شناسه درخواست:\n"
            f"{advertisement_id}\n\n"
            f"👤 تبلیغ‌دهنده:\n"
            f"{user_id}\n\n"
            f"💰 مبلغ تبلیغ:\n"
            f"{price:,} سکه\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "📝 متن تبلیغ:\n\n"
            f"{content}\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "آیا تبلیغ را تایید می‌کنید؟"
        )

        send_message(
            api_request,
            owner_id,
            owner_text,
            reply_markup={
                "inline_keyboard": [
                    [
                        {
                            "text": "✅ تایید تبلیغ",
                            "callback_data": (
                                f"approve_ad:{advertisement_id}"
                            )
                        },
                        {
                            "text": "❌ رد تبلیغ",
                            "callback_data": (
                                f"reject_ad:{advertisement_id}"
                            )
                        }
                    ]
                ]
            }
        )

        return

    # ==========================================================
    # AD CANCEL
    # ==========================================================

    if data == "ad_cancel":

        user_states.pop(
            user_id,
            None
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "❌ خرید تبلیغ لغو شد."
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "❌ خرید تبلیغ لغو شد.\n\n"
                    "می‌تونی دوباره از بخش تبلیغات "
                    "یک کانال انتخاب کنی."
                )
            }
        )

        return

    # ==========================================================
    # OWNER APPROVE AD
    # ==========================================================

    if data.startswith("approve_ad:"):

        advertisement_id_text = data.split(
            ":",
            1
        )[1]

        try:

            advertisement_id = int(
                advertisement_id_text
            )

        except ValueError:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ درخواست نامعتبر است.",
                    "show_alert": True
                }
            )

            return

        advertisement = get_advertisement(
            advertisement_id
        )

        if not advertisement:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ درخواست پیدا نشد یا قبلاً بررسی شده.",
                    "show_alert": True
                }
            )

            return

        if advertisement["owner_id"] != user_id:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ این تبلیغ مربوط به کانال شما نیست.",
                    "show_alert": True
                }
            )

            return

        result = approve_advertisement(
            advertisement_id,
            user_id
        )

        if not result["success"]:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ تایید تبلیغ انجام نشد.",
                    "show_alert": True
                }
            )

            return

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "✅ تبلیغ تایید شد."
            }
        )

        channel_id = advertisement[
            "bale_channel_id"
        ]

        content = advertisement[
            "content"
        ]

        publish_result = send_message(
            api_request,
            channel_id,
            content
        )

        if not publish_result:

            send_message(
                api_request,
                user_id,
                "⚠️ تبلیغ تایید شد اما انتشار در کانال با خطا مواجه شد."
            )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "✅ تبلیغ تایید شد.\n\n"
                    "📢 تبلیغ برای انتشار ارسال شد.\n\n"
                    f"💰 مبلغ: "
                    f"{advertisement['price']:,} سکه"
                )
            }
        )

        send_message(
            api_request,
            advertisement["advertiser_id"],
            "🎉 تبلیغ شما تایید شد!\n\n"
            f"📺 کانال: "
            f"{advertisement['channel_username']}\n\n"
            f"💰 مبلغ: "
            f"{advertisement['price']:,} سکه\n\n"
            "✅ تبلیغ شما توسط صاحب کانال تایید شد."
        )

        return

    # ==========================================================
    # OWNER REJECT AD
    # ==========================================================

    if data.startswith("reject_ad:"):

        advertisement_id_text = data.split(
            ":",
            1
        )[1]

        try:

            advertisement_id = int(
                advertisement_id_text
            )

        except ValueError:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ درخواست نامعتبر است.",
                    "show_alert": True
                }
            )

            return

        advertisement = get_advertisement(
            advertisement_id
        )

        if not advertisement:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ درخواست پیدا نشد.",
                    "show_alert": True
                }
            )

            return

        if advertisement["owner_id"] != user_id:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ این تبلیغ مربوط به کانال شما نیست.",
                    "show_alert": True
                }
            )

            return

        result = reject_advertisement(
            advertisement_id,
            user_id
        )

        if not result["success"]:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ رد تبلیغ انجام نشد.",
                    "show_alert": True
                }
            )

            return

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "❌ تبلیغ رد شد و پول برگشت."
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "❌ تبلیغ رد شد.\n\n"
                    f"💰 مبلغ {advertisement['price']:,} "
                    "سکه به کیف پول تبلیغ‌دهنده برگشت داده شد."
                )
            }
        )

        send_message(
            api_request,
            advertisement["advertiser_id"],
            "❌ تبلیغ شما توسط صاحب کانال رد شد.\n\n"
            f"📺 کانال: "
            f"{advertisement['channel_username']}\n\n"
            f"💰 مبلغ برگشتی: "
            f"{advertisement['price']:,} سکه\n\n"
            "🪙 مبلغ کامل به کیف پول شما برگشت داده شد."
        )

        return

    # ==========================================================
    # BACK TO CHANNELS
    # ==========================================================

    if data in (
        "back_channels",
        "channels_back"
    ):

        channels = get_user_channels(
            user_id
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        if not channels:

            api_request(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": (
                        "📺 کانال‌های من\n\n"
                        "شما هنوز هیچ کانالی ثبت نکردید."
                    ),
                    "reply_markup": my_channels_empty_keyboard()
                }
            )

        else:

            api_request(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": (
                        "📺 کانال‌های من\n\n"
                        "کانال موردنظر را انتخاب کنید:"
                    ),
                    "reply_markup": my_channels_keyboard(
                        channels
                    )
                }
            )

        return

    # ==========================================================
    # DELETE CHANNEL
    # ==========================================================

    if data.startswith("delete_channel:"):

        channel_id = data.split(
            ":",
            1
        )[1]

        channel = get_channel_for_owner(
            channel_id,
            user_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ این کانال متعلق به شما نیست.",
                    "show_alert": True
                }
            )

            return

        username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "🗑 حذف کانال\n\n"
                    f"📺 {username}\n\n"
                    "آیا مطمئن هستید؟"
                ),
                "reply_markup": delete_channel_keyboard(
                    channel_id
                )
            }
        )

        return

    # ==========================================================
    # CONFIRM DELETE
    # ==========================================================

    if data.startswith("confirm_delete:"):

        channel_id = data.split(
            ":",
            1
        )[1]

        channel = get_channel_for_owner(
            channel_id,
            user_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ کانال پیدا نشد.",
                    "show_alert": True
                }
            )

            return

        deleted = delete_channel(
            channel_id,
            user_id
        )

        if not deleted:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ حذف کانال انجام نشد.",
                    "show_alert": True
                }
            )

            return

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "✅ کانال حذف شد."
            }
        )

        channels = get_user_channels(
            user_id
        )

        if not channels:

            api_request(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": "🗑 کانال با موفقیت حذف شد.",
                    "reply_markup": my_channels_empty_keyboard()
                }
            )

        else:

            api_request(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": (
                        "✅ کانال با موفقیت حذف شد.\n\n"
                        "📺 کانال‌های شما:"
                    ),
                    "reply_markup": my_channels_keyboard(
                        channels
                    )
                }
            )

        return

    # ==========================================================
    # CANCEL DELETE
    # ==========================================================

    if data.startswith("cancel_delete:"):

        channel_id = data.split(
            ":",
            1
        )[1]

        channel = get_channel_for_owner(
            channel_id,
            user_id
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        if not channel:
            return

        username = (
            channel["channel_username"]
            or "بدون یوزرنیم"
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "📺 مدیریت کانال\n\n"
                    f"📢 کانال: {username}\n\n"
                    "حذف کانال لغو شد."
                ),
                "reply_markup": channel_management_keyboard(
                    channel_id
                )
            }
        )

        return

    # ==========================================================
    # SET CHANNEL PRICE
    # ==========================================================

    if data.startswith("set_price:"):

        channel_id = data.split(
            ":",
            1
        )[1]

        channel = get_channel_for_owner(
            channel_id,
            user_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ این کانال متعلق به شما نیست.",
                    "show_alert": True
                }
            )

            return

        user_states[user_id] = {
            "step": "price",
            "channel_id": channel_id
        }

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        send_message(
            api_request,
            chat_id,
            "💰 قیمت هر تبلیغ را وارد کنید.\n\n"
            "مثلاً:\n"
            "15000\n\n"
            "فقط عدد وارد کنید."
        )

        return

    # ==========================================================
    # ADMIN APPROVE PRICE
    # ==========================================================

    if data.startswith("approve_price:"):

        parts = data.split(":")

        if len(parts) != 3:
            return

        channel_id = parts[1]

        try:
            owner_id = int(parts[2])
        except ValueError:
            return

        if user_id not in ADMIN_IDS:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ شما دسترسی ندارید.",
                    "show_alert": True
                }
            )

            return

        channel = get_channel(
            channel_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ کانال پیدا نشد.",
                    "show_alert": True
                }
            )

            return

        update_channel_status(
            channel_id,
            "approved"
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "✅ مبلغ تایید شد."
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "✅ مبلغ تبلیغ تایید شد.\n\n"
                    f"📺 {channel['channel_username']}\n\n"
                    f"💰 قیمت: "
                    f"{channel['ad_price']:,} سکه"
                )
            }
        )

        send_message(
            api_request,
            owner_id,
            "🎉 قیمت تبلیغ کانال شما تایید شد!\n\n"
            f"📺 {channel['channel_username']}\n\n"
            f"💰 قیمت هر تبلیغ: "
            f"{channel['ad_price']:,} سکه\n\n"
            "✅ کانال شما اکنون آماده دریافت تبلیغ است."
        )

        return

    # ==========================================================
    # ADMIN REJECT PRICE
    # ==========================================================

    if data.startswith("reject_price:"):

        parts = data.split(":")

        if len(parts) != 3:
            return

        channel_id = parts[1]

        try:
            owner_id = int(parts[2])
        except ValueError:
            return

        if user_id not in ADMIN_IDS:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ شما دسترسی ندارید.",
                    "show_alert": True
                }
            )

            return

        channel = get_channel(
            channel_id
        )

        if not channel:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "❌ کانال پیدا نشد.",
                    "show_alert": True
                }
            )

            return

        update_channel_status(
            channel_id,
            "rejected"
        )

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id,
                "text": "❌ قیمت رد شد."
            }
        )

        api_request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": (
                    "❌ قیمت تبلیغ رد شد.\n\n"
                    f"📺 {channel['channel_username']}\n\n"
                    f"💰 قیمت پیشنهادی: "
                    f"{channel['ad_price']:,} سکه"
                )
            }
        )

        send_message(
            api_request,
            owner_id,
            "❌ قیمت تبلیغ کانال شما تایید نشد.\n\n"
            f"📺 {channel['channel_username']}\n\n"
            f"💰 قیمت پیشنهادی: "
            f"{channel['ad_price']:,} سکه\n\n"
            "می‌تونی دوباره قیمت جدیدی ثبت کنی."
        )

        return

    # ==========================================================
    # ADMIN MESSAGE OWNER
    # ==========================================================

    if data.startswith("message_owner:"):

        parts = data.split(":")

        if len(parts) != 3:
            return

        channel_id = parts[1]

        try:
            owner_id = int(parts[2])
        except ValueError:
            return

        if user_id not in ADMIN_IDS:

            api_request(
                "answerCallbackQuery",
                {
                    "callback_query_id": callback_id,
                    "text": "⛔ شما دسترسی ندارید.",
                    "show_alert": True
                }
            )

            return

        user_states[user_id] = {
            "step": "admin_message",
            "owner_id": owner_id,
            "channel_id": channel_id
        }

        api_request(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_id
            }
        )

        send_message(
            api_request,
            chat_id,
            "💬 پیام خود را برای صاحب کانال ارسال کنید.\n\n"
            "متنی که بفرستید مستقیماً برای او ارسال می‌شود."
        )

        return

    # ==========================================================
    # UNKNOWN CALLBACK
    # ==========================================================

    api_request(
        "answerCallbackQuery",
        {
            "callback_query_id": callback_id
        }
    )
