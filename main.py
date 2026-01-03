import telebot
import google.generativeai as genai

# --- PHẦN 1: THÔNG TIN CẤU HÌNH ---
TELEGRAM_TOKEN = '8524133533:AAFdCN27kW0fuTUPEOd-v0mlGudCBRe4M9I'
GEMINI_API_KEY = 'AIzaSyDuK-XTxbya5eh-PnNJISDBdbqlamRh3as'
MY_CHAT_ID = 5101441540 

# --- PHẦN 2: CẤU HÌNH AI GEMINI ---
genai.configure(api_key=GEMINI_API_KEY)

instruction = (
    "Bạn là chuyên gia phân tích kỹ thuật Crypto cho sàn ONUS. "
    "Khi nhận dữ liệu, hãy phân tích và trả về: "
    "1. Cặp tiền | 2. Lệnh (Long/Short) | 3. Entry | 4. TP (3 mức) | 5. SL. "
    "Trình bày ngắn gọn, dễ nhìn bằng tiếng Việt."
)

# Sửa thành gemini-pro để tránh lỗi 404 trên Render
model = genai.GenerativeModel(
    model_name='gemini-pro', 
    system_instruction=instruction
)

# --- PHẦN 3: CẤU HÌNH BOT TELEGRAM ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != MY_CHAT_ID:
        return
    try:
        waiting_msg = bot.reply_to(message, "🔄 AI đang soi kèo, đợi chút...")
        response = model.generate_content(message.text)
        bot.edit_message_text(chat_id=MY_CHAT_ID, message_id=waiting_msg.message_id, text=response.text)
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    print("--- BOT ĐÃ SẴN SÀNG CHẠY ---")
    bot.infinity_polling()
