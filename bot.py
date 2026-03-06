import telebot
from telebot import types
import yt_dlp
import os

bot = telebot.TeleBot("8060441677:AAEYEarCDmN6wM0OoxXHW4m87lY7ODgVSQ4")

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def ask_format(message):
    url = message.text
    markup = types.InlineKeyboardMarkup()
    btn_mp3 = types.InlineKeyboardButton("🎧 MP3", callback_data=f"mp3|{url}")
    btn_mp4 = types.InlineKeyboardButton("🎬 MP4", callback_data=f"mp4|{url}")
    markup.add(btn_mp3, btn_mp4)
    bot.reply_to(message, "Select the type of download:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download_choice(call):
    data = call.data.split('|')
    format_type = data[0]
    url = data[1]
    
    bot.answer_callback_query(call.id, "Downloading, please wait...")
    
    # ပြင်ဆင်ချက် - ဖိုင်နာမည် အသေမသတ်မှတ်ဘဲ အလိုအလျောက် detect လုပ်စေခြင်း
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # ဒေါင်းပြီးသားဖိုင်ကို ပြန်ပို့ခြင်း
        if format_type == 'mp3':
            bot.send_audio(call.message.chat.id, open(filename, 'rb'))
        else:
            bot.send_video(call.message.chat.id, open(filename, 'rb'))
        
        # ဖိုင်ဖျက်ခြင်း
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        bot.reply_to(call.message, f"Error: {str(e)}")

# Render အတွက် bot.infinity_polling ကို သုံးပါ
bot.infinity_polling()
