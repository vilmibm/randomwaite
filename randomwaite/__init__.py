from random import choice
import typing as t
import sys

import flickrapi
from flickrapi.core import FlickrAPI
from .secrets import FLICKR_KEY, FLICKR_SECRET

OK_LICENSES = [1,2,4,5,7]
NO_ATTRIBUTION = [7]

class TarotCard:
    __slots__ = ['name', 'search']
    def __init__(self, name, search) -> None:
        self.name = name
        self.search = search

    def __repr__(self):
        return '<TarotCard: {}>'.format(self.name)

    def __str__(self):
        return self.name

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

CARDS = [
    TarotCard('Death', 'death'),
]

def get_tarot_card() -> TarotCard:
    return choice(CARDS)

def get_photo(flickr: FlickrAPI, search: str) -> Photo:
    result = flickr.photos.search(text=search, license=OK_LICENSES)
    # TODO pull from more than the first page
    photos = result['photos']['photo']
    return Photo(flickr, choice(photos))

def main():
    flickr = flickrapi.FlickrAPI(FLICKR_KEY, FLICKR_SECRET, format='parsed-json')
    if len(sys.argv) > 1 and sys.argv[1] == 'authenticate':
        print('authenticating...')
        flickr.authenticate_via_browser(perms='read')

    search = get_tarot_card().search
    photo = get_photo(flickr, search)
    print('going to fetch {}'.format(photo.url))
    # TODO get photo bits; either read into memory or save to disk. Would
    # prefer the former.

    sys.exit(0)
