# 🚀 AdMarketBot
_________________________
> ⚠️ **Copyright © 2026 AHZAR & Commander04. All Rights Reserved.**
>
> این پروژه و تمامی کدها، ساختارها و محتوای آن متعلق به **AHZAR & Commander04** بوده و هرگونه کپی، انتشار مجدد، فروش یا استفاده تجاری بدون اجازه صاحبان اثر مجاز نیست.
_________________________
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Bale-00AEEF?style=for-the-badge" alt="Bale">
  <img src="https://img.shields.io/badge/Database-SQLite-green?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
</p>

<p align="center">

**🤖 AdMarketBot** — یک سیستم مدیریت و خرید و فروش تبلیغات در پیام‌رسان **بله**

</p>

<p align="center">
  <b>⚡ سریع • ساده • قابل توسعه • مدیریت‌پذیر</b>
</p>

---

## 📌 درباره پروژه

**AdMarketBot** یک ربات مدیریت بازار تبلیغات برای پیام‌رسان **Bale** است که با زبان **Python** توسعه داده شده.

هدف پروژه ایجاد یک محیط ساده برای:

> 📢 صاحبان کانال‌ها → ثبت کانال و ارائه فضای تبلیغاتی
> 💰 تبلیغ‌دهندگان → پیدا کردن کانال مناسب و خرید تبلیغات
> 👨‍💼 مدیر → مدیریت کاربران، کانال‌ها و درخواست‌ها

این پروژه با ساختاری ساده و قابل توسعه طراحی شده تا در آینده بتوان امکانات بیشتری به آن اضافه کرد.

---

# ✨ Features

### 👤 سیستم کاربران

* 🆕 ایجاد حساب کاربری
* 💰 سیستم موجودی و Coin
* 🎁 دریافت پاداش
* 🎡 گردونه روزانه
* 👥 سیستم دعوت دوستان
* 🎯 دریافت پاداش Referral
* 📊 مدیریت اطلاعات کاربر

---

### 📢 مدیریت کانال

صاحبان کانال می‌توانند کانال خود را برای نمایش در بازار ثبت کنند.

امکانات:

* ➕ ثبت کانال
* 📝 ثبت اطلاعات کانال
* 💰 تعیین قیمت تبلیغات
* 👁 ثبت ویوی تقریبی
* ⏳ بررسی درخواست توسط مدیریت
* ✅ تأیید کانال
* ❌ رد درخواست
* 📋 نمایش کانال‌های تأییدشده

---

### 🛒 بازار تبلیغات

کاربران می‌توانند کانال‌های موجود در بازار را مشاهده کرده و فضای تبلیغاتی موردنظر خود را خریداری کنند.

فرآیند کلی:

```text
👤 User
   │
   ▼
🔎 مشاهده کانال‌ها
   │
   ▼
📊 بررسی قیمت و ویو
   │
   ▼
🛒 انتخاب تبلیغ
   │
   ▼
💰 پرداخت با Coin
   │
   ▼
📢 ثبت درخواست تبلیغ
```

---

### 💳 سیستم Coin

سیستم داخلی Coin برای انجام تراکنش‌های تبلیغاتی استفاده می‌شود.

نمونه:

```text
💰 موجودی فعلی: 5,000 Coin

📢 قیمت تبلیغ: 1,500 Coin

─────────────────

💸 پرداخت: -1,500 Coin
💰 موجودی جدید: 3,500 Coin
```

---

### 👥 Referral System

هر کاربر می‌تواند افراد جدیدی را به ربات دعوت کند و از سیستم Referral پاداش دریافت کند.

```text
👤 User A
   │
   │ دعوت
   ▼
👤 User B
   │
   ▼
🎁 پاداش Referral
```

---

### 🎡 Daily Wheel

سیستم **گردونه روزانه** برای ایجاد تعامل بیشتر کاربران.

کاربر می‌تواند در بازه مشخص از گردونه استفاده کرده و بر اساس نتیجه، پاداش دریافت کند.

