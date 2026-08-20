# ==========================
# AutoNewsBot Config v1.6
# ==========================

# توکن ربات بله
BOT_TOKEN = "1484088959:S5Wy-ohXpUGvS6boDHTSoeeHwKBkXbGGdJ0"

# ==========================
# مسیر فایل‌ها
# ==========================

USERS_FILE = "data/users.json"
SENT_NEWS_FILE = "data/sent_news.json"

# ==========================
# تنظیمات خبر
# ==========================

# حداکثر تعداد خبرهای ذخیره شده
MAX_SENT_NEWS = 5000

# زمان بررسی در صورت نبود خبر
CHECK_EMPTY_INTERVAL = 60

# زمان انتظار بعد از ارسال خبر
SEND_INTERVALS = [300, 600]

# ==========================
# تنظیمات کانال‌ها
# ==========================

MAX_CHANNELS = 3

# ==========================
# RSS خبرگزاری‌ها
# ==========================

RSS_FEEDS = [

    # عمومی
    "https://www.tasnimnews.com/fa/rss/feed/0/7/0",
    "https://www.mehrnews.com/rss",
    "https://www.isna.ir/rss",

    # ایرنا
    "https://www.irna.ir/rss",

    # فارس
    "https://www.farsnews.ir/rss",

    # باشگاه خبرنگاران جوان
    "https://www.yjc.ir/fa/rss",

    # ایلنا
    "https://www.ilna.ir/rss",

    # صدا و سیما
    "https://www.iribnews.ir/fa/rss",

    # دفاع پرس
    "https://defapress.ir/fa/rss",

    # نورنیوز
    "https://nournews.ir/fa/rss",

    # اقتصاد
    "https://www.eghtesadnews.com/rss",

    # TGJU ارز و طلا
    "https://www.tgju.org/rss",

    # ورزش
    "https://www.varzesh3.com/rss",
    "https://www.khabarvarzeshi.com/rss",

    # فناوری
    "https://www.zoomit.ir/feed/",
]


# ==========================
# Category Rules v1.7
# ==========================

CATEGORY_RULES = {

    "ورزش": {

        "sources": [
            "varzesh3",
            "khabarvarzeshi"
        ],

        "keywords": [
            "فوتبال",
            "والیبال",
            "بسکتبال",
            "لیگ",
            "جام",
            "بازیکن",
            "مربی",
            "گل",
            "مسابقه",
            "تیم",
            "قهرمانی",
            "استقلال",
            "پرسپولیس"
        ],

        "negative": [
            "جنگ",
            "حمله نظامی",
            "موشک",
            "ارتش",
            "تحریم"
        ]
    },


    "اقتصاد": {

        "sources": [
            "tgju",
            "eghtesadnews"
        ],

        "keywords": [
            "دلار",
            "طلا",
            "سکه",
            "بورس",
            "ارز",
            "اقتصاد",
            "بازار",
            "تورم",
            "قیمت"
        ],

        "negative": [
            "فوتبال",
            "مسابقه",
            "جنگ"
        ]
    },


    "جنگ": {

        "sources": [
            "defapress",
            "noornews"
        ],

        "keywords": [
            "حمله",
            "موشک",
            "پهپاد",
            "ارتش",
            "نیروی نظامی",
            "عملیات",
            "درگیری",
            "جنگنده",
            "تجاوز",
            "شهادت"
        ],

        "negative": [
            "آتش سوزی",
            "جنگل",
            "حریق",
            "ورزش",
            "مسابقه"
        ]
    },


    "فناوری": {

        "sources": [
            "zoomit"
        ],

        "keywords": [
            "گوشی",
            "موبایل",
            "لپ تاپ",
            "هوش مصنوعی",
            "تکنولوژی",
            "اینترنت",
            "نرم افزار"
        ],

        "negative": [
            "جنگ",
            "اقتصاد"
        ]
    }

}

# ==========================
# Force Join
# ==========================

FORCE_JOIN_ENABLED = True

FORCE_JOIN_CHANNELS = [
    {
        "id": 5156805259,
        "username": "@adminbots_ir"
    }
]

