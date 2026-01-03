import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os

# --- CẤU HÌNH ---
TELEGRAM_TOKEN = '8524133533:AAFdCN27kW0fuTUPEOd-v0mlGudCBRe4M9I'
# Đã cập nhật API Key mới của bạn
GEMINI_API_KEY = 'AIzaSyC23x0tY6D6syUYLXP0fmRmM7zDrhnT46U'
MY_CHAT_ID = 5101441540

# --- FIX LỖI RENDER (PORT SCAN) ---
app = Flask('')
@app.route('/')
def home(): return "Bot Onus Live!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CẤU HÌNH AI (FIX LỖI 404) ---
genai.configure(api_key=GEMINI_API_KEY)
# Sử dụng tên model ổn định nhất
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != MY_CHAT_ID: return
    try:
        waiting_msg = bot.reply_to(message, "🔄 AI ONUS đang soi kèo...")
        # Gửi lệnh phân tích cho AI
        response = model.generate_content(f"Bạn là chuyên gia Crypto ONUS. Hãy phân tích: {message.text}")
        
        bot.edit_message_text(chat_id=MY_CHAT_ID, message_id=waiting_msg.message_id, text=response.text)
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    # Chạy cổng giả cho Render
    threading.Thread(target=run).start()
    
    # Xóa webhook cũ (Fix lỗi 409 Conflict)
    bot.remove_webhook()
    print("--- BOT STARTED WITH NEW API KEY ---")
    bot.infinity_polling(skip_pending=True)
