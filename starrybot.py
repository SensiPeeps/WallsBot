# Copyright (C) - 2020 Starry69 // @starryboi
#
# This file is part of WallsBot
#
# WallsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Licensed under GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
# Copyright (C) 2007 Free Software Foundation, Inc.
# you may not use this file except in compliance with the License.


from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import os


# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)

# Currently only webhook mode is supported.

TOKEN = os.environ.get('TOKEN')
URL = os.environ.get('URL')
PORT = int(os.environ.get('PORT'))
PIX_API = os.environ.get('PIX_API', None)

updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    update.effective_message.reply_text("Hello!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

LOGGER.info("Starting WALLSBOT | Using webhook...")
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)

updater.bot.set_webhook(url=URL + TOKEN)
updater.idle()
