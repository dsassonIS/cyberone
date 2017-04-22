#!/usr/bin/python

from urllib2 import urlopen

from utils import logger

# logger ref
log = logger.getLogger()


# Function returns the robots.txt for a given url
def robots_get_robots_txt(url):
    if url.endswith('/'):
        path = url
    else:
        path = url + '/'
    # TODO: need to parse and add to list
    log.debug("trying to get robots.txt")
    data = urlopen(path + "robots.txt")

    return data.read()
