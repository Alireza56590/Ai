import os
import logging
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route('/')
def home():
    logging.info("✅ Flask root endpoint called (health check)")
    return "✅ Bot is alive!"

async def start(update, context):
    logging.info(f"📩 Received /start from user {update.effective_user.id}")
    await update.message.reply_text("سلام! من آنلاینم 🤖")

async def run_bot():
    logging.info("🚀 Starting Telegram polling...")
    try:
        application = ApplicationBuilder().token(TOKEN).build()
        logging.info("📦 Application built, adding handlers...")
        application.add_handler(CommandHandler("start", start))
        await application.run_polling()
        logging.info("✅ Polling finished normally (should not happen)")
    except Exception as e:
        logging.error(f"❌ Exception in run_bot: {e}")

if __name__ == "__main__":
    logging.info("🔧 Main script started")

    def start_polling():
        logging.info("🧵 Polling thread starting...")
        try:
            asyncio.run(run_bot())
        except Exception as e:
            logging.error(f"❌ Exception in polling thread: {e}")

    threading.Thread(target=start_polling, name="PollingThread").start()

    logging.info(f"🌱 Starting Flask server on port {PORT}")
    try:
        app.run(host="0.0.0.0", port=PORT)
    except Exception as e:
        logging.error(f"❌ Exception in Flask server: {e}")
