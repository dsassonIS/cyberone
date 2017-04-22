#! /usr/bin/env python
from scapy.all import *

from utils import logger

# logger ref
log = logger.getLogger()


# TODO: should support multiprocessing
def pingCheck(ip):
    ping = IP(dst=ip, ttl=20) / ICMP()

    reply = sr1(ping, timeout=3, verbose=0)
    # log.debug(reply.show())

    if not (reply is None) and (reply.src == ip):
        log.debug("dst ip is " + ip)
        log.debug('{} online'.format(reply.src))


if __name__ == "__main__":
    for ip in range(0, 256):
        pingCheck(ip)
