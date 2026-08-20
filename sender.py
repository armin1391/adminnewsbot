
import requests

from config import BOT_TOKEN


BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


# ==========================
# ارسال متن
# ==========================

def send_message(channel_id, text):

    try:

        response = requests.post(
            f"{BASE_URL}/sendMessage",
            data={
                "chat_id": channel_id,
                "text": text
            },
            timeout=15
        )

        if response.status_code != 200:
            print(
                f"❌ خطا در ارسال متن به {channel_id}: "
                f"{response.status_code}"
            )

        return response.status_code

    except requests.RequestException as e:

        print(
            f"❌ خطای شبکه در ارسال متن به {channel_id}:",
            e
        )

        return None


# ==========================
# ارسال عکس
# ==========================

def send_photo(channel_id, photo_url, caption):

    if (
        not isinstance(photo_url, str)
        or
        not photo_url.startswith("http")
    ):

        return send_message(
            channel_id,
            caption
        )


    try:

        response = requests.post(
            f"{BASE_URL}/sendPhoto",
            data={
                "chat_id": channel_id,
                "photo": photo_url,
                "caption": caption
            },
            timeout=15
        )

        if response.status_code == 200:
            return 200


        print(
            f"⚠️ ارسال عکس به {channel_id} ناموفق بود "
            f"({response.status_code})"
        )

        return send_message(
            channel_id,
            caption
        )

    except requests.RequestException as e:

        print(
            f"❌ خطای شبکه در ارسال عکس به {channel_id}:",
            e
        )

        return send_message(
            channel_id,
            caption
        )