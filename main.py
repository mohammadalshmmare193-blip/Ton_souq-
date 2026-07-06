import time
import requests

BOT_TOKEN = "8746835546:AAGjm15pv3l2qUJpbhynKwTuNW6KA_v8xqs"
CHANNEL_ID = -1003895483427

def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    response = requests.get(url).json()
    price = response['the-open-network']['usd']
    return price

def send_to_channel():
    try:
        price = get_ton_price()
        message = f"💎 TON Price: {price}$"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": message})
    except Exception as e:
        print(f"Error: {e}")

while True:
    send_to_channel()
    time.sleep(300)

