from config import ADMIN_IDS
from services import get_user


def format_user(user_id):
    user = get_user(user_id)

    if not user:
        return str(user_id)

    username = user["username"]
    first_name = user["first_name"]

    if username:
        if not username.startswith("@"):
            username = f"@{username}"
        return username

    if first_name:
        return f"{first_name} (ID: {user_id})"

    return str(user_id)


def notify_admin_published(
    api_request,
    advertiser_id,
    owner_id,
    channel_username,
    price,
    content,
    advertisement_id
):
    buyer = format_user(advertiser_id)
    seller = format_user(owner_id)

    if channel_username:
        channel = channel_username
        if not channel.startswith("@"):
            channel = f"@{channel_username}"
    else:
        channel = "بدون یوزرنیم"

    admin_text = (
        "📢 تبلیغ با موفقیت منتشر شد\n\n"

        f"👤 خریدار: {buyer}\n"
        f"👤 خرید از: {seller}\n"
        f"📢 کانال: {channel}\n\n"

        f"💰 مبلغ تبلیغ: {price:,} سکه\n\n"

        "━━━━━━━━━━━━━━\n\n"

        "📝 متن بنر:\n\n"
        f"{content}\n\n"

        "━━━━━━━━━━━━━━\n\n"

        f"🆔 شماره سفارش: #{advertisement_id}\n"
        "✅ وضعیت: منتشر شده"
    )

    for admin_id in ADMIN_IDS:
        try:
            api_request(
                "sendMessage",
                {
                    "chat_id": admin_id,
                    "text": admin_text
                }
            )

        except Exception as error:
            print(
                f"❌ Admin publish notification error: {error}"
      )
