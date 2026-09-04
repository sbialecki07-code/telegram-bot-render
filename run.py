import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_FILE = "bot_memory.db"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-3.7-flash')
from keep_alive import keep_alive

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (user_id INTEGER, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_recent_history(user_id, limit=20):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM history WHERE user_id=? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": role, "parts": [content]} for role, content in reversed(rows)]

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, role, content) VALUES (?,?,?)", (user_id, role, content))
    conn.commit()
    conn.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    print(f"Wiadomość: {user_message}")

    await context.bot.send_chat_action(chat_id=user_id, action='typing')
    
    history = get_recent_history(user_id)
    chat_session = model.start_chat(history=history)

    try:
        response = await chat_session.send_message_async(user_message)
        bot_answer = response.text
        save_message(user_id, "user", user_message)
        save_message(user_id, "model", bot_answer)
        await update.message.reply_text(bot_answer)
    except Exception as e:
        print(f"Błąd: {e}")
        await update.message.reply_text("Problem z połączeniem z chmurą. Spróbuj za chwilę.")

if __name__ == '__main__':
    init_db()
    print("Baza danych gotowa.")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot uruchomiony i nasłuchuje! Naciśnij Ctrl+C, aby zatrzymać.")
    app.run_polling()