```text
🎡 گردونه روزانه

        ↓

🎁 Reward

        ↓

💰 + Coin
```

---

# 🛠 Tech Stack

| Technology                   | Usage                   |
| ---------------------------- | ----------------------- |
| 🐍 **Python**                | زبان اصلی پروژه         |
| 🤖 **Bale Bot API**          | ارتباط با پیام‌رسان بله |
| 🌐 **Requests**              | ارسال درخواست‌های API   |
| 🗄️ **SQLite**               | ذخیره اطلاعات           |
| 🔐 **Environment Variables** | مدیریت اطلاعات حساس     |

---

# 📂 Project Structure

ساختار فعلی پروژه به شکل زیر است:

```text
AdMarketBot/
│
├── 📄 main.py
├── 📄 config.py
├── 📄 database.py
├── 📄 handlers.py
├── 📄 keyboards.py
├── 📄 services.py
├── 📄 requirements.txt
│
├── 📁 data/
│   └── 🗄️ Database / Data Files
│
└── 📄 .gitignore
```

### 🧩 توضیح فایل‌ها

#### `main.py`

نقطه شروع اجرای ربات و مدیریت فرآیند اصلی Bot.

```python
python main.py
```

---

#### `config.py`

تنظیمات پروژه و Configuration.

> ⚠️ اطلاعات حساس مانند Token نباید مستقیماً داخل GitHub قرار بگیرند.

---

#### `database.py`

مسئول ارتباط با دیتابیس و مدیریت اطلاعات ذخیره‌شده.

---

#### `handlers.py`

شامل منطق پردازش پیام‌ها، دستورات و تعاملات کاربران.

---

#### `keyboards.py`

ساخت Keyboardها و دکمه‌های رابط کاربری ربات.

---

#### `services.py`

منطق سرویس‌ها و عملیات اصلی پروژه.

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/armin1391/adminnewsbot.git
```

سپس:

```bash
cd adminnewsbot
```

---

## 2️⃣ ساخت Virtual Environment

پیشنهاد می‌شود از محیط مجازی Python استفاده کنید.

### Windows

```powershell
py -3.12 -m venv .venv
```

فعال‌سازی:

```powershell
.\.venv\Scripts\Activate.ps1
```

اگر PowerShell اجازه اجرای Script نداد:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

سپس دوباره:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3️⃣ نصب Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuration

قبل از اجرای ربات، تنظیمات موردنیاز را در Configuration پروژه قرار دهید.

برای اطلاعات حساس از Environment Variables استفاده کنید.

نمونه:

```env
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_ID=YOUR_ADMIN_ID
```

> 🚨 **هیچ‌وقت Bot Token واقعی را داخل Repository عمومی قرار ندهید.**

---

# ▶️ Run

بعد از نصب Dependencies و تنظیم Configuration:

```bash
python main.py
```

اگر همه چیز درست باشد، ربات شروع به دریافت Updateها خواهد کرد.

---

# 🗄️ Database

پروژه از **SQLite** برای ذخیره اطلاعات استفاده می‌کند.

اطلاعاتی مانند:

```text
👤 Users
💰 Coins
📢 Channels
🛒 Advertisements
👥 Referrals
🎡 Daily Rewards
```

در دیتابیس مدیریت می‌شوند.

---

# 🔄 How It Works

### 👤 User Flow

```text
/start
   │
   ▼
🏠 Main Menu
   │
   ├── 👤 Profile
   │
   ├── 💰 Wallet
   │
   ├── 🎡 Daily Wheel
   │
   ├── 👥 Referral
   │
   ├── 📢 Channel Market
   │
   └── 🛒 Buy Advertisement
```

---

### 📢 Channel Owner Flow

```text
👤 Channel Owner
       │
       ▼
📢 Register Channel
       │
       ▼
💰 Set Advertisement Price
       │
       ▼
👨‍💼 Admin Review
       │
   ┌───┴───┐
   ▼       ▼
  ✅       ❌
Approve   Reject
   │
   ▼
