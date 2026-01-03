import os
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from flask import Flask

# ---- Gemini ----
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = model.generate_content(update.message.text)
    await update.message.reply_text(response.text)

def run_bot():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()

# ---- Fake Web Server for Render ----
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    web_app.run(host="0.0.0.0", port=10000)
