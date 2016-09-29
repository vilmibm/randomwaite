import logging
import math
import re
import typing as t
from enum import Enum
from functools import partial
from os import path
from random import choice, random, randrange, randint
from time import sleep

from flickrapi.core import FlickrAPI
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
from pixelsorter.sort import sort_image

from . import secrets as sec
from .cards import TarotCard, draw_tarot_card
from .flickr import get_photo
from .sentiment import POSITIVE, NEGATIVE
from .errors import TinyImageException
from .logs import get_logger

logger = get_logger()

R = 0
G = 1
B = 2
CARD_WIDTH = 385
CARD_HEIGHT = 666
ZOOM_CHANCE = .25
FONT_PATH = path.join(path.dirname(__file__), 'fonts')
# repeats == increased likelihood
FONTS = [
    'alegreya.ttf',
    'antic_didone.ttf',
    'cinzel.ttf',
    'juliussans.ttf',
    'oswald.ttf',
    'vcr.ttf',
    'vcr.ttf',
    'amatica.ttf',
    'bree.ttf',
    'vcr.ttf',
    'cormorant_infant.ttf',
    'imfell.ttf',
    'lobster.ttf',
    'vcr.ttf',
    'palanquin.ttf',
    'vt323.ttf',
    'vcr.ttf',
    'amethysta.ttf',
    'cantata.ttf',
    'cutive.ttf',
    'imfell.ttf',
    'jacques.ttf',
    'nothing.ttf',
    'tangerine.ttf',
]

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

TitlePlacement = Enum('TitlePlacement', 'top bottom middle random')

break_string_re = re.compile(' ')

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

    if max_y0 <= 0 or max_x0 <= 0:
        raise TinyImageException()

    x0 = choice(range(min_x0, max_x0))
    y0 = choice(range(min_y0, max_y0))
    x1 = x0 + CARD_WIDTH
    y1 = y0 + CARD_HEIGHT

    logger.debug('CROPPING AT {}, {}, {}, {}'.format(x0, y0, x1, y1))

    return original.crop((x0, y0, x1, y1))


def maybe_zoom(original: Image) -> Image:
    zoom_level = 1 + random()
    new_width = math.floor(original.width * zoom_level)
    new_height = math.floor(original.height * zoom_level)

    logger.debug('ZOOMING AT %s', zoom_level)

    resized = original.resize((new_width, new_height))

    return random_crop(resized)


def color_balance(card: TarotCard, original: Image) -> Image:
    # TODO
    return original

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
    logger.debug('USING FONT %s', font_path)
    fnt = ImageFont.truetype(font_path, TITLE_SIZES[size])
    txt = Image.new('RGBA', im.size, (0,0,0,0))
    d = ImageDraw.Draw(txt)
    logger.debug('title: %s, position: %s, size: %s, align: %s', title, position, size, align)

    # ~ * randomness * ~
    if random() < .5:
        title = maybe_romanize(title)

    if random() < .6:
        if random() < .5:
            title = title.lower()
        else:
            title = title.upper()

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

    # actual drawing
    d.rectangle((0, text_y, im.width, text_y+text_h+15), fill=(0,0,0,255))
    d.text((text_x, text_y),
           title,
           font=fnt,
           fill=(255,255,255,255),
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

def sort_pixels(max_interval:int, im: Image) -> Image:
    # TODO random angle, or at least diagonal chance
    pixels = list(im.getdata())
    outpixels = sort_image(pixels, im.size, max_interval=max_interval, randomize=True)
    output = Image.new(im.mode, im.size)
    output.putdata(outpixels)
    return output

def blur(im: Image) -> Image:
    return im.filter(ImageFilter.BLUR)

def find_edges(im: Image) -> Image:
    return im.filter(ImageFilter.FIND_EDGES)

def contour(im: Image) -> Image:
    return im.filter(ImageFilter.CONTOUR)

def emboss(im: Image) -> Image:
    return im.filter(ImageFilter.EMBOSS)

def detail(im: Image) -> Image:
    return im.filter(ImageFilter.DETAIL)

def invert(im: Image) -> Image:
    return ImageOps.invert(im)

def edge_enhance(im: Image) -> Image:
    return im.filter(ImageFilter.EDGE_ENHANCE)

def edge_enhance_more(im: Image) -> Image:
    return im.filter(ImageFilter.EDGE_ENHANCE_MORE)

def grayscale(im: Image) -> Image:
    return ImageOps.grayscale(im)

def posterize(bits: int, im: Image) -> Image:
    return ImageOps.posterize(im, bits)

def brighten(im: Image) -> Image:
    enbrightener = ImageEnhance.Brightness(im)
    return enbrightener.enhance(1.4)

PRE_TITLE_DISTORT = [
    blur,
    partial(sort_pixels, 15),
    find_edges,
    contour,
    emboss,
    detail,
    invert,
]

POST_TITLE_DISTORT = [
    blur,
    edge_enhance,
    detail,
    invert,
    partial(sort_pixels, 5),
]

def process_sentiment(card: TarotCard, im: Image) -> Image:
    """To be called prior to title placement."""
    logger.debug('PROCESSING A {} SENTIMENT'.format(card.sentiment))
    if card.sentiment == NEGATIVE:
        # first, replace a color band with black
        bands = im.split()
        bye_band = choice([0,1,2])
        black_band = bands[bye_band].point(lambda _: 0)
        bands[bye_band].paste(black_band)
        im = Image.merge(im.mode, bands)

        return posterize(4, grayscale(im))
    elif card.sentiment == POSITIVE:
        return brighten(im)
    else:
        return posterize(7, im)

# TODO pass in drawn card, then only return image
def _generate(card:TarotCard) -> Image:
    flickr = FlickrAPI(sec.FLICKR_KEY, sec.FLICKR_SECRET, format='parsed-json')

    if card.inverted:
        logger.debug('drew inverted %s', card)
    else:
        logger.debug('drew %s', card)

    search_term = card.search_term

    logger.debug('searching for %s', search_term)

    photo = get_photo(flickr, card.search_term)

    logger.debug('going to fetch %s', photo.url)

    original = Image.open(photo.data)

    logger.debug('processing image')

    # 1 Pick random section of image to cut card from
    im = random_crop(original)

    # 2 Pick zoom level (possibly 100%)
    im = maybe_zoom(im)

    # 3 modify color balance (based on card)
    im = color_balance(card, im)

    im = process_sentiment(card, im)

    pre_distort = choice(PRE_TITLE_DISTORT)
    logger.debug('PRE-TITLE DISTORTING %s %s', im, pre_distort)
    im = im.convert('RGB')
    im = pre_distort(im)

    logger.debug('PLACING TITLE')
    im = place_title(card, im)

    im = maybe_inverse(card, im)

    first_post_distort = choice(POST_TITLE_DISTORT)
    second_post_distort = choice(POST_TITLE_DISTORT)
    while second_post_distort == first_post_distort:
        second_post_distort = choice(POST_TITLE_DISTORT)
    logger.debug('POST-TITLE DISTORTING %s %s %s',
                 im,
                 first_post_distort,
                 second_post_distort)
    im = im.convert('RGB')
    im = first_post_distort(im)
    im = im.convert('RGB')
    im = second_post_distort(im)

    return im

def generate(card:TarotCard) -> Image:
    im = None
    while im == None:
        try:
            im = _generate(card)
        except TinyImageException:
            logger.error('ignoring bad image')
            sleep(1)
        except Exception as e:
            logger.critical('whoa there bud: %s', e)
            sleep(10)
    return im
