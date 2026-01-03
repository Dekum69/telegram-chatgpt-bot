import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = model.generate_content(user_text)

    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
