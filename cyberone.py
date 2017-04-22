#!/usr/bin/python

import logging
import sys

import reconManager
from utils import logger

if __name__ == '__main__':
    # create logger
    logger.loggerInit(logging.DEBUG, logging.DEBUG)
    log = logger.getLogger()
    log.debug("Starting program...");

    comp = 'ibm'
    domain = 'ibm.com'

    reconManager.main(comp, domain)

    # Finished
    log.debug("Finished all.")
    sys.exit(0)
