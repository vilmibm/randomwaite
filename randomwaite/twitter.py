from io import BytesIO

from PIL import Image
import tweepy

from . import secrets as sec

def post_image(text: str,
               image: Image,
               reply_to_status_id:str=None) -> None:
    twitter_auth = tweepy.OAuthHandler(sec.TWITTER_KEY, sec.TWITTER_SECRET)
    twitter_auth.set_access_token(sec.TWITTER_ACCESS_TOKEN, sec.TWITTER_ACCESS_SECRET)
    client = tweepy.API(twitter_auth)

    buffer = BytesIO()
    image.save(buffer, format='JPEG')

    if reply_to_status_id:
        # TODO pass in_reply_to_status_id=reply_to_status_id
        raise Exception('Not Implemented')
    else:
        client.update_with_media('tarot.jpg', text, file=buffer)
