# TODO emoji suites
import logging
import re
import sys
from io import BytesIO
from logging.handlers import RotatingFileHandler
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
MENTION_CHECK_INTERVAL = 70 # seconds
GENERATION_INTERVAL = 60 * 60 * 4 # seconds
SINCE_KEY = 'tarot_mentions_since_id'
RESPOND_TEXT = 'draw me a card'

should_respond_re = re.compile(RESPOND_TEXT)

LOG_FILE = '/tmp/randomwaite.log'
MENTIONS_LOG_FILE = '/tmp/randomwaite.mentions.log'
GENERATION_LOG_FILE = '/tmp/randomwaite.generation.log'
LOG_MAXSIZE = 1000 * 2 # 2 mb
LOG_BACKUP_COUNT = 5

logger = logging.getLogger('randomwaite')

def init_logger(logger: logging.Logger, filename: str) -> None:
    logger.addHandler(RotatingFileHandler(filename, maxBytes=LOG_MAXSIZE, backupCount=LOG_BACKUP_COUNT))
    logger.setLevel(logging.DEBUG)

init_logger(logger, LOG_FILE)

def should_respond(text: str) -> bool:
    return should_respond_re.search(text)

def mention_loop() -> None:
    logger = logging.getLogger('randomwaite.mentions')
    init_logger(logger, MENTIONS_LOG_FILE)
    logger.debug('starting mentions listener...')
    redis = Redis()
    twitter_client = twitter.get_client()

    while True:
        since_id = redis.get(SINCE_KEY)
        mentions = twitter.get_mentions(twitter_client, since_id)
        if len(mentions) > 0:
            logger.debug('found some mentions')
        else:
            logger.debug('found no mentions')

        for mention in mentions:
            if not should_respond(mention.text):
                logger.debug('found mention but it is not for responding to')
                continue
            username = mention.author.screen_name
            status_id = mention.id_str
            handle_reply.delay(status_id, username)

        if len(mentions) > 0 and mentions[0].id_str != since_id:
            logger.debug('updated since_id in redis')
            redis.set(SINCE_KEY, mentions[0].id_str)

        logger.debug('done, sleeping...')
        sleep(MENTION_CHECK_INTERVAL)

def generation_loop() -> None:
    logger = logging.getLogger('randomwaite.generation')
    init_logger(logger, GENERATION_LOG_FILE)
    logger.debug('starting generation loop...')
    twitter_client = twitter.get_client()

    while True:
        logger.debug('wakin up to tweet')
        card = draw_tarot_card()
        im = generate(card)

        twitter.post_image(twitter_client, card.name.lower(), im)

        logger.debug('tweeted, going back to sleep')

        sleep(GENERATION_INTERVAL)

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
        logger.debug('saving to', DEBUG_IMAGE_PATH)
        im.save(DEBUG_IMAGE_PATH)
        sys.exit(0)


    if not looping:
        im = generate(card)
        twitter_client = twitter.get_client()
        logger.debug('updating twitter...')
        twitter.post_image(twitter_client, card.name.lower(), im)
        sys.exit(0)

    mention_looper = Process(target=mention_loop)
    mention_looper.start()

    generation_looper = Process(target=generation_loop)
    generation_looper.start()

    mention_looper.join()
    generation_looper.join()
