import os
from keep_alive import keep_alive
import telebot
import google.generativeai as genai

# Pobieranie tokenów z ustawień Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Konfiguracja Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicjalizacja bota
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(message, "Cześć! Jestem gotowy do działania.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(message, f"Wystąpił błąd: {e}")


if __name__ == "__main__":
  # Uruchomienie serwera utrzymującego działanie na Renderze
  keep_alive()
  # Start bota Telegrama
  bot.infinity_polling()
