import telebot
from telebot import types
import yt_dlp
import os
from flask import Flask
from threading import Thread

bot = telebot.TeleBot("8060441677:AAEYEarCDmN6wM0OoxXHW4m87lY7ODgVSQ4")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# TikTok Link တွေ့ရင် ခလုတ်ပြပေးမယ့် အပိုင်း
@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def ask_format(message):
    url = message.text
    markup = types.InlineKeyboardMarkup()
    # ဒီမှာ ခလုတ်နှစ်ခု ဖန်တီးပါတယ်
    btn_mp3 = types.InlineKeyboardButton("🎧 MP3 (Music)", callback_data=f"mp3|{url}")
    btn_mp4 = types.InlineKeyboardButton("🎬 MP4 (Video)", callback_data=f"mp4|{url}")
    markup.add(btn_mp3, btn_mp4)
    bot.reply_to(message, "👇Select the type of download:", reply_markup=markup)

# ခလုတ်ကို နှိပ်လိုက်ရင် အလုပ်လုပ်မယ့် အပိုင်း
@bot.callback_query_handler(func=lambda call: True)
def download_choice(call):
    data = call.data.split('|')
    format_type = data[0]
    url = data[1]
    
    bot.answer_callback_query(call.id, "Start video downloading...")
    
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
        'outtmpl': 'video.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        if format_type == 'mp3':
            bot.send_audio(call.message.chat.id, open(filename, 'rb'))
        else:
            bot.send_video(call.message.chat.id, open(filename, 'rb'))
        
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        bot.reply_to(call.message, f"Error: {str(e)}")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=8080)
    
