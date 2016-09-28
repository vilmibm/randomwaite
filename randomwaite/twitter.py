import typing as t
from io import BytesIO

from PIL import Image
import tweepy

from . import secrets as sec


TwitterClient = tweepy.API

def get_client() -> TwitterClient:
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    return tweepy.API(twitter_auth)

def get_mentions(client: TwitterClient, since_id: t.Optional[str]):
    if since_id:
        return client.mentions_timeline(since_id=since_id)
    else:
        return client.mentions_timeline()

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
