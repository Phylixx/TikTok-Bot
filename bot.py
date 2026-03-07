import telebot
from telebot import types
import yt_dlp
import os
from flask import Flask
from threading import Thread

# သင့် Bot Token
BOT_TOKEN = "8060441677:AAEYEarCDmN6wM0OoxXHW4m87lY7ODgVSQ4"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def ask_format(message):
    url = message.text
    markup = types.InlineKeyboardMarkup()
    btn_mp3 = types.InlineKeyboardButton("🎧 MP3 (သီချင်း)", callback_data=f"mp3|{url}")
    btn_mp4 = types.InlineKeyboardButton("🎬 MP4 (Video)", callback_data=f"mp4|{url}")
    markup.add(btn_mp3, btn_mp4)
    bot.reply_to(message, "👇Select Tyle:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download_choice(call):
    # ခလုတ်ကို နှိပ်လိုက်တာနဲ့ ခလုတ်ကို ဖျောက်ပေးခြင်း
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        reply_markup=None
    )
    
    data = call.data.split('|')
    format_type = data[0]
    url = data[1]
    
    bot.answer_callback_query(call.id, "Downloading is starting...")
    
    try:
        # ဗီဒီယိုအရှည်ကို စစ်ဆေးခြင်း
        ydl_opts_info = {'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
        
        # ၃ မိနစ် (၁၈၀ စက္ကန့်) ကျော်ရင် ငြင်းပယ်ခြင်း
        if duration > 180:
            bot.reply_to(call.message, f"❌ Sorry , Video {int(duration/60)} cannot download because it is over a minute old.(It takes less than 3 minutes.)")
            return

        bot.reply_to(call.message, "Start Download Video⏳")
        
        ydl_opts = {
            'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
            'outtmpl': 'video.%(ext)s',
        }
        
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
