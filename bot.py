import os
import telebot
from telebot import types
import yt_dlp

TOKEN = '8606363844:AAHqMunymcZUXE0zM2ASGzsJwYDGSF-iBmI'
bot = telebot.TeleBot(TOKEN, threaded=True)

user_links = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga YouTube yoki Instagram linkini yuboring.")

@bot.message_handler(func=lambda message: message.text and ("youtube.com" in message.text or "youtu.be" in message.text or "instagram.com" in message.text))
def handle_link(message):
    user_links[message.chat.id] = message.text
    markup = types.InlineKeyboardMarkup()
    btn_video = types.InlineKeyboardButton("🎬 Video", callback_data="download_video")
    btn_audio = types.InlineKeyboardButton("🎵 Musiqa", callback_data="download_audio")
    markup.add(btn_video, btn_audio)
    bot.send_message(message.chat.id, "Formatni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["download_video", "download_audio"])
def callback_download(message_call):
    chat_id = message_call.message.chat.id
    url = user_links.get(chat_id)

    if not url:
        bot.send_message(chat_id, "📌 Iltimos, avval linkni yuboring!")
        return

    status_msg = bot.send_message(chat_id, "⏳ Yuklanmoqda...")

    ydl_opts = {
    'format': 'best' if is_video else 'bestaudio/best',
    'outtmpl': f'{chat_id}_download.%(ext)s',
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'mweb', 'tv'],
            'skip': ['webpage', 'configs']
        }
    },
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'en-US,en;q=0.9',
    },
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
}

    if message_call.data == "download_audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if message_call.data == "download_video":
            file_path = os.path.splitext(filename)[0] + '.mp4' if not filename.endswith('.mp4') else filename
            if os.path.exists(file_path):
                with open(file_path, 'rb') as video:
                    bot.send_video(chat_id, video, caption="🎬 Video yuklandi!")
        else:
            file_path = os.path.splitext(filename)[0] + '.mp3'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as audio:
                    bot.send_audio(chat_id, audio, caption="🎵 Musiqa yuklandi!")

    except Exception as e:
        print("Xatolik:", e)
        bot.send_message(chat_id, f"❌ Xatolik yuz berdi: {str(e)[:100]}")

    finally:
        for file in os.listdir():
            if str(chat_id) in file and not file.endswith('.py'):
                try:
                    os.remove(file)
                except Exception:
                    pass
        bot.delete_message(chat_id, status_msg.message_id)

print("Bot ishga tushdi...")
bot.infinity_polling(timeout=300, long_polling_timeout=300)
