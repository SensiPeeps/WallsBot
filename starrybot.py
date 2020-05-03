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
                      ParseMode,
                      InlineKeyboardButton)

from telegram.error import BadRequest
from functools import wraps
import requests
from random import randint

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

################ START & HELPER FUCS ##############

# Good bots should send actions.
def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func

    return decorator

#==============================#

START_MSG = f"""Hello there! my name is <b>{dispatcher.bot.first_name}</b>.
I'm here to give you some cool high definition wallpapers.
\nClick: /help to get list of commands!"""

HELP_MSG = """
Here are the list of available commands i can help you with.\n
× /wall <query>: Gives you wallpapers related to you query.
× /wcolor <color>: Filter images by color properties. click: /colors to get list of colors available.
× /editors: Gives you images that have recived Editor's Choice award.
× /random: Gives you randomly choosen wallpapers.
× /about: To get information about bot!"""

@run_async
@send_action(ChatAction.TYPING)
def help(update, context):
    update.effective_message.reply_text(HELP_MSG)

@run_async
@send_action(ChatAction.TYPING)
def start(update, context):
    update.effective_message.reply_text(START_MSG, parse_mode=ParseMode.HTML)

# Log Errors caused by Updates

def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)

############ WALL FUNCTIONS #############

@run_async
@send_action(ChatAction.UPLOAD_PHOTO)
def wall(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    args = context.args
    query = " ".join(args)

    if not query:
       msg.reply_text("Please enter some keywords!")
       return
    query = query.replace(" ", "+")
    contents = requests.get(f"https://pixabay.com/api/?key={PIX_API}&q={query}").json()
    hits = contents.get('hits')
    if not contents.get('hits'):
       msg.reply_text("Couldn't find any matching results for the query!")
       return
    else:
       index = randint(0, len(hits)-1) # Random hits
       hits = hits[index]
       preview = hits.get('webformatURL')

       context.bot.send_photo(chat.id, photo=preview)


############### HANDLERS #################
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
wall_handler = CommandHandler(["wall", "wallpaper"], wall)

# Register handlers to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(wall_handler)
dispatcher.add_error_handler(error)

############### BOT ENGINE ################
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
