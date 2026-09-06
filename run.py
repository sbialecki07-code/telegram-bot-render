import os
import time
import telebot
from telebot import types

# Pobieranie tokenu 
TOKEN = "8814824218:AAEbXtnRRtytHuIshnzNHF0-YvXFv7NjgOH"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Dyspozytor AI w chmurze gotowy do pracy. System operacyjny działa w trybie bezpiecznym.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Sztuczne opóźnienie dla stabilizacji obciążenia (zgodnie z regułami)
    time.sleep(0.5)
    
    user_text = message.text
    # Prosta odpowiedź testowa zwrotna
    bot.reply_to(message, f"Otrzymano polecenie: {user_text}. Łączność z chmurą stabilna.")

if __name__ == '__main__':
    print("Uruchamianie bota w trybie ciągłym...")
    bot.infinity_polling()


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
