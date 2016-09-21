from io import BytesIO
import math
from random import choice, random
import sys
import typing as t
import urllib.request

import flickrapi
from flickrapi.core import FlickrAPI
from PIL import Image
import tweepy

from . import secrets as sec
from .cards import TarotCard, CARDS, get_tarot_card

OK_LICENSES = [1,2,4,5,7]
NO_ATTRIBUTION = [7]
CARD_WIDTH = 385
CARD_HEIGHT = 666
ZOOM_CHANCE = .25

class Photo:
    __slots__ = ['_url', 'path', '_license', '_data', 'flickr']

    def __init__(self, flickr: FlickrAPI, flickr_data: t.Dict) -> None:
        self.path = None
        self._license = None
        self._url = None
        self._data = flickr_data
        self.flickr = flickr

    def needs_attribution(self) -> bool:
        return self.license in NO_ATTRIBUTION

    @property
    def license(self) -> int:
        if not self._license:
            info = self.flickr.photos.getInfo(photo_id=self._data['id'], secret=self._data['secret'])
            self._license = info['photo']['license']
        return self._license

    @property
    def url(self) -> str:
        if not self._url:
            sizes = self.flickr.photos.getSizes(photo_id=self._data['id'])
            self._url = sizes['sizes']['size'][-1]['source']
        return self._url

    @property
    def attribution(self) -> str:
        return "TODO"

def get_photo(flickr: FlickrAPI, search: str) -> Photo:
    result = flickr.photos.search(text=search, license=OK_LICENSES)
    # TODO pull from more than the first page
    photos = result['photos']['photo']
    return Photo(flickr, choice(photos))

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
    row_height = 5
    max_x = original.width
    max_y = original.height
    for y0 in xrange(0, max_y - row_height):
        row_box = (0, max_x, y0, y0 + rpw_height)
        row = original.crop(row_box)
        shifted = row.crop((0, max_x - 10, 0, row.height))
        original.paste(shifted, row_box)



def main():
    flickr = flickrapi.FlickrAPI(sec.FLICKR_KEY, sec.FLICKR_SECRET, format='parsed-json')
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    twitter = tweepy.API(twitter_auth)

    if len(sys.argv) > 1 and sys.argv[1] == 'authenticate':
        print('authenticating...')
        flickr.authenticate_via_browser(perms='read')

    card = get_tarot_card()
    photo = get_photo(flickr, card.search)
    test_url = 'https://farm6.staticflickr.com/5533/11031461323_e59917dd84_o.jpg'

    print('going to fetch {}'.format(photo.url))

    # move into Photo
    request = urllib.request.urlopen(photo.url)
    #request = urllib.request.urlopen(test_url)
    original = Image.open(request)

    # 1 Pick random section of image to cut card from
    im = random_crop(original)

    # 2 Pick zoom level (possibly 100%)
    im = maybe_zoom(im)

    # 3 modify color balance (based on card)
    im = color_balance(card, im)

    buffer = BytesIO()
    im.save(buffer, format='JPEG')
    twitter.update_with_media('tarot.jpg', file=buffer)


    # TODO no network
    #im.save('there.jpg')

    # 4 potentially emoji bomb, if the card supports it
    # 5 glitch step (might not happen)
    # 6 text application
      # 6a choose font (card based or random?)
      # 6b choose size / placement / color of number
      # 6c choose size / placement / color of text
    # 7 glitch step (will always happen)

    sys.exit(0)
