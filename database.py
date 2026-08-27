# ==============================
# AdMarketBot - database.py
# ==============================

import sqlite3
from pathlib import Path


# ==============================
# Database Path
# ==============================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "bot.db"


# ==============================
# Database Connection
# ==============================

def get_connection():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==============================
# Initialize Database
# ==============================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    # ==========================
    # Users
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            user_id INTEGER PRIMARY KEY,

            username TEXT,

            first_name TEXT,

            coins INTEGER NOT NULL DEFAULT 0,

            referral_id INTEGER,

            referral_rewarded INTEGER NOT NULL DEFAULT 0,

            last_wheel_date TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ==========================
    # Channels
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            owner_id INTEGER NOT NULL,

            channel_id TEXT NOT NULL UNIQUE,

            channel_username TEXT,

            channel_name TEXT,

            members INTEGER NOT NULL DEFAULT 0,

            daily_views INTEGER NOT NULL DEFAULT 0,

            ad_price INTEGER NOT NULL DEFAULT 0,

            status TEXT NOT NULL DEFAULT 'pending',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ==========================
    # Add daily_views to old DB
    # ==========================

    try:

        cursor.execute("""
            ALTER TABLE channels
            ADD COLUMN daily_views INTEGER NOT NULL DEFAULT 0
        """)

    except sqlite3.OperationalError:

        # ستون از قبل وجود دارد
        pass

    # ==========================
    # Advertisements
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advertisements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            advertiser_id INTEGER NOT NULL,

            channel_id INTEGER NOT NULL,

            content TEXT,

            price INTEGER NOT NULL DEFAULT 0,

            status TEXT NOT NULL DEFAULT 'pending',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ==========================
    # Coin Transactions
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            amount INTEGER NOT NULL,

            balance_after INTEGER NOT NULL,

            transaction_type TEXT NOT NULL,

            description TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ==========================
    # Referrals
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            inviter_id INTEGER NOT NULL,

            invited_id INTEGER NOT NULL UNIQUE,

            reward INTEGER NOT NULL DEFAULT 0,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


# ==============================
# Auto Initialize
# ==============================

if __name__ == "__main__":

    init_database()

    print(
        "✅ Database initialized successfully."
    )