#!/usr/bin/python

import logging
import os

# create logger application
_logger = logging.getLogger("cyberOne")


# logger initialization
def loggerInit(fileLogLevel, streamLogLevel):
    # set logger threshold level
    _logger.setLevel(logging.DEBUG)

    # create file handler
    if os._exists('logger.log'):
        os.remove('logger.log')
    fh = logging.FileHandler('logger.log')
    fh.setLevel(fileLogLevel)

    # create console logger
    ch = logging.StreamHandler()
    ch.setLevel(streamLogLevel)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add handlers
    _logger.addHandler(fh)
    _logger.addHandler(ch)


def getLogger():
    return _logger
