import os
import logging
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

# لاگ‌گذاری
logging.basicConfig(level=logging.INFO)

# متغیرها
TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

# تابع هندلر
async def start(update, context):
    await update.message.reply_text("سلام! من آنلاینم 🤖")

# تابع اجرای ربات
async def run_bot():
    logging.info("✅ Starting Telegram polling...")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

if __name__ == "__main__":
    # اجرای ربات در یک Thread جدا
    def start_polling():
        asyncio.run(run_bot())

    threading.Thread(target=start_polling).start()

    # اجرای Flask برای باز بودن پورت
    logging.info(f"🌱 Starting Flask server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
