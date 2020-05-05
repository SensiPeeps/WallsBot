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

from telegram.ext import(
Updater, CommandHandler,
run_async, Filters)

from telegram import(
Chat, Update,
Bot, ChatAction,
ParseMode, InlineKeyboardButton,
InlineKeyboardMarkup)

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
def helper(update, context):
    update.effective_message.reply_text(HELP_MSG)

@run_async
@send_action(ChatAction.TYPING)
def start(update, context):
    update.effective_message.reply_text(START_MSG, parse_mode=ParseMode.HTML)

# Log Errors caused by Updates

def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)

# WALL FUNCTIONS

BASE_URL = 'https://pixabay.com/api/'

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
    contents = requests.get(
               f"{BASE_URL}?key={PIX_API}&q={query}&page=1&per_page=200"
               ).json()

    hits = contents.get('hits')
    if not hits:
       msg.reply_text("Couldn't find any matching results for the query!")
       return
    else:
       pickrandom = random.choice(list(hits)) # Random hits
       hits = pickrandom
       preview = hits.get('webformatURL')
       views = hits.get('views')
       downloads = hits.get('downloads')
       likes = hits.get('likes')
       author = hits.get('user')
       authid = hits.get('user_id')
       tags = hits.get('tags')
       imgurl = hits.get('pageURL')
       document = hits.get('largeImageURL')

       keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'https://pixabay.com/users/{author}-{authid}')
                  ]]


       WALL_STR = f"""
× <b>Likes</b>: {likes}
× <b>Author</b>: {author}
× <b>Views</b>: {views}
× <b>Downloads</b>: {downloads}
× <b>Tags</b>: {tags}
"""

    try:
       context.bot.send_photo(chat.id, photo=preview,
            caption=(WALL_STR),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML,
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
    color = " ".join(args)

    if not color:
       msg.reply_text("Please enter some keywords to get walls based on color properties.")
       return
    if color not in VALID_COLORS:
       msg.reply_text(
           "This seems like invalid color filter, Click /colors to get list of valid colors!"
               )
       return

    contents = requests.get(
               f"{BASE_URL}?key={PIX_API}&colors={color}&page=2&per_page=200"
               ).json()

    hits = contents.get('hits')
    if not hits: # should never happen since these colors are in supported list by API
       msg.reply_text("Couldn't find any matching results")
       return
    else:
       pickrandom = random.choice(list(hits)) # Random hits
       hits = pickrandom
       preview = hits.get('webformatURL')
       views = hits.get('views')
       downloads = hits.get('downloads')
       likes = hits.get('likes')
       author = hits.get('user')
       authid = hits.get('user_id')
       tags = hits.get('tags')
       imgurl = hits.get('pageURL')
       document = hits.get('largeImageURL')

       keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'https://pixabay.com/users/{author}-{authid}')
                  ]]

       WCOLOR_STR = f"""
× <b>Likes</b>: {likes}
× <b>Author</b>: {author}
× <b>Views</b>: {views}
× <b>Downloads</b>: {downloads}
× <b>Tags</b>: {tags}
"""

    try:
       context.bot.send_photo(chat.id, photo=preview,
       caption=(WCOLOR_STR),
       reply_markup=InlineKeyboardMarkup(keyboard),
       parse_mode=ParseMode.HTML,
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
    preview = hits.get('webformatURL')
    views = hits.get('views')
    downloads = hits.get('downloads')
    likes = hits.get('likes')
    author = hits.get('user')
    authid = hits.get('user_id')
    tags = hits.get('tags')
    imgurl = hits.get('pageURL')
    document = hits.get('largeImageURL')

    keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'https://pixabay.com/users/{author}-{authid}')
                  ]]

    EDITOR_STR = f"""
× <b>Likes</b>: {likes}
× <b>Author</b>: {author}
× <b>Views</b>: {views}
× <b>Downloads</b>: {downloads}
× <b>Tags</b>: {tags}
"""
    try:
       context.bot.send_photo(chat.id, photo=preview,
       caption=(EDITOR_STR),
       reply_markup=InlineKeyboardMarkup(keyboard),
       parse_mode=ParseMode.HTML,
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
    preview = hits.get('webformatURL')
    views = hits.get('views')
    downloads = hits.get('downloads')
    likes = hits.get('likes')
    author = hits.get('user')
    authid = hits.get('user_id')
    tags = hits.get('tags')
    imgurl = hits.get('pageURL')
    document = hits.get('largeImageURL')

    keyboard = [[
       InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
       InlineKeyboardButton(text="Author 👸",
            url=f'https://pixabay.com/users/{author}-{authid}')
                  ]]

    RANDOM_STR = f"""
× <b>Likes</b>: {likes}
× <b>Author</b>: {author}
× <b>Views</b>: {views}
× <b>Downloads</b>: {downloads}
× <b>Tags</b>: {tags}
"""
    try:
       context.bot.send_photo(chat.id, photo=preview,
       caption=(RANDOM_STR),
       reply_markup=InlineKeyboardMarkup(keyboard),
       parse_mode=ParseMode.HTML,
       timeout=60)

       context.bot.send_document(chat.id,
               document=document,
               timeout=100)
    except BadRequest as excp:
       msg.reply_text(f"Error! {excp.message}")


@run_async
@send_action(ChatAction.TYPING)
def colors(update, context):
    user = update.effective_user

    COLOR_STR = f"""
Hello {user.first_name}!
here are the list of color filters you can use:
× <code>grayscale</code>, <code>blue</code>.
× <code>transparent</code>, <code>lilac</code>.
× <code>red</code>, <code>pink</code>.
× <code>orange</code>, <code>white</code>.
× <code>yellow</code>, <code>grey</code>.
× <code>green</code>, <code>black</code>.
× <code>turquoise</code>, <code>brown</code>.
"""
    update.effective_message.reply_text(
           COLOR_STR,
           parse_mode=ParseMode.HTML)


@run_async
@send_action(ChatAction.TYPING)
def about(update, context):
    user = update.effective_user
    chat = update.effective_chat
    ABOUT_STR = f"""
Hello <b>{user.first_name}</b>!
I'm a simple wallpapers bot which
gives you stunning free images & royalty free stock wallpapers from <a href="https://pixabay.com/">pixabay</a>.

I'm written on Python3 using PTB library by this <a href="tg://user?id=894380120">person</a>.
Contact him if you're having any trouble using me!
"""
    context.bot.sendMessage(chat.id, ABOUT_STR,
                parse_mode=ParseMode.HTML)

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

       msg.reply_text(text,
              parse_mode=ParseMode.HTML)

    except:
         msg.reply_text(f"API status: {status}")



# HANDLERS
def main():
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
