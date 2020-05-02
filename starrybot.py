from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import os


# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# Currently only webhook mode is supported.

TOKEN = os.environ.get('TOKEN')
URL = os.environ.get('URL')
PORT = int(os.environ.get('PORT'))

updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher


LOGGER.info("Starting WALLSBOT | Using webhook...")
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)

updater.bot.set_webhook(url=URL + TOKEN)
updater.idle()


def start(update, context):
    update.effective_message.reply_text("Hello!")
    LOGGER.info("lmao")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

