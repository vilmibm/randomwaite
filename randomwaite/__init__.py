# TODO emoji suites
# TODO twitter responding / celery queue
# TODO logging
import re
import sys
from io import BytesIO
from multiprocessing import Process
from time import sleep

from flickrapi.core import FlickrAPI
from redis import Redis

from . import secrets as sec
from . import twitter
from .images import generate
from .tasks import handle_reply
from .cards import draw_tarot_card

DEBUG_IMAGE_PATH = '/tmp/tarot.jpg'
MENTION_CHECK_INTERVAL = 90 # seconds
GENERATION_INTERVAL = 60 * 60 * 4 # seconds
SINCE_KEY = 'tarot_mentions_since_id'
RESPOND_TEXT = 'draw me a card'

should_respond_re = re.compile(RESPOND_TEXT)

def should_respond(text: str) -> bool:
    return should_respond_re.search(text)

def mention_loop() -> None:
    print('starting mentions listener...')
    redis = Redis()
    twitter_client = twitter.get_client()

    while True:
        since_id = redis.get(SINCE_KEY)
        mentions = twitter.get_mentions(twitter_client, since_id)
        if len(mentions) > 0:
            print('found some mentions')
        else:
            print('found no mentions')

        for mention in mentions:
            if not should_respond(mention.text):
                print('found mention but it is not for responding to')
                continue
            username = mention.author.screen_name
            status_id = mention.id_str
            handle_reply.delay(status_id, username)

        if len(mentions) > 0 and mentions[0].id_str != since_id:
            print('updated since_id in redis')
            redis.set(SINCE_KEY, mentions[0].id_str)

        print('done, sleeping...')
        sleep(MENTION_CHECK_INTERVAL)

def post_loop() -> None:
    pass

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

    card = draw_tarot_card()
    if debug:
        im = generate(card)
        print('saving to', DEBUG_IMAGE_PATH)
        im.save(DEBUG_IMAGE_PATH)
        sys.exit(0)


    if not looping:
        im = generate(card)
        twitter_client = twitter.get_client()
        print('updating twitter...')
        twitter.post_image(twitter_client, card.name, im)
        sys.exit(0)

    replies_loop = Process(target=mention_loop)
    replies_loop.start()

    # TODO start 4 hour loop to generate card

    replies_loop.join()

