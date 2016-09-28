set -x

venv=$1

source $venv/bin/activate

celery -A randomwaite.tasks worker --logfile=/tmp/randomwaite.celery.log --loglevel=info --detach
randomwaite loop

