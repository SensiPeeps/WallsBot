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
from telegram.ext import CommandHandler, run_async
import logging
import os

from telegram import (Message,
                      Chat,
                      Update,
                      Bot,
                      User,
                      ChatAction,
                      ParseMode)

from telegram.error import BadRequest
from functools import wraps

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

ENV = bool(os.environ.get('ENV', False))

if ENV:
       TOKEN = os.environ.get('TOKEN')
       URL = os.environ.get('URL')
       PORT = int(os.environ.get('PORT'))
       WEBHOOK = bool(os.environ.get('WEBHOOK', False))
       PIX_API = os.environ.get('PIX_API', None)
else:
      from config import TOKEN, PIX_API, WEBHOOK


updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher

##########################################

def typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

START_MSG = f"""Heya my name is <b>{dispatcher.bot.first_name}</b>.
            \nI'm here to give you some cool high definition wallpapers.
            \nClick: /help to get list of commands!"""

HELP_MSG = """Help the helper"""

@run_async
@typing_action
def help(update, context):
    update.effective_message.reply_text(HELP_MSG, parse_mode=ParseMode.HTML)

@run_async
@typing_action
def start(update, context):
    update.effective_message.reply_text(START_MSG, parse_mode=ParseMode.HTML)

# Log Errors caused by Updates

def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_error_handler(error)

##########################################
if WEBHOOK:
          LOGGER.info("Starting WallpaperRobot | Using webhook...")
          updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)

          updater.bot.set_webhook(url=URL + TOKEN)

else:
     LOGGER.info("Starting WAallpaperRobot | Using long polling...")
     updater.start_polling(timeout=15, read_latency=4)

updater.idle()
