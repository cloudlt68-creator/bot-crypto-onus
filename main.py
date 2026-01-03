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

# --- FIX LỖI 404 (DÙNG MODEL LATEST) ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != MY_CHAT_ID: return
    try:
        waiting_msg = bot.reply_to(message, "🔄 AI ONUS đang soi kèo...")
        response = model.generate_content(f"Phân tích kỹ thuật chuyên sâu cho: {message.text}")
        bot.edit_message_text(chat_id=MY_CHAT_ID, message_id=waiting_msg.message_id, text=response.text)
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    # Chạy web server giả lập để Render báo Live
    threading.Thread(target=run).start()
    
    # FIX LỖI 409: Xóa mọi kết nối (webhook) cũ đang kẹt
    bot.remove_webhook()
    print("--- BOT ĐÃ SẴN SÀNG ---")
    bot.infinity_polling(skip_pending=True)
