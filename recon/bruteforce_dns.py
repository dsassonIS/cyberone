#!/usr/bin/python

import socket

from gevent.pool import Pool
from gevent.queue import Queue

import recon
from database import database

q = Queue()
for c in range(1, 255):
    q.put_nowait(c)


# C CLASS BRUTE FORCE
def bruteforce1(mask):
    db = recon.comp + ".db"
    con = database.connect(db)
    f = open("IPs.txt", "a")
    for _ in range(17):
        if not q.empty():
            ip = mask + '.' + q.get()
            try:
                addr = socket.gethostbyaddr(ip)
                database.insert_hosts_data(con, addr, ip, "")
                f.write(str(ip) + "\n")
            except socket.error:
                pass


def main(masks):
    #
    # BRUTE FORCE 1
    #
    while not masks.empty():
        ip = masks.get()
        ip = ip.split('.')
        mask = ip[0] + '.' + ip[1] + '.' + ip[2]
        pool = Pool(15)
        for i in range(15):
            pool.spawn(bruteforce1, mask).join()
