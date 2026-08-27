# ==============================
# AdMarketBot - main.py
# ==============================

import time
import requests

from config import BOT_TOKEN

from database import init_database

from handlers import (
    handle_message,
    handle_callback
)


# ==============================
# Bale API
# ==============================

API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


# ==============================
# API Request
# ==============================

def api_request(method, data=None):

    url = f"{API_URL}/{method}"

    try:

        response = requests.post(
            url,
            json=data or {},
            timeout=35
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("ok"):

            print(
                f"❌ API Error: {result}"
            )

            return None

        return result.get("result")

    except requests.RequestException as error:

        print(
            f"❌ Request Error: {error}"
        )

        return None

    except ValueError:

        print(
            "❌ Invalid API response"
        )

        return None


# ==============================
# Get Updates
# ==============================

def get_updates(offset=None):

    data = {
        "timeout": 30
    }

    if offset is not None:

        data["offset"] = offset

    return api_request(
        "getUpdates",
        data
    )


# ==============================
# Process Update
# ==============================

def process_update(update):

    # ==========================
    # Message
    # ==========================

    message = update.get("message")

    if message:

        handle_message(
            api_request,
            message
        )

        return

    # ==========================
    # Callback Query
    # ==========================

    callback_query = update.get("callback_query")

    if callback_query:

        handle_callback(
            api_request,
            callback_query
        )


# ==============================
# Main
# ==============================

def main():

    print(
        "🚀 AdMarketBot Starting..."
    )

    # ==========================
    # Database
    # ==========================

    init_database()

    print(
        "🗄️ Database initialized."
    )

    # ==========================
    # Check Bot
    # ==========================

    me = api_request(
        "getMe"
    )

    if not me:

        print(
            "❌ Could not connect to Bale API."
        )

        return

    print(
        f"🤖 Bot: "
        f"{me.get('first_name', 'Unknown')} "
        f"(@{me.get('username', 'Unknown')})"
    )

    # ==========================
    # Polling
    # ==========================

    offset = None

    while True:

        try:

            updates = get_updates(
                offset
            )

            if updates:

                for update in updates:

                    update_id = update.get(
                        "update_id"
                    )

                    if update_id is not None:

                        offset = update_id + 1

                    print(
                        f"📩 Update: {update_id}"
                    )

                    process_update(
                        update
                    )

        except KeyboardInterrupt:

            print(
                "\n🛑 Bot stopped."
            )

            break

        except Exception as error:

            print(
                f"❌ Main Error: {error}"
            )

            time.sleep(3)


# ==============================
# Run
# ==============================

if __name__ == "__main__":

    main()