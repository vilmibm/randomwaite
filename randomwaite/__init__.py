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
from PIL import Image, ImageDraw, ImageFont, ImageOps

from . import secrets as sec
from .cards import TarotCard, draw_tarot_card
from .flickr import get_photo


"""
So, for glitching, I read through ImageEnhance, ImageFilter, and ImageOps
modules. There's a bunch of operations and I will use combinations of these,
before and after applying the title (fewer after).

I don't have a solid plan yet for how to actually use all these neat things.
I've tested them all in the repl and they're making sense; it's just time to
start scripting them.

I'd really like to have the glitching (this isn't really glitching frankly but
meh) tied to the meaning of the card / its sentiment but am not sure how
possible this is...

for the pre-title and post-title operations, i would be picking 0-3 operations.
The sentiment related operations all happen pre-title.

generic pre-title operations:
 * blur
 * find edges
 * contour
 * emboss
 * detail
 * invert

negative sentiment:
 1 delete a color band
 2 grayscale
 3 posterize

neutral sentiment:
 1 posterize slightly

positive sentiment:
 1 increase brightness
 2 maxfilter

generic post-title operations:
 * blur
 * edge_enhance
 * edge_enhance_more
 * detail
 * invert

"""


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

def maybe_inverse(card: TarotCard, im: Image) -> Image:
    if not card.inverted:
        return im

    if random() < .7:
        return im.rotate(180)
    else:
        return ImageOps.mirror(im)


def main():
    flickr = FlickrAPI(sec.FLICKR_KEY, sec.FLICKR_SECRET, format='parsed-json')
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    twitter = tweepy.API(twitter_auth)

    if len(sys.argv) > 1 and sys.argv[1] == 'authenticate':
        print('authenticating...')
        flickr.authenticate_via_browser(perms='read')

    card = draw_tarot_card()
    if card.inverted:
        print('drew inverted', card)
    else:
        print('drew', card)

    search_term = card.search_term

    print('searching for', search_term)

    photo = get_photo(flickr, card.search_term)

    print('going to fetch', photo.url)

    original = Image.open(photo.data)

    print('processing image')

    # 1 Pick random section of image to cut card from
    im = random_crop(original)

    # 2 Pick zoom level (possibly 100%)
    im = maybe_zoom(im)

    # 3 modify color balance (based on card)
    im = color_balance(card, im)

    im = place_title(card, im)

    im = maybe_inverse(card, im)

    if not DEBUG:
        print('updating twitter...')
        buffer = BytesIO()
        im.save(buffer, format='JPEG')
        twitter.update_with_media('tarot.jpg', file=buffer)
    else:
        print('saving to /tmp/tarot.jpg')
        im.save('/tmp/tarot.jpg')

    sys.exit(0)
