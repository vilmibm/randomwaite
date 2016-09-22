# TODO deal with loss of randomness
# TODO reversed/inversed cards
# TODO sentiment analysis of search words
# TODO emoji suites
# TODO twitter responding / celery queue

import math
import re
import sys
import typing as t
from enum import Enum
from io import BytesIO
from os import path
from random import choice, random, randrange

import tweepy
from flickrapi.core import FlickrAPI
from PIL import Image, ImageDraw, ImageFont

from . import secrets as sec
from .cards import TarotCard, CARDS, get_tarot_card
from .flickr import get_photo

DEBUG = True
CARD_WIDTH = 385
CARD_HEIGHT = 666
ZOOM_CHANCE = .25
FONT_PATH = path.join(path.dirname(__file__), 'fonts')
FONTS = ['CantataOne-Regular.ttf']
ROMAN_TABLE = {
    'two': 'ii',
    'three': 'iii',
    'four': 'iv',
    'five': 'v',
    'six': 'vi',
    'seven': 'vii',
    'eight': 'viii',
    'nine': 'ix',
    'ten': 'x',
}
TITLE_ALIGNS = ('left', 'right', 'center')
TITLE_SIZES = {
    'large': 50,
    'small': 32,
    'stupid': 80,
}

Fill = t.Tuple[int]
TitlePlacement = Enum('TitlePlacement', 'top bottom middle random')

break_string_re = re.compile(' ')

def random_fill() -> Fill:
    return (
        randrange(0,255),
        randrange(0,255),
        randrange(0,255),
        randrange(0,255),
    )

def maybe_romanize(text: str) -> str:
    for english,roman in ROMAN_TABLE.items():
        if re.search(english, text, flags=re.I):
            return re.sub(english, roman, text, flags=re.I)
    return text


def random_crop(original: Image) -> Image:
    min_x0 = 0
    max_x0 = original.width - CARD_WIDTH
    min_y0 = 0
    max_y0 = original.height - CARD_HEIGHT

    print('min x0', min_x0)
    print('max x0', max_x0)
    print('min y0', min_y0)
    print('max y0', max_y0)

    x0 = choice(range(min_x0, max_x0))
    y0 = choice(range(min_y0, max_y0))
    x1 = x0 + CARD_WIDTH
    y1 = y0 + CARD_HEIGHT

    print('CROPPING AT {}, {}, {}, {}'.format(x0, y0, x1, y1))

    return original.crop((x0, y0, x1, y1))


def maybe_zoom(original: Image) -> Image:
    zoom_level = 1 + random()
    new_width = math.floor(original.width * zoom_level)
    new_height = math.floor(original.height * zoom_level)

    print('ZOOMING AT', zoom_level)

    resized = original.resize((new_width, new_height))

    return random_crop(resized)

def color_balance(card: TarotCard, original: Image) -> Image:
    # TODO
    return original

def row_shift(original: Image) -> Image:
    # TODO this doesn't work
    row_height = 5
    max_x = original.width
    max_y = original.height
    for y0 in xrange(0, max_y - row_height):
        row_box = (0, max_x, y0, y0 + rpw_height)
        row = original.crop(row_box)
        shifted = row.crop((0, max_x - 10, 0, row.height))
        original.paste(shifted, row_box)


def get_font_path() -> str:
    # TODO perhaps take a card and tie font to card
    return path.join(FONT_PATH, choice(FONTS))


def place_title(card: TarotCard, im: Image) -> Image:
    # boilerplate
    title = card.name
    position = choice(list(TitlePlacement))
    size = choice(list(TITLE_SIZES.keys()))
    align = choice(TITLE_ALIGNS)
    im = im.convert('RGBA')
    font_path = get_font_path()
    fnt = ImageFont.truetype(font_path, TITLE_SIZES[size])
    txt = Image.new('RGBA', im.size, (0,0,0,0))
    d = ImageDraw.Draw(txt)
    print(title)
    print(position)
    print(size)
    print(align)

    # ~ * randomness * ~
    if random() < .5:
        title = maybe_romanize(title)

    if random() < .6:
        title = title.lower()

    # check to see if we'd go out of bounds and split text if so
    if d.textsize(title, fnt)[0] > im.width:
        title = break_string_re.sub('\n', title)

    text_w, text_h = d.textsize(title, fnt)

    text_x = 0
    if text_w < im.width:
        text_x += randrange(0, im.width - text_w)

    if position == TitlePlacement.top:
        text_y = 0
    elif position == TitlePlacement.middle:
        text_y = im.height // 2
        if text_y + text_h > im.height:
            position = TitlePlacement.bottom
    elif position == TitlePlacement.bottom:
        text_y = im.height - text_h
    elif position == TitlePlacement.random:
        text_y = randrange(0, (im.height - text_h))

    print(text_x, text_y, text_w, text_h)

    # actual drawing
    d.rectangle((text_x, text_y, text_x+text_w, text_y+text_h+15), fill=random_fill())
    d.text((text_x, text_y),
           title,
           font=fnt,
           fill=random_fill(),
           spacing=1,
           align=align)

    out = Image.alpha_composite(im, txt)

    return out


def main():
    flickr = FlickrAPI(sec.FLICKR_KEY, sec.FLICKR_SECRET, format='parsed-json')
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    twitter = tweepy.API(twitter_auth)

    if len(sys.argv) > 1 and sys.argv[1] == 'authenticate':
        print('authenticating...')
        flickr.authenticate_via_browser(perms='read')

    card = get_tarot_card()
    photo = get_photo(flickr, card.search_term)

    print('going to fetch {}'.format(photo.url))

    original = Image.open(photo.data)

    # 1 Pick random section of image to cut card from
    im = random_crop(original)

    # 2 Pick zoom level (possibly 100%)
    im = maybe_zoom(im)

    # 3 modify color balance (based on card)
    im = color_balance(card, im)

    im = place_title(card, im)

    if not DEBUG:
        buffer = BytesIO()
        im.save(buffer, format='JPEG')
        twitter.update_with_media('tarot.jpg', file=buffer)
    else:
        im.save('/tmp/tarot.jpg')

    sys.exit(0)
