import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# Konfigurasi Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Inisialisasi klien Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = 'gemini-2.5-flash'

# Kamus untuk menyimpan riwayat chat pengguna
chat_sessions = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.message.from_user.id
    user_message = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action="typing"
    )

    try:
        if user_id not in chat_sessions:
            chat_sessions[user_id] = client.chats.create(model=MODEL_NAME)
        
        chat = chat_sessions[user_id]
        response = chat.send_message(user_message)
        bot_reply = response.text

        await update.message.reply_text(bot_reply)

    except Exception as e:
        logging.error(f"Error saat memproses pesan: {e}")
        await update.message.reply_text("Maaf, terjadi sedikit kendala saat menghubungi AI. Silakan coba sebentar lagi ya!")

def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        logging.error("TELEGRAM_TOKEN atau GEMINI_API_KEY belum disetel!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logging.info("Bot Telegram AI berhasil dijalankan!")
    application.run_polling()

if __name__ == '__main__':
    main()
