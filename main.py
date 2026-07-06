import time
import requests
from flask import Flask
from threading import Thread

# هذا الجزء يخدع Render ليظن أن البوت موقع ويب ويعطيك حالة "Live"
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

# كود البوت الخاص بك يبدأ من هنا
BOT_TOKEN = "8746835546:AAGjm15pv3l2qUJpbhynKwTuNW6KA_v8xqs"
CHANNEL_ID = -1003895483427

# ... أكمل باقي الكود الخاص بك (دالة إرسال السعر والـ while loop) ...
