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

import logging
import os
import requests
import random
import strings as str

from telegram.ext import(
Updater, CommandHandler,
run_async, Filters, Defaults)

from telegram import(
ChatAction, ParseMode,
InlineKeyboardButton,
InlineKeyboardMarkup)

from telegram.error import BadRequest
from telegram.utils.helpers import mention_html

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

@run_async
@send_action(ChatAction.TYPING)
def start(update, context):
    update.effective_message.reply_text(
    str.START_MSG.format(context.bot.first_name))

@run_async
@send_action(ChatAction.TYPING)
def helper(update, context):
    update.effective_message.reply_text(
    str.HELP_MSG, parse_mode=None)

# Log Errors caused by Updates

def error(update, context):
    try:
        raise context.error
    finally:
        LOGGER.warning('Update "%s" caused error "%s"', update, context.error)

# WALL FUNCTIONS

BASE_URL = 'https://pixabay.com/api/'
AUTH_URL = 'https://pixabay.com/users'

@run_async
@send_action(ChatAction.UPLOAD_PHOTO)
def wall(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    args = context.args
    query = " ".join(args).lower()

    if not query:
       msg.reply_text(str.NO_ARGS)
       return
    query = query.replace(" ", "+")
    contents = requests.get(
               f"{BASE_URL}?key={PIX_API}&q={query}&page=1&per_page=200"
               ).json()

    hits = contents.get('hits')
    if not hits:
       msg.reply_text(str.NOT_FOUND)
       return
    else:
       pickrandom = random.choice(list(hits)) # Random hits
       hits = pickrandom
       preview = hits.get('largeImageURL')
       views = hits.get('views')
       downloads = hits.get('downloads')
       likes = hits.get('likes')
       author = hits.get('user')
       authid = hits.get('user_id')
       tags = hits.get('tags')
       imgurl = hits.get('pageURL')
       document = hits.get('imageURL')

       keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'{AUTH_URL}/{author}-{authid}')
                  ]]

    try:
       context.bot.send_photo(chat.id, photo=preview,
            caption=(str.WALL_STR.format(
            likes, author, views, downloads, tags)),
            reply_markup=InlineKeyboardMarkup(keyboard),
            timeout=60)

       context.bot.send_document(chat.id,
               document=document,
               timeout=100)
    except BadRequest as excp:
            msg.reply_text(f"Error! {excp.message}")



VALID_COLORS = (
"grayscale", "transparent",
"red", "orange", "yellow","green",
"turquoise", "blue", "lilac",
"pink", "white", "gray", "black", "brown"
)


@run_async
@send_action(ChatAction.UPLOAD_PHOTO)
def wallcolor(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    args = context.args
    color = " ".join(args).lower()

    if not color:
       msg.reply_text(str.NO_ARGS)
       return
    if color not in VALID_COLORS:
       msg.reply_text(str.INVALID_COLOR)
       return

    contents = requests.get(
               f"{BASE_URL}?key={PIX_API}&colors={color}&page=2&per_page=200"
               ).json()

    hits = contents.get('hits')
    if not hits: # should never happen since these colors are in supported list by API
       msg.reply_text(str.NOT_FOUND)
       return
    else:
       pickrandom = random.choice(list(hits)) # Random hits
       hits = pickrandom
       preview = hits.get('largeImageURL')
       views = hits.get('views')
       downloads = hits.get('downloads')
       likes = hits.get('likes')
       author = hits.get('user')
       authid = hits.get('user_id')
       tags = hits.get('tags')
       imgurl = hits.get('pageURL')
       document = hits.get('imageURL')

       keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'{AUTH_URL}/{author}-{authid}')
                  ]]

    try:
       context.bot.send_photo(chat.id, photo=preview,
       caption=(str.WALL_STR.format(
       likes, author, views, downloads, tags)),
       reply_markup=InlineKeyboardMarkup(keyboard),
       timeout=60)

       context.bot.send_document(chat.id,
                document=document,
                timeout=100)
    except BadRequest as excp:
       msg.reply_text(f"Error! {excp.message}")


