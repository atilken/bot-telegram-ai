import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Bot AI sudah aktif dan siap menjawab pertanyaan di grup. Cukup mention (@nama_bot) atau reply pesan saya.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_text = message.text
        response = model.generate_content(user_text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Maaf, terjadi kesalahan: {e}")

print("Bot Telegram AI sedang berjalan...")
bot.infinity_polling()
