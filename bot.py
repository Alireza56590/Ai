import logging
from flask import Flask
from config import TELEGRAM_TOKEN, PORT
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message
import asyncio

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def health_check():
    return "✅ Bot is alive!", 200

async def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Starting Telegram polling...")
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    logging.info(f"Starting Flask server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