@run_async
@send_action(ChatAction.UPLOAD_PHOTO)
def editorschoice(update, context):
    msg = update.effective_message
    chat = update.effective_chat

    contents = requests.get(
               f"{BASE_URL}?key={PIX_API}&editors_choice=true&page=2&per_page=200"
               ).json()

    hits = contents.get('hits')
    pickrandom = random.choice(list(hits)) # Random hits
    hits = pickrandom
    preview = hits.get('largeImageURL')
    views = hits.get('views')
    downloads = hits.get('downloads')
    likes = hits.get('likes')
    author = hits.get('user')
    authid = hits.get('user_id')
    tags = hits.get('tags')
    imgurl = hits.get('pageURL')
    document = hits.get('imageURL')

    keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'{AUTH_URL}/users/{author}-{authid}')
                  ]]

    try:
       context.bot.send_photo(chat.id, photo=preview,
       caption=(str.WALL_STR.format(
       likes, author, views, downloads, tags)),
       reply_markup=InlineKeyboardMarkup(keyboard),
       timeout=60)

       context.bot.send_document(chat.id,
               document=document,
               timeout=100)
    except BadRequest as excp:
       msg.reply_text(f"Error! {excp.message}")



@run_async
@send_action(ChatAction.UPLOAD_PHOTO)
def randomwalls(update, context):
    msg = update.effective_message
    chat = update.effective_chat

    contents = requests.get(
               f"{BASE_URL}?key={PIX_API}&page=2&per_page=200"
               ).json()

    hits = contents.get('hits')
    pickrandom = random.choice(list(hits)) # Random hits
    hits = pickrandom
    preview = hits.get('largeImageURL')
    views = hits.get('views')
    downloads = hits.get('downloads')
    likes = hits.get('likes')
    author = hits.get('user')
    authid = hits.get('user_id')
    tags = hits.get('tags')
    imgurl = hits.get('pageURL')
    document = hits.get('imageURL')

    keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'{AUTH_URL}/{author}-{authid}')
                  ]]

    try:
       context.bot.send_photo(chat.id, photo=preview,
       caption=(str.WALL_STR.format(
       likes, author, views, downloads, tags)),
       reply_markup=InlineKeyboardMarkup(keyboard),
       timeout=60)

       context.bot.send_document(chat.id,
               document=document,
               timeout=100)
    except BadRequest as excp:
       msg.reply_text(f"Error! {excp.message}")


@run_async
@send_action(ChatAction.TYPING)
def colors(update, context):
    update.effective_message.reply_text(
    str.COLOR_STR.format(mention_html(
    update.effective_user.id,
    update.effective_user.full_name)))


@run_async
@send_action(ChatAction.TYPING)
def about(update, context):
    update.effective_message.reply_text(
    str.ABOUT_STR.format(mention_html(
    update.effective_user.id,
    update.effective_user.full_name)))

@run_async
@send_action(ChatAction.TYPING)
def api_status(update, context):
    msg = update.effective_message
    r = requests.get(
        f"{BASE_URL}?key={PIX_API}")
    if r.status_code == 200:
       status = 'functional'
    elif r.status_code == 429:
       status = 'limit exceeded!'
    else:
       status = f'Error! {r.status_code}'

    try:
       ratelimit = r.headers['X-RateLimit-Limit']
       remaining = r.headers['X-RateLimit-Remaining']

       text = f"API status: <code>{status}</code>\n"
       text += f"Requests limit: <code>{ratelimit}</code>\n"
       text += f"Requests remaining: <code>{remaining}</code>"

       msg.reply_text(text)

    except Exception:
         msg.reply_text(f"API status: {status}")


# HANDLERS
def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(TOKEN, use_context=True, defaults=defaults)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', helper)
    wall_handler = CommandHandler(["wall", "wallpaper"], wall)
    wcolor_handler = CommandHandler('wcolor', wallcolor)
    random_handler = CommandHandler('random', randomwalls)
    editors_handler = CommandHandler('editors', editorschoice)
    colors_handler = CommandHandler('colors', colors)
    about_handler = CommandHandler('about', about)
    apistatus_handler = CommandHandler('status', api_status, filters=Filters.user(894380120))

# Register handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(wall_handler)
    dispatcher.add_handler(wcolor_handler)
    dispatcher.add_handler(editors_handler)
    dispatcher.add_handler(random_handler)
    dispatcher.add_handler(colors_handler)
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(apistatus_handler)
    dispatcher.add_error_handler(error)

# BOT ENGINE
    if WEBHOOK:
          LOGGER.info("Starting WallsBot // Using webhooks...")
          updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)

          updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Starting WallsBot // Using long polling...")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()

if __name__ == '__main__':
   main()
