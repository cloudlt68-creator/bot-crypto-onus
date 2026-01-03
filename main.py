import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os

# --- CẤU HÌNH ---
TELEGRAM_TOKEN = '8524133533:AAFdCN27kW0fuTUPEOd-v0mlGudCBRe4M9I'
GEMINI_API_KEY = 'AIzaSyDuK-XTxbya5eh-PnNJISDBdbqlamRh3as'
MY_CHAT_ID = 5101441540

# --- FIX LỖI RENDER (MỞ CỔNG WEB) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is live!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- FIX LỖI AI (MODEL CHUẨN) ---
genai.configure(api_key=GEMINI_API_KEY)
# Sử dụng gemini-1.5-flash với đường dẫn đầy đủ
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != MY_CHAT_ID: return
    try:
        waiting_msg = bot.reply_to(message, "🔄 AI đang soi kèo...")
        response = model.generate_content(f"Bạn là chuyên gia ONUS, hãy phân tích: {message.text}")
        bot.edit_message_text(chat_id=MY_CHAT_ID, message_id=waiting_msg.message_id, text=response.text)
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    # Chạy cổng web giả ở luồng phụ để Render không tắt bot
    threading.Thread(target=run).start()
    print("--- BOT ĐÃ SẴN SÀNG ---")
    bot.infinity_polling()
