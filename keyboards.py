# ==========================
# AutoNewsBot Keyboards
# Version 2.7.1
# ==========================

from bale import (
    MenuKeyboardMarkup,
    MenuKeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


BTN_PROFILE = "👤 پروفایل"
BTN_WALLET = "💰 کیف پول"

BTN_CHANNEL = "📢 کانال‌های من"
BTN_ADD_CHANNEL = "➕ افزودن کانال جدید"
BTN_REFERRAL = "🎁 دعوت دوستان"

BTN_SUBSCRIPTION = "💳 خرید اشتراک"
BTN_SUPPORT = "📞 پشتیبانی"

BTN_ADMIN = "🛠 پنل مدیریت"

BTN_BACK = "🔙 بازگشت"
BTN_HOME = "🏠 منوی اصلی"
BTN_CANCEL = "❌ انصراف"

BTN_ADMIN_STATS_USERS = "📊 آمار کاربران"
BTN_ADMIN_STATS_CHANNELS = "📢 آمار کانال‌ها"
BTN_ADMIN_STATS_NEWS = "📰 آمار اخبار"

BTN_ADMIN_USERS = "👤 مدیریت کاربران"
BTN_ADMIN_CHANNELS = "📺 مدیریت کانال‌ها"
BTN_ADMIN_ADMINS = "👮 ادمین‌ها"

BTN_ADMIN_BROADCAST = "📨 ارسال همگانی"

BTN_ADMIN_SETTINGS = "⚙️ تنظیمات ربات"

BTN_ADMIN_JOIN = "🔒 جوین اجباری"



# ==========================
# منوی اصلی
# ==========================

def main_menu(is_admin=False):

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton(BTN_PROFILE),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton(BTN_CHANNEL),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton(BTN_SUPPORT),
        row=3
    )

    if is_admin:
        keyboard.add(
            MenuKeyboardButton(BTN_ADMIN),
            row=4
        )

    return keyboard



# ==========================
# منوی کانال‌ها
# ==========================

def channel_menu():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton(BTN_ADD_CHANNEL),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton(BTN_BACK),
        row=2
    )

    keyboard.add(
        MenuKeyboardButton(BTN_HOME),
        row=2
    )

    return keyboard



# ==========================
# منوی پایین تنظیمات کانال
# ==========================

def channel_settings_bottom_menu():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton(BTN_BACK),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton(BTN_HOME),
        row=1
    )

    return keyboard



# ==========================
# لیست کانال‌ها
# ==========================

def channel_inline_menu(channels):

    keyboard = InlineKeyboardMarkup()

    for channel in channels:

        keyboard.add(
            InlineKeyboardButton(
                f"⚙️ {channel['id']}",
                callback_data=f"channel_{channel['id']}"
            )
        )

    return keyboard



# ==========================
# تنظیمات کانال
# ==========================

def channel_settings_menu(channel_id, send_image=True, show_emoji=True):

    if send_image:

        image_text = "🖼 عکس: 🟢 روشن"

    else:

        image_text = "🖼 عکس: 🔴 خاموش"


    if show_emoji:

        emoji_text = "😀 ایموجی: 🟢 روشن"

    else:

        emoji_text = "😀 ایموجی: 🔴 خاموش"


    keyboard = InlineKeyboardMarkup()


    keyboard.add(
        InlineKeyboardButton(
            image_text,
            callback_data=f"img_{channel_id}"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            emoji_text,
            callback_data=f"emoji_{channel_id}"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "⏱ زمان ارسال",
            callback_data=f"time_{channel_id}"
        ),
        row=2
    )


    keyboard.add(
        InlineKeyboardButton(
            "🏷 دسته‌بندی",
            callback_data=f"cat_{channel_id}"
        ),
        row=2
    )


    keyboard.add(
        InlineKeyboardButton(
            "✏️ متن پایین خبر",
            callback_data=f"link_{channel_id}"
        ),
        row=3
    )


    keyboard.add(
        InlineKeyboardButton(
            "🗑 حذف کانال",
            callback_data=f"delete_{channel_id}"
        ),
        row=3
    )


    return keyboard


# ==========================
# تایید حذف کانال
# ==========================

def delete_channel_menu(channel_id):

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "✅ بله",
            callback_data=f"yesdel_{channel_id}"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "❌ خیر",
            callback_data=f"nodel_{channel_id}"
        ),
        row=1
    )


    return keyboard



# ==========================
# بازگشت
# ==========================

def back_menu():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton(BTN_BACK),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton(BTN_HOME),
        row=1
    )

    return keyboard



# ==========================
# انصراف
# ==========================

def cancel_menu():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton(BTN_CANCEL),
        row=1
    )

    return keyboard
    
    
# ==========================
# پیش نمایش متن پایین خبر
# ==========================

def footer_preview_menu():

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "✅ تایید",
            callback_data="footer_save"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "✏️ ویرایش",
            callback_data="footer_edit"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "❌ انصراف",
            callback_data="footer_cancel"
        ),
        row=2
    )

    return keyboard
    
    

# ==========================
# پیش نمایش متن پایین خبر
# ==========================

