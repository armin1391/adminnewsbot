# ==============================
# AdMarketBot - services.py
# ==============================

import random
from datetime import datetime

from database import get_connection


# ==============================
# Settings
# ==============================

REFERRAL_REWARD = 10

WHEEL_MIN_REWARD = 1
WHEEL_MAX_REWARD = 100


# ==============================
# Users
# ==============================

def create_user(
    user_id,
    username=None,
    first_name=None,
    referral_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT OR IGNORE INTO users (
                user_id,
                username,
                first_name,
                referral_id
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                first_name,
                referral_id
            )
        )

        connection.commit()

    except Exception as error:

        print(
            f"❌ create_user error: {error}"
        )

        connection.rollback()

    finally:

        connection.close()


def get_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:

        connection.close()


# ==============================
# Coins
# ==============================

def get_coins(user_id):

    user = get_user(user_id)

    if not user:
        return 0

    return user["coins"]


def add_coins(
    user_id,
    amount,
    transaction_type="reward",
    description=None
):

    if amount <= 0:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT coins
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return False

        current_balance = user["coins"]

        new_balance = (
            current_balance + amount
        )

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_balance,
                user_id
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                amount,
                new_balance,
                transaction_type,
                description
            )
        )

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ add_coins error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


def remove_coins(
    user_id,
    amount,
    transaction_type="spend",
    description=None
):

    if amount <= 0:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT coins
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return False

        current_balance = user["coins"]

        if current_balance < amount:
            return False

        new_balance = (
            current_balance - amount
        )

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_balance,
                user_id
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                -amount,
                new_balance,
                transaction_type,
                description
            )
        )

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ remove_coins error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Transfer Coins
# ==============================

