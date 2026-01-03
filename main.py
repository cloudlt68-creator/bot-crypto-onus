import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os

# --- 1. CẤU HÌNH THÔNG SỐ (GIỮ NGUYÊN) ---
TELEGRAM_TOKEN = '8524133533:AAFdCN27kW0fuTUPEOd-v0mlGudCBRe4M9I'
GEMINI_API_KEY = 'AIzaSyDuK-XTxbya5eh-PnNJISDBdbqlamRh3as'
MY_CHAT_ID = 5101441540

# --- 2. FIX LỖI PORT SCAN (ĐỂ RENDER BÁO LIVE) ---
app = Flask('')
@app.route('/')
def home(): return "Bot Onus is Running!"

def run_web():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- 3. CẤU HÌNH AI (FIX LỖI 404) ---
genai.configure(api_key=GEMINI_API_KEY)
# Sử dụng model flash là bản ổn định nhất cho API tự do
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != MY_CHAT_ID: return
    try:
        waiting_msg = bot.reply_to(message, "🔄 AI đang soi kèo, đợi chút...")
        # Lệnh điều hướng chuyên sâu cho AI
        prompt = (
            f"Bạn là chuyên gia phân tích kỹ thuật Crypto sàn ONUS. "
            f"Hãy phân tích và đưa ra kèo (Entry, TP, SL) cho: {message.text}"
        )
        response = model.generate_content(prompt)
        bot.edit_message_text(chat_id=MY_CHAT_ID, message_id=waiting_msg.message_id, text=response.text)
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    # Chạy Web giả lập ở luồng phụ
    threading.Thread(target=run_web).start()
    print("--- BOT STARTED ---")
    # Khởi động Bot với chế độ xóa bỏ các kết nối cũ (Fix lỗi 409)
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
