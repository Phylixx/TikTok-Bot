import telebot
import requests
from flask import Flask
from threading import Thread

# ၁။ သင့် Token နှင့် Key များ
API_TOKEN = '8060441677:AAEYEarCDmN6wM0OoxXHW4m87lY7ODgVSQ4'
RAPIDAPI_KEY = '72690317d9msh749cae73607f169p14e193jsnf8d38d2b1573'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ၂။ Web Server အပိုင်း (Render အတွက် လိုအပ်သည်)
@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# ၃။ TikTok Downloader Function
@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tiktok(message):
    try:
        bot.reply_to(message, "ဗီဒီယိုကို ရှာဖွေနေပါတယ်...")
        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
        payload = {"url": message.text}
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()
        
        if data.get('code') == 0:
            bot.send_video(message.chat.id, data['data']['play'])
        else:
            bot.reply_to(message, "ဗီဒီယို ရှာမတွေ့ပါ။")
    except:
        bot.reply_to(message, "Error ဖြစ်နေပါသည်။")

# ၄။ Web Server နှင့် Bot ကို တစ်ပြိုင်နက် Run ခြင်း
if __name__ == "__main__":
    Thread(target=run_web_server).start()
    bot.polling()
    