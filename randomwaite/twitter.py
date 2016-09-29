import typing as t
from functools import wraps
from io import BytesIO
from time import sleep

from PIL import Image
import tweepy

from . import secrets as sec
from .errors import TwitterMessedUpException
from .logs import get_logger


TwitterClient = tweepy.API
Status = tweepy.models.Status

logger = get_logger()

MAX_RETRIES = 10
DECAY_FACTOR = 2

def twitter_retry(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        tries = 1
        result = None

        while tries <= MAX_RETRIES:
            try:
                logger.debug('making a call to twitter...')
                return fn(*args, **kwargs)
            except tweepy.TweepError as e:
                logger.exception('got an error from twitter')
                sleep(tries ** DECAY_FACTOR)
            finally:
                tries += 1

        if result is None:
            raise TwitterMessedUpException('giving up after {} tries'.format(tries))

    return wrapper


def get_client() -> TwitterClient:
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    return tweepy.API(twitter_auth)

@twitter_retry
def get_mentions(client: TwitterClient, since_id: t.Optional[str]) -> t.List[Status]:
    if since_id:
        return client.mentions_timeline(since_id=since_id)
    else:
        return client.mentions_timeline()

@twitter_retry
def post_image(client: TwitterClient,
               text: str,
               image: Image,
               reply_to_status_id:str=None) -> None:

    logger.debug('posting an image')

    buffer = BytesIO()
    image.save(buffer, format='JPEG')

    if reply_to_status_id:
        client.update_with_media('tarot.jpg',
                                 text,
                                 file=buffer,
                                 in_reply_to_status_id=reply_to_status_id)
    else:
        client.update_with_media('tarot.jpg',
                                 text,
                                 file=buffer)
