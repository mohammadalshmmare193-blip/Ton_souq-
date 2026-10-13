import os
import time
import requests
from datetime import datetime

# سحب التوكن والمعرف من متغيرات البيئة بأمان تام
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@ton_souq")

if not TOKEN:
    raise ValueError("Error: BOT_TOKEN is not set in environment variables!")

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def generate_progress_bar(change_val):
    abs_val = abs(change_val)
    if abs_val >= 5:
        filled_count = 5
    elif abs_val >= 3:
        filled_count = 4
    elif abs_val >= 2:
        filled_count = 3
    elif abs_val >= 1:
        filled_count = 2
    elif abs_val > 0:
        filled_count = 1
    else:
        filled_count = 0

    empty_count = 5 - filled_count

    if change_val > 0:
        return "🟢 " + ("▇" * filled_count) + ("░" * empty_count)
    elif change_val < 0:
        return "🔴 " + ("▇" * filled_count) + ("░" * empty_count)
    else:
        return "⚪ ░░░░░"

def fetch_ton_data():
    current_usd = 1.40  
    change_24h = 0.0
    
    iqd_rate = 1520   # السعر الرسمي المحدث للبنك المركزي
    asia_rate = 1580  # سعر التحويلات أو أسياسيل التقريبي بناءً على السوق
    
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=the-open-network"
        res = requests.get(url, timeout=10).json()
        if res and len(res) > 0:
            current_usd = res[0]['current_price']
            change_24h = res[0]['price_change_percentage_24h'] or 0.0
    except:
        pass

    iqd = int(current_usd * iqd_rate)
    asia = int(current_usd * asia_rate)
    progress = generate_progress_bar(change_24h)

    return {
        "title": "عملة تونكوين (TON)",
        "usd": f"\${current_usd:,.2f}",
        "iqd": f"{iqd:,} د.ع",
        "asia": f"{asia:,} د.ع",
        "progress": progress,
        "change_24h": f"{change_24h:+.2f}%"
    }

def send_ton_message(item):
    current_time = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
    
    msg = "╔═══════════════════════╗\n"
    msg += f"🔹 **{item['title']}**\n"
    msg += "╠═══════════════════════╣\n"
    msg += f"💵 الدولار: `{item['usd']}`\n"
    msg += f"🇮🇶 الدينار: `{item['iqd']}`\n"
    msg += f"🌐 أسياسيل: `{item['asia']}`\n"
    msg += f"📈 المؤشر: {item['progress']} `({item['change_24h']})`\n"
    msg += f"⏱ التحديث: {current_time}\n"
    msg += "╚═══════════════════════╝"
    
    payload = {
        "chat_id": CHANNEL_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(API_URL, json=payload, timeout=10)
    except:
        pass

def main():
    print("بدء تشغيل بوت سهم TON كـ Background Worker...")
    while True:
        try:
            ton_data = fetch_ton_data()
            send_ton_message(ton_data)
            print("تم إرسال تحديث TON بنجاح.")
        except Exception as e:
            print(f"خطأ: {e}")

        # الانتظار لمدة 5 دقائق (300 ثانية)
        time.sleep(300)

if __name__ == "__main__":
    main()
