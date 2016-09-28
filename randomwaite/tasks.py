from celery import Celery

from . import secrets as sec
from .twitter import post_image, get_client
from .images import generate

app = Celery('randomwaite.tasks', broker='redis://localhost')

@app.task
def handle_reply(status_id: str, username: str) -> None:
    print('IN TASK')
    twitter_client = get_client()
    im, card = generate()
    print('GOT IMAGE')
    text = "@{} {}".format(username, card.name)
    post_image(twitter_client, text, im, reply_to_status_id=status_id)
