import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os

# --- CẤU HÌNH ---
TELEGRAM_TOKEN = '8524133533:AAFdCN27kW0fuTUPEOd-v0mlGudCBRe4M9I'
GEMINI_API_KEY = 'AIzaSyDuK-XTxbya5eh-PnNJISDBdbqlamRh3as'
MY_CHAT_ID = 5101441540

# --- FIX LỖI TIMEOUT TRÊN RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

def run():
    # Render yêu cầu mở một cổng (Port) để kiểm tra bot còn sống hay không
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- FIX LỖI 404 (Sử dụng tên model đầy đủ) ---
genai.configure(api_key=GEMINI_API_KEY)
# Thêm 'models/' vào trước tên để hệ thống nhận diện đúng
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != MY_CHAT_ID: return
    try:
        waiting_msg = bot.reply_to(message, "🔄 AI đang soi kèo, đợi chút...")
        prompt = f"Bạn là chuyên gia Crypto ONUS. Hãy phân tích kỹ thuật cho: {message.text}"
        response = model.generate_content(prompt)
        bot.edit_message_text(chat_id=MY_CHAT_ID, message_id=waiting_msg.message_id, text=response.text)
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    # Chạy cổng web giả ở luồng phụ
    threading.Thread(target=run).start()
    print("--- BOT ĐÃ SẴN SÀNG ---")
    bot.infinity_polling()
