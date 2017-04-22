#!/usr/bin/python

from multiprocessing import Lock
from socket import *

from gevent.pool import Pool
from gevent.queue import Queue

from utils import logger

# TODO: support multiprocessing

# logger ref
log = logger.getLogger()

open_ports = []

q = Queue()

# port scanner params
port_scanner_ip = ""
port_scanner_start = 0
port_scanner_stop = 0


def set_ip(ip):
    global port_scanner_ip
    port_scanner_ip = ip


def set_range(portStart, portStop):
    global port_scanner_start, port_scanner_stop, q
    port_scanner_start = portStart
    port_scanner_stop = portStop

    for p in range(port_scanner_start, port_scanner_stop):
        q.put_nowait(p)


def scan(ip, lock):
    s = socket()
    for _ in range(port_scanner_start, port_scanner_stop):

        try:
            # lock.acquire
            port = q.get()
            s.connect((ip, port))
            # TODO: shared resource need to protect
            open_ports.append(port)
            log.debug("port: %d --> OPEN " % port)
            # lock.release()
        except:
            log.debug("port: %d --> CLOSED " % port)
            continue


def main(ip):
    global port_scanner_ip
    lock = Lock()

    if port_scanner_ip is 0:
        port_scanner_ip = ip
    # TODO: currently using only one pool ....
    pool = Pool(1)
    for i in range(1):
        pool.spawn(scan, port_scanner_ip, lock).join()
    return open_ports
