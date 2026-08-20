import json
import os
import time
from datetime import datetime


USERS_FILE = "data/users.json"



# ==========================
# Load Users
# ==========================

def load_users():

    os.makedirs("data", exist_ok=True)


    if not os.path.exists(USERS_FILE):

        with open(
            USERS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file,
                ensure_ascii=False,
                indent=4
            )


    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            users = json.load(file)

            print("===== USERS.JSON =====")
            print(users)
            print("======================")

            return users


    except (json.JSONDecodeError, OSError):

        return {}



# ==========================
# Save Users
# ==========================

def save_users(users):

    os.makedirs("data", exist_ok=True)


    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=4
        )



# ==========================
# Check User
# ==========================

def user_exists(user_id):

    users = load_users()

    return str(user_id) in users



# ==========================
# Add User
# ==========================

def add_user(user_id, first_name, username=None):

    users = load_users()

    user_id = str(user_id)


    if user_id not in users:

        users[user_id] = {

            "first_name": first_name,

            "username": username,

            "join_date":
                datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "wallet": 0,

            "channels": [],

            "subscription": {
                "type": None,
                "expire": None
            },

            "invited_by": None,

            "invite_count": 0,

            "is_admin": False
        }


        save_users(users)



# ==========================
# Get User
# ==========================

def get_user(user_id):

    users = load_users()

    return users.get(str(user_id))



# ==========================
# Update User
# ==========================

def update_user(user_id, data):

    users = load_users()

    user_id = str(user_id)


    if user_id in users:

        users[user_id].update(data)

        save_users(users)



# ==========================
# Add Channel
# ==========================

def add_channel(user_id, channel):

    users = load_users()

    user_id = str(user_id)


    if user_id not in users:

        return False


    channels = users[user_id]["channels"]


    if len(channels) >= 3:

        return False



    for item in channels:

        if item["id"] == channel:

            return False



    new_channel = {

        "id": channel,

        "status": "active",


        "send_image": True,

        "show_emoji": True,

        "footer_text": "",


        "interval": 10, 
        
        "last_send": 0,

        "categories": [
            "همه"
        ]

    }



    channels.append(new_channel)


    save_users(users)


    return True



# ==========================
# Delete Channel
# ==========================

def delete_channel(user_id, channel_id):

    users = load_users()

    user_id = str(user_id)


    if user_id not in users:

        return False



    channels = users[user_id]["channels"]



    for channel in channels:


        if channel["id"] == channel_id:


            channels.remove(channel)


            save_users(users)


            return True



    return False


# ==========================
# Toggle Channel Image
# ==========================

def toggle_channel_image(user_id, channel_id):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        return None

    channels = users[user_id]["channels"]

    for channel in channels:

        if channel["id"] == channel_id:

            channel["send_image"] = not channel.get(
                "send_image",
                True
            )

            save_users(users)

            return channel["send_image"]

    return None


# ==========================
# Toggle Channel Emoji
# ==========================

def toggle_channel_emoji(user_id, channel_id):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        return None

    channels = users[user_id]["channels"]

    for channel in channels:

        if channel["id"] == channel_id:

            channel["show_emoji"] = not channel.get(
                "show_emoji",
                True
            )

            save_users(users)

            return channel["show_emoji"]

    return None


# ==========================
# Update Channel Footer Text
# ==========================

def update_footer_text(user_id, channel_id, text):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        return False

    channels = users[user_id]["channels"]

    for channel in channels:

        if channel["id"] == channel_id:

            channel["footer_text"] = text

            save_users(users)

            return True

    return False


# ==========================
# Update Categories
# ==========================

def update_categories(user_id, channel_id, categories):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        return False

    channels = users[user_id]["channels"]

    for channel in channels:

        if channel["id"] == channel_id:

            channel["categories"] = categories

            save_users(users)

            return True

    return False
    
    
# ==========================
# Update Send Time
# ==========================

def update_send_time(user_id, channel_id, interval):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        return False


    channels = users[user_id].get(
        "channels",
        []
    )


    for channel in channels:

        if channel.get("id") == channel_id:

            channel["interval"] = int(interval)

            save_users(users)

            return True


    return False



# ==========================
# Update Last Send
# ==========================

def update_last_send(user_id, channel_id, last_send):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        return False


    channels = users[user_id].get(
        "channels",
        []
    )


    for channel in channels:

        if channel.get("id") == channel_id:

            channel["last_send"] = last_send

            save_users(users)

            return True


    return False