📢 Published in Market
```

---

### 🛒 Advertiser Flow

```text
🔎 Browse Market
      │
      ▼
📢 Select Channel
      │
      ▼
💰 Check Price
      │
      ▼
🛒 Buy Advertisement
      │
      ▼
💳 Pay with Coin
      │
      ▼
✅ Advertisement Request
```

---

# 👨‍💼 Admin System

مدیریت ربات می‌تواند درخواست‌های مختلف را بررسی کند.

از جمله:

* 📢 بررسی کانال‌ها
* ✅ تأیید کانال
* ❌ رد کانال
* 📋 مدیریت درخواست‌ها
* 👤 بررسی کاربران
* 🛒 بررسی تبلیغات
* 📩 ارتباط با صاحب کانال

---

# 🛡️ Security

امنیت اطلاعات پروژه اهمیت زیادی دارد.

### ❌ این کار را انجام ندهید:

```python
BOT_TOKEN = "123456789:REAL_TOKEN"
```

### ✅ به‌جای آن:

```env
BOT_TOKEN=YOUR_SECRET_TOKEN
```

و فایل `.env` را در `.gitignore` قرار دهید:

```gitignore
.env
__pycache__/
*.pyc
```

> 🔒 **Token = Secret**

اگر Token به‌صورت عمومی منتشر شد، باید در سریع‌ترین زمان ممکن آن را از طریق Bot management مربوطه **تعویض (Rotate)** کنید.

---

# 🚀 Future Plans

پروژه قابلیت توسعه زیادی دارد و می‌توان امکانات بیشتری به آن اضافه کرد.

برخی ایده‌ها:

* [ ] 📊 پنل آماری پیشرفته
* [ ] 📈 سیستم Analytics
* [ ] 💳 سیستم پرداخت پیشرفته
* [ ] 🔔 سیستم Notification
* [ ] 📢 سیستم تبلیغات زمان‌بندی‌شده
* [ ] 🧾 سیستم فاکتور
* [ ] ⭐ سیستم Rating برای کانال‌ها
* [ ] 🔎 جستجوی پیشرفته کانال‌ها
* [ ] 🏆 Leaderboard کاربران
* [ ] 🎁 سیستم Reward پیشرفته
* [ ] 🛡️ سیستم ضدتقلب
* [ ] ⚡ بهینه‌سازی Performance
* [ ] 🌐 Web Admin Panel
* [ ] 📱 رابط کاربری بهتر

---

# 🤝 Contributing

Pull Requestها و پیشنهادهای توسعه‌ای استقبال می‌شوند.

برای مشارکت:

```bash
git clone https://github.com/armin1391/adminnewsbot.git
```

سپس تغییرات خود را ایجاد کرده و Pull Request ارسال کنید.

---

# ⚠️ Disclaimer

این پروژه برای اهداف آموزشی و توسعه نرم‌افزار ارائه شده است.

مسئولیت نحوه استفاده از ربات و امکانات آن بر عهده استفاده‌کننده است.

---

# 📜 License

در حال حاضر License مشخصی برای پروژه تعریف نشده است.

در صورت تعیین License، این بخش به‌روزرسانی خواهد شد.

---

# ❤️ Credits

<p align="center">

### ساخته شده با ❤️ توسط

**AHZAR**

### و

**Commander04**
[@commander004](https://github.com/commander004)

</p>

---

<p align="center">

**⭐ اگر این پروژه براتون مفید بود، یک Star به Repository بدید!**

<br>

**Made with 🐍 Python & ❤️**

<br>

[⬆️ Back to Top](#-admarketbot)

</p>


_____________________________
> ⚠️ **Copyright © 2026 AHZAR & Commander04. All Rights Reserved.**
>
> این پروژه و تمامی کدها، ساختارها و محتوای آن متعلق به **AHZAR & Commander04** بوده و هرگونه کپی، انتشار مجدد، فروش یا استفاده تجاری بدون اجازه صاحبان اثر مجاز نیست.
> ___________________________
