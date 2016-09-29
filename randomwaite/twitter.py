import typing as t
from functools import wraps
from io import BytesIO

from PIL import Image
import tweepy

from . import secrets as sec
from .logs import get_logger

TwitterClient = tweepy.API

logger = get_logger()

def twitter_retry(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        max_tries = 10
        tries = 1
        decay_factor = 2
        result = None

        while result is None and tries <= max_tries:
            try:
                result = fn(*args, **kwargs)
            except tweepy.TweepError as e:
                logger.exception('got an error from twitter')
                sleep(tries ** decay_factor)
                tries += 1

        if result is None:
            raise Exception('twitter is seriously ill, giving up after {} tries'.format(tries))

        return result
    return wrapper


def get_client() -> TwitterClient:
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    return tweepy.API(twitter_auth)

@twitter_retry
def get_mentions(client: TwitterClient, since_id: t.Optional[str]):
    if since_id:
        return client.mentions_timeline(since_id=since_id)
    else:
        return client.mentions_timeline()

@twitter_retry
def post_image(client: TwitterClient,
               text: str,
               image: Image,
               reply_to_status_id:str=None) -> None:

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
