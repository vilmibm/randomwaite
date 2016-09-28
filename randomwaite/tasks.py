from celery import Celery

from . import secrets as sec
from .twitter import post_image

app = Celery('tasks', broker='redis://localhost')

@app.task
def handle_reply(status_id: str, username: str) -> None:
    pass
