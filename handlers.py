from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من آنلاینم 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in user_context:
        user_context[user_id] = []

    user_context[user_id].append({"role": "user", "content": user_message})

    if len(user_context[user_id]) > 10:
        user_context[user_id] = user_context[user_id][-10:]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "تو یک دستیار فارسی‌زبان هستی."},
            *user_context[user_id]
        ]
    )
    reply = response.choices[0].message.content
    user_context[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)
