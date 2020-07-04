#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Stɑrry Shivɑm
#
# WallsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Licensed under GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
# Copyright (C) 2007 Free Software Foundation, Inc.
# you may not use this file except in compliance with the License.


START_MSG = """Hello there! my name is <b>{}</b>.
I'm here to give you some cool high definition stock Images.
Click: /help to get list of commands!"""

HELP_MSG = """Here is the list of available commands i can help you with.\n
× /wall <query>: Gives you wallpapers related to you query.
× /wcolor <color>: Filter images by color properties. click: /colors to get list of colors available.
× /editors: Gives you images that have recived Editor's Choice award.
× /random: Gives you randomly choosen wallpapers.
× /anime: Gives you random anime wallpapers.
× /about: To get information about me!"""

WALL_STR = """
× <b>Likes</b>: {}
× <b>Author</b>: {}
× <b>Views</b>: {}
× <b>Downloads</b>: {}
× <b>Tags</b>: {}
"""

COLOR_STR = """Hello {}
here are the list of color filters you can use:
× <code>grayscale</code>, <code>blue</code>.
× <code>transparent</code>, <code>lilac</code>.
× <code>red</code>, <code>pink</code>.
× <code>orange</code>, <code>white</code>.
× <code>yellow</code>, <code>grey</code>.
× <code>green</code>, <code>black</code>.
× <code>turquoise</code>, <code>brown</code>.
"""

ABOUT_STR = """Hello {}
I'm a simple wallpapers bot which
gives you stunning free images & royalty free stock wallpapers from <a href="https://pixabay.com/">pixabay</a> API.

I'm written on Python3 using PTB library by this <a href="tg://user?id=894380120">person</a>.
You can checkout my source code <a href="https://github.com/starry69/WallsBot">here</a> and drop a star if you enjoyed using me!

Feel free to contact my creator if you're having any trouble or found some rough edge inside me :)"""

INVALID_COLOR = """
This seems like invalid color filter,
Click /colors to get list of valid colors!"""

NO_ARGS = "Please enter some keywords!"

NOT_FOUND = "Sorry, couldn't find any matching results for the query!"
