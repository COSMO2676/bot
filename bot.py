import os
import telebot
import urllib.parse
from flask import Flask
from threading import Thread
import yt_dlp

TOKEN = 'YOUR_BOT_TOKEN_HERE'  # <- Shu yerga o'z bot tokeningizni qo'ying!
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot faol ishlamoqda!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "👋 Xush kelibsiz!\n\n"
        "1. Instagram Video Yuklash: Instagram havolasini yuboring.\n"
        "2. AI Rasm Generatsiya: /rasm so'zidan keyin rasm tasvirini yozing.\n\n"
        "✨ *Maslahat:* Aniqroq rasm chiqishi uchun ingliz tilida yozing (masalan: /rasm giant green hulk angry)."
    )
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['rasm'])
def generate_image(message):
    prompt = message.text.replace('/rasm', '').strip()
    
    if not prompt:
        bot.reply_to(message, "⚠️ Iltimos, rasm tasvirini yozing!\nMisol: /rasm hulk", parse_mode="Markdown")
        return

    msg = bot.reply_to(message, "🎨 Rasm chizilmoqda, biroz kuting...")
    
    try:
        # Promptni to'g'ridan-to'g'ri URL formatiga o'tkazish
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
        
        bot.send_photo(message.chat.id, image_url, caption=f"🖼 Natija: {prompt}")
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("❌ Rasm yaratishda xatolik yuz berdi.", message.chat.id, msg.message_id)

@bot.message_handler(func=lambda message: 'instagram.com' in message.text)
def download_instagram(message):
    url = message.text.strip()
    msg = bot.reply_to(message, "📥 Video yuklanmoqda, kuting...")
    
    chat_id = message.chat.id
    file_path = f"{chat_id}_insta.mp4"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        with open(file_path, 'rb') as video:
            bot.send_video(chat_id, video)
            
        bot.delete_message(chat_id, msg.message_id)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        bot.edit_message_text("❌ Videoni yuklashda xatolik yuz berdi.", chat_id, msg.message_id)
        if os.path.exists(file_path):
            os.remove(file_path)

bot.infinity_polling()
