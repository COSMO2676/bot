import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8606363844:AAHqMunymcZUXE0zM2ASGzsJwYDGSF-iBmI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga biror rasm yuboring, uni Android ilovangiz yuklab olib fon rasmi qiladi.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Botga yuborilgan rasmni olish
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    # Rasmni kompyuter/serverga saqlash (yoki ilova to'g'ridan-to'g'ri yuklab oladi)
    file_path = "latest_wallpaper.jpg"
    await file.download_to_drive(file_path)
    
    await update.message.reply_text("Rasm qabul qilindi! Android ilova bu rasmni ekranga o'rnatadi.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot ishga tushdi...")
    app.run_polling()

if name == 'main':
    main()