def footer_preview_menu():

    keyboard = InlineKeyboardMarkup()


    keyboard.add(
        InlineKeyboardButton(
            "✅ تایید",
            callback_data="footer_save"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "✏️ ویرایش",
            callback_data="footer_edit"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "❌ انصراف",
            callback_data="footer_cancel"
        ),
        row=2
    )


    return keyboard



# ==========================
# مدیریت متن پایین خبر
# ==========================

def footer_manage_menu():

    keyboard = InlineKeyboardMarkup()


    keyboard.add(
        InlineKeyboardButton(
            "✏️ تغییر متن",
            callback_data="footer_edit"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "🗑 حذف متن",
            callback_data="footer_delete"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "🔙 بازگشت",
            callback_data="footer_back"
        ),
        row=2
    )


    return keyboard



# ==========================
# تایید حذف متن پایین خبر
# ==========================

def footer_delete_menu():

    keyboard = InlineKeyboardMarkup()


    keyboard.add(
        InlineKeyboardButton(
            "✅ بله، حذف شود",
            callback_data="footer_delete_yes"
        ),
        row=1
    )


    keyboard.add(
        InlineKeyboardButton(
            "❌ خیر",
            callback_data="footer_delete_no"
        ),
        row=1
    )


    return keyboard
    
    
# ==========================
# منوی دسته بندی خبر
# ==========================

def category_menu():

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "🚨 جنگ و حوادث",
            callback_data="cat_select_جنگ"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "💵 اقتصاد و بازار",
            callback_data="cat_select_اقتصاد"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "🌐 فناوری و اینترنت",
            callback_data="cat_select_فناوری"
        ),
        row=2
    )

    keyboard.add(
        InlineKeyboardButton(
            "⚽ ورزش",
            callback_data="cat_select_ورزش"
        ),
        row=2
    )

    keyboard.add(
        InlineKeyboardButton(
            "🏛 سیاسی",
            callback_data="cat_select_سیاسی"
        ),
        row=3
    )

    keyboard.add(
        InlineKeyboardButton(
            "🌍 همه دسته‌ها",
            callback_data="cat_select_همه"
        ),
        row=3
    )
    
    keyboard.add(
        InlineKeyboardButton(
            "💾 ذخیره",
            callback_data="cat_save"
        ),
        row=4
    )

    return keyboard
    
    
    # ==========================
# منوی زمان ارسال
# ==========================

def send_time_menu(channel_id):

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "🕐 ۱ دقیقه",
            callback_data=f"stime_1_{channel_id}"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "🕔 ۵ دقیقه",
            callback_data=f"stime_5_{channel_id}"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "🕙 ۱۰ دقیقه",
            callback_data=f"stime_10_{channel_id}"
        ),
        row=2
    )

    keyboard.add(
        InlineKeyboardButton(
            "🕒 ۱۵ دقیقه",
            callback_data=f"stime_15_{channel_id}"
        ),
        row=2
    )

    keyboard.add(
        InlineKeyboardButton(
            "🕞 ۳۰ دقیقه",
            callback_data=f"stime_30_{channel_id}"
        ),
        row=3
    )

    keyboard.add(
        InlineKeyboardButton(
            "🕐 ۶۰ دقیقه",
            callback_data=f"stime_60_{channel_id}"
        ),
        row=3
    )

    return keyboard
    
    # ==========================
# پنل مدیریت
# ==========================

def admin_menu():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(MenuKeyboardButton(BTN_ADMIN_STATS_USERS), row=1)
    keyboard.add(MenuKeyboardButton(BTN_ADMIN_STATS_CHANNELS), row=2)
    keyboard.add(MenuKeyboardButton(BTN_ADMIN_STATS_NEWS), row=3)

    keyboard.add(MenuKeyboardButton(BTN_ADMIN_USERS), row=4)
    keyboard.add(MenuKeyboardButton(BTN_ADMIN_CHANNELS), row=5)
    keyboard.add(MenuKeyboardButton(BTN_ADMIN_ADMINS), row=6)

    keyboard.add(MenuKeyboardButton(BTN_ADMIN_BROADCAST), row=7)

    keyboard.add(MenuKeyboardButton(BTN_ADMIN_SETTINGS), row=8)

    keyboard.add(MenuKeyboardButton(BTN_ADMIN_JOIN), row=9)

    keyboard.add(MenuKeyboardButton("🔙 بازگشت"), row=10)

    return keyboard	
    
    
    # ==========================
# صفحه بندی پنل مدیریت
# ==========================

def pagination_menu(page, total_pages, prefix):

    keyboard = InlineKeyboardMarkup()

    buttons = []

    if page > 0:
        buttons.append(
            InlineKeyboardButton(
                "⬅️",
                callback_data=f"{prefix}_{page-1}"
            )
        )

    buttons.append(
        InlineKeyboardButton(
            f"📄 {page+1} / {total_pages}",
            callback_data="ignore"
        )
    )

    if page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton(
                "➡️",
                callback_data=f"{prefix}_{page+1}"
            )
        )

    keyboard.add(*buttons, row=1)

    return keyboard