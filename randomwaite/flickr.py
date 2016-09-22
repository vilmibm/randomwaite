from io import BytesIO
from random import choice
import typing as t
import urllib.request

from flickrapi.core import FlickrAPI

OK_LICENSES = [1,2,4,5,7]
NO_ATTRIBUTION = [7]

class Photo:

    def __init__(self, flickr: FlickrAPI, flickr_data: t.Dict) -> None:
        self.path = None
        self._img_data = None
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

    @property
    def data(self) -> BytesIO:  # TODO I don't think this return type is right
        if not self._img_data:
            self._img_data = urllib.request.urlopen(self.url)

        return self._img_data


def get_photo(flickr: FlickrAPI, search_term: str) -> Photo:
    # This will check title, description, and tags for the given word
    result = flickr.photos.search(text=search_term, license=OK_LICENSES)

    # TODO pull from more than the first page
    photos = result['photos']['photo']
    return Photo(flickr, choice(photos))