def transfer_coins(
    sender_id,
    receiver_id,
    amount,
    description=None
):

    if amount <= 0:
        return False

    if sender_id == receiver_id:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT coins
            FROM users
            WHERE user_id = ?
            """,
            (sender_id,)
        )

        sender = cursor.fetchone()

        if not sender:
            return False

        sender_balance = sender["coins"]

        if sender_balance < amount:
            return False

        cursor.execute(
            """
            SELECT coins
            FROM users
            WHERE user_id = ?
            """,
            (receiver_id,)
        )

        receiver = cursor.fetchone()

        if not receiver:
            return False

        receiver_balance = receiver["coins"]

        new_sender_balance = (
            sender_balance - amount
        )

        new_receiver_balance = (
            receiver_balance + amount
        )

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_sender_balance,
                sender_id
            )
        )

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_receiver_balance,
                receiver_id
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                sender_id,
                -amount,
                new_sender_balance,
                "transfer_out",
                description
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                receiver_id,
                amount,
                new_receiver_balance,
                "transfer_in",
                description
            )
        )

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ transfer_coins error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Daily Wheel
# ==============================

def spin_daily_wheel(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT coins, last_wheel_date
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:

            return {
                "success": False,
                "reason": "user_not_found"
            }

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        if user["last_wheel_date"] == today:

            return {
                "success": False,
                "reason": "already_spun"
            }

        reward = random.randint(
            WHEEL_MIN_REWARD,
            WHEEL_MAX_REWARD
        )

        current_balance = user["coins"]

        new_balance = (
            current_balance + reward
        )

        cursor.execute(
            """
            UPDATE users
            SET coins = ?,
                last_wheel_date = ?
            WHERE user_id = ?
            """,
            (
                new_balance,
                today,
                user_id
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                reward,
                new_balance,
                "daily_wheel",
                "جایزه گردونه روزانه"
            )
        )

        connection.commit()

        return {
            "success": True,
            "reward": reward,
            "balance": new_balance
        }

    except Exception as error:

        print(
            f"❌ spin_daily_wheel error: {error}"
        )

        connection.rollback()

        return {
            "success": False,
            "reason": "database_error"
        }

    finally:

        connection.close()


# ==============================
# Referral Count
# ==============================

def get_referral_count(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM referrals
            WHERE inviter_id = ?
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        return result[0]

    finally:

        connection.close()


# ==============================
# Process Referral
# ==============================

def process_referral(
    new_user_id,
    inviter_id
):

    if new_user_id == inviter_id:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE user_id = ?
            """,
            (new_user_id,)
        )

        new_user = cursor.fetchone()

        if not new_user:
            return False

        cursor.execute(
            """
            SELECT user_id, coins
            FROM users
            WHERE user_id = ?
            """,
            (inviter_id,)
        )

        inviter = cursor.fetchone()

        if not inviter:
            return False

        cursor.execute(
            """
            SELECT id
            FROM referrals
            WHERE invited_id = ?
            """,
            (new_user_id,)
        )

        existing = cursor.fetchone()

        if existing:
            return False

        cursor.execute(
            """
            INSERT INTO referrals (
                inviter_id,
                invited_id,
                reward
            )
            VALUES (?, ?, ?)
            """,
            (
                inviter_id,
                new_user_id,
                REFERRAL_REWARD
            )
        )

        current_balance = inviter["coins"]

        new_balance = (
            current_balance + REFERRAL_REWARD
        )

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_balance,
                inviter_id
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                inviter_id,
                REFERRAL_REWARD,
                new_balance,
                "referral",
                "پاداش دعوت دوست"
            )
        )

        connection.commit()

        return inviter_id

    except Exception as error:

        print(
            f"❌ process_referral error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Channels
# ==============================

def add_channel(
    owner_id,
    channel_id,
    channel_username,
    channel_name=None
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO channels (
                owner_id,
                channel_id,
                channel_username,
                channel_name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                owner_id,
                str(channel_id),
                channel_username,
                channel_name
            )
        )

        connection.commit()

        return cursor.lastrowid

    except Exception as error:

        print(
            f"❌ add_channel error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


def get_channel(channel_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE channel_id = ?
            """,
            (str(channel_id),)
        )

        return cursor.fetchone()

    finally:

        connection.close()


def get_user_channels(owner_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE owner_id = ?
            ORDER BY id DESC
            """,
            (owner_id,)
        )

        return cursor.fetchall()

    finally:

        connection.close()


def get_channel_by_owner(
    channel_id,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE channel_id = ?
            AND owner_id = ?
            """,
            (
                str(channel_id),
                owner_id
            )
        )

        return cursor.fetchone()

    finally:

        connection.close()


# ==============================
# Delete Channel
# ==============================

def delete_channel(
    channel_id,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM channels
            WHERE channel_id = ?
            AND owner_id = ?
            """,
            (
                str(channel_id),
                owner_id
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ delete_channel error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Set Advertisement Price
# ==============================

def set_channel_ad_price(
    channel_id,
    price,
    daily_views
):

    if price <= 0:
        return False

    if daily_views <= 0:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE channels
            SET ad_price = ?,
                daily_views = ?,
                status = 'price_pending'
            WHERE channel_id = ?
            """,
            (
                price,
                daily_views,
                str(channel_id)
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ set_channel_ad_price error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Update Channel Status
# ==============================

def update_channel_status(
    channel_id,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE channels
            SET status = ?
            WHERE channel_id = ?
            """,
            (
                status,
                str(channel_id)
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ update_channel_status error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Get Pending Price Requests
# ==============================

def get_pending_price_requests():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE status = 'price_pending'
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()

    finally:

        connection.close()
        
# ==============================
# Delete Channel
# ==============================

def delete_channel(
    channel_id,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM channels
            WHERE channel_id = ?
            AND owner_id = ?
            """,
            (
                str(channel_id),
                owner_id
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except Exception as error:

        print(
            f"❌ delete_channel error: {error}"
        )

        connection.rollback()

        return False

    finally:

        connection.close()


# ==============================
# Get Channel For Owner
# ==============================

def get_channel_for_owner(
    channel_id,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE channel_id = ?
            AND owner_id = ?
            """,
            (
                str(channel_id),
                owner_id
            )
        )

        return cursor.fetchone()

    finally:

        connection.close()


# ==============================
# Check Channel Ownership
# ==============================

def is_channel_owner(
    channel_id,
    owner_id
):

    channel = get_channel_for_owner(
        channel_id,
        owner_id
    )

    return channel is not None
    
# ==============================
# Get Approved Advertising Channels
# ==============================

def get_approved_channels():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE status = 'approved'
            AND ad_price > 0
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    except Exception as error:

        print(
            f"❌ get_approved_channels error: {error}"
        )

        return []

    finally:

        connection.close()
        
        
# ==============================
# Advertisements
# ==============================

def create_advertisement(
    advertiser_id,
    channel_id,
    content
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # --------------------------
        # Get Channel
        # --------------------------

        cursor.execute(
            """
            SELECT *
            FROM channels
            WHERE channel_id = ?
            AND status = 'approved'
            AND ad_price > 0
            """,
            (str(channel_id),)
        )

        channel = cursor.fetchone()

        if not channel:

            return {
                "success": False,
                "reason": "channel_not_available"
            }

        price = channel["ad_price"]
        owner_id = channel["owner_id"]

        # --------------------------
        # Get Advertiser
        # --------------------------

        cursor.execute(
            """
            SELECT coins
            FROM users
            WHERE user_id = ?
            """,
            (advertiser_id,)
        )

        advertiser = cursor.fetchone()

        if not advertiser:

            return {
                "success": False,
                "reason": "user_not_found"
            }

        balance = advertiser["coins"]

        # --------------------------
        # Check Balance
        # --------------------------

        if balance < price:

            return {
                "success": False,
                "reason": "insufficient_coins",
                "price": price,
                "balance": balance
            }

        # --------------------------
        # Deduct Coins
        # --------------------------

        new_balance = balance - price

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_balance,
                advertiser_id
            )
        )

        # --------------------------
        # Create Advertisement
        # --------------------------

        cursor.execute(
            """
            INSERT INTO advertisements (
                advertiser_id,
                channel_id,
                content,
                price,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                advertiser_id,
                channel["id"],
                content,
                price,
                "pending"
            )
        )

        advertisement_id = cursor.lastrowid

        # --------------------------
        # Transaction
        # --------------------------

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                advertiser_id,
                -price,
                new_balance,
                "advertisement_purchase",
                f"خرید تبلیغ در کانال {channel['channel_username']}"
            )
        )

        connection.commit()

        return {
            "success": True,
            "advertisement_id": advertisement_id,
            "channel_id": channel["channel_id"],
            "channel_db_id": channel["id"],
            "owner_id": owner_id,
            "price": price,
            "balance": new_balance
        }

    except Exception as error:

        print(
            f"❌ create_advertisement error: {error}"
        )

        connection.rollback()

        return {
            "success": False,
            "reason": "database_error"
        }

    finally:

        connection.close()


# ==============================
# Get Advertisement
# ==============================

def get_advertisement(
    advertisement_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                advertisements.*,
                channels.channel_id AS bale_channel_id,
                channels.channel_username,
                channels.channel_name,
                channels.owner_id
            FROM advertisements

            INNER JOIN channels
                ON advertisements.channel_id = channels.id

            WHERE advertisements.id = ?
            """,
            (advertisement_id,)
        )

        return cursor.fetchone()

    finally:

        connection.close()


# ==============================
# Get Pending Advertisement
# ==============================

def get_pending_advertisement(
    advertisement_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                advertisements.*,
                channels.channel_id AS bale_channel_id,
                channels.channel_username,
                channels.channel_name,
                channels.owner_id

            FROM advertisements

            INNER JOIN channels
                ON advertisements.channel_id = channels.id

            WHERE advertisements.id = ?
            AND advertisements.status = 'pending'
            """,
            (advertisement_id,)
        )

        return cursor.fetchone()

    finally:

        connection.close()


# ==============================
# Approve Advertisement
# ==============================

def approve_advertisement(
    advertisement_id,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                advertisements.*,
                channels.owner_id AS channel_owner_id

            FROM advertisements

            INNER JOIN channels
                ON advertisements.channel_id = channels.id

            WHERE advertisements.id = ?
            AND advertisements.status = 'pending'
            """,
            (advertisement_id,)
        )

        advertisement = cursor.fetchone()

        if not advertisement:

            return {
                "success": False,
                "reason": "not_found"
            }

        # --------------------------
        # Check Channel Owner
        # --------------------------

        if advertisement["channel_owner_id"] != owner_id:

            return {
                "success": False,
                "reason": "not_owner"
            }

        # --------------------------
        # Approve
        # --------------------------

        cursor.execute(
            """
            UPDATE advertisements
            SET status = 'approved'
            WHERE id = ?
            AND status = 'pending'
            """,
            (advertisement_id,)
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return {
                "success": False,
                "reason": "already_processed"
            }

        connection.commit()

        return {
            "success": True,
            "advertisement_id": advertisement_id,
            "advertiser_id": advertisement["advertiser_id"],
            "price": advertisement["price"],
            "content": advertisement["content"]
        }

    except Exception as error:

        print(
            f"❌ approve_advertisement error: {error}"
        )

        connection.rollback()

        return {
            "success": False,
            "reason": "database_error"
        }

    finally:

        connection.close()


# ==============================
# Reject Advertisement
# ==============================

def reject_advertisement(
    advertisement_id,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                advertisements.*,
                channels.owner_id AS channel_owner_id

            FROM advertisements

            INNER JOIN channels
                ON advertisements.channel_id = channels.id

            WHERE advertisements.id = ?
            AND advertisements.status = 'pending'
            """,
            (advertisement_id,)
        )

        advertisement = cursor.fetchone()

        if not advertisement:

            return {
                "success": False,
                "reason": "not_found"
            }

        # --------------------------
        # Check Channel Owner
        # --------------------------

        if advertisement["channel_owner_id"] != owner_id:

            return {
                "success": False,
                "reason": "not_owner"
            }

        advertiser_id = advertisement["advertiser_id"]
        price = advertisement["price"]

        # --------------------------
        # Get Current Balance
        # --------------------------

        cursor.execute(
            """
            SELECT coins
            FROM users
            WHERE user_id = ?
            """,
            (advertiser_id,)
        )

        advertiser = cursor.fetchone()

        if not advertiser:

            connection.rollback()

            return {
                "success": False,
                "reason": "advertiser_not_found"
            }

        current_balance = advertiser["coins"]

        new_balance = current_balance + price

        # --------------------------
        # Return Coins
        # --------------------------

        cursor.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_balance,
                advertiser_id
            )
        )

        # --------------------------
        # Change Advertisement Status
        # --------------------------

        cursor.execute(
            """
            UPDATE advertisements
            SET status = 'rejected'
            WHERE id = ?
            AND status = 'pending'
            """,
            (advertisement_id,)
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return {
                "success": False,
                "reason": "already_processed"
            }

        # --------------------------
        # Refund Transaction
        # --------------------------

        cursor.execute(
            """
            INSERT INTO transactions (
                user_id,
                amount,
                balance_after,
                transaction_type,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                advertiser_id,
                price,
                new_balance,
                "advertisement_refund",
                f"بازگشت وجه تبلیغ شماره {advertisement_id}"
            )
        )

        connection.commit()

        return {
            "success": True,
            "advertisement_id": advertisement_id,
            "advertiser_id": advertiser_id,
            "price": price,
            "balance": new_balance
        }

    except Exception as error:

        print(
            f"❌ reject_advertisement error: {error}"
        )

        connection.rollback()

        return {
            "success": False,
            "reason": "database_error"
        }

    finally:

        connection.close()