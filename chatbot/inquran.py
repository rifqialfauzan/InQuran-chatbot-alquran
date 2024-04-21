from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from botResponse import bot_response
from dataLoad import list_surah, greeting_msg
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../config.env")

token = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=greeting_msg)


async def helpMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=greeting_msg)


async def listSurah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_surat = "NAMA SURAT DALAM AL-QUR'AN \n\n"
    for i in range(114):
        list_surat += f"{i + 1}. {list_surah[i]} \n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=list_surat)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    rsp = bot_response(msg)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=rsp)


if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    listsurah_handler = CommandHandler("listsurah", listSurah)
    application.add_handler(listsurah_handler)

    help_handler = CommandHandler("help", helpMsg)
    application.add_handler(help_handler)

    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)
    application.add_handler(message_handler)

    application.run_polling()
