
import os
import google.generativeai as genai
from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask
import threading

print("VERSION: STABLE TELEGRAM v13 BOT")

# ---- Gemini ----
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def reply(update, context):
    response = model.generate_content(update.message.text)
    update.message.reply_text(response.text)

def run_bot():
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    updater.start_polling()
    updater.idle()

# ---- Flask keep-alive ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
