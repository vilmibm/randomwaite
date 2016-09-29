import logging
import os
from logging.handlers import RotatingFileHandler

LOGFILE = '/tmp/randomwaite.{}.log'
MAXLOGSIZE = 1000 * 1000 * 10 # 10 mb
BACKUP_COUNT = 5
LOGGER_NAME = 'randomwaite.{}'


def get_logger() -> logging.Logger:
    pid = os.getpid()
    logger = logging.getLogger(LOGGER_NAME.format(pid))
    logger.addHandler(RotatingFileHandler(LOGFILE.format(pid),
                                          maxBytes=MAXLOGSIZE,
                                          backupCount=BACKUP_COUNT))
    logger.setLevel(logging.DEBUG)
    return logger

