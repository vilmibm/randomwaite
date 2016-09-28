# TODO emoji suites
# TODO twitter responding / celery queue
# TODO logging
import multiprocessing
import sys
from io import BytesIO

from flickrapi.core import FlickrAPI

from . import secrets as sec
from .images import generate
from .twitter import post_image
from .tasks import handle_reply

DEBUG_IMAGE_PATH = '/tmp/tarot.jpg'

def main():
    looping = False
    debug = False

    if len(sys.argv) > 1:
        if sys.argv[1] == 'authenticate':
            flickr = FlickrAPI(sec.FLICKR_KEY, sec.FLICKR_SECRET, format='parsed-json')
            print('authenticating...')
            flickr.authenticate_via_browser(perms='read')

        if sys.argv[1] == 'debug':
            print('running in debug mode; no twitter/looping')
            debug = True

        if sys.argv[1] == 'loop':
            looping = True
        else:
            print("'loop' not specified so just running once.")

    if debug:
        im, _ = generate()
        print('saving to', DEBUG_IMAGE_PATH)
        im.save(DEBUG_IMAGE_PATH)
        sys.exit(0)

    im, card = generate()
    print('updating twitter...')
    post_image(card.name, im)

    if not looping:
        sys.exit(0)


    # TODO start 90sec loop to check for replies
    # TODO start 4 hour loop to generate card

