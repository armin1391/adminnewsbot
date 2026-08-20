import json
import os

from config import SENT_NEWS_FILE, USERS_FILE


def ensure_storage():
    """
    ساخت خودکار پوشه و فایل ذخیره‌سازی
    """

    folder = os.path.dirname(SENT_NEWS_FILE)

    if folder:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(SENT_NEWS_FILE):
        with open(SENT_NEWS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)


def load_sent_news():

    ensure_storage()

    try:

        with open(SENT_NEWS_FILE, "r", encoding="utf-8") as file:

            data = json.load(file)

            if isinstance(data, list):
                return set(data)

            return set()

    except (json.JSONDecodeError, FileNotFoundError):

        with open(SENT_NEWS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        return set()

    except Exception as e:

        print("❌ خطا در خواندن فایل ذخیره‌سازی:", e)
        return set()


def save_sent_news(sent_news):

    ensure_storage()

    try:

        with open(SENT_NEWS_FILE, "w", encoding="utf-8") as file:

            json.dump(
                list(sent_news),
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:

        print("❌ خطا در ذخیره فایل:", e)


def load_users():

    try:

        with open(USERS_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except FileNotFoundError:

        return {}

    except json.JSONDecodeError:

        return {}

    except Exception as e:

        print("❌ خطا در خواندن users.json:", e)

        return {}