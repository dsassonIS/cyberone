# !/usr/bin/python
#
import os
import socket

from gevent import queue
from gevent.pool import Pool

# from scapy.all import *

#
# #sub_domains_ip = []
#
q = queue.Queue()
# #lst = open("hostnames.txt", "r").read().split('\n')
# #for sub in lst:
# #    q.put_nowait(sub)
#
#
# def bruteforce2(domain):
#     # db = recon.comp + ".db"
#     # TODO: change to generic
#     db = "wikipedia.db"
#     con = database.connect(db)
#     f = open("IPs.txt", "w")
#     # for sub in range(40):
#     #     if not q.empty():
#     #         site = q.get() + "." + domain
#     #         try:
#     #             pck = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=site))
#     #             answer = sr1(pck, verbose=0)
#     #             count = answer[DNS].ancount
#     #             for i in range(count):
#     #                 dnsrr = answer[DNS].an[i]
#     #                 print "[+]Found " + site + " >> " + dnsrr.rdata + ""
#     #                 database.insert_hosts_data(con, site, dnsrr.rdata, "")
#     #                 f.write(str(dnsrr.rdata) + "\n")
#     #         except socket.error:
#     #             pass
#     f.close()
#
#


sub_domains_ip = {}

queue = queue.Queue
# !/usr/bin/python


import logging
import sys

# import bruteforce_dns
import dict_dns
import get_subdomains
import ping_scan

from database import database
# import get_subdomains
# import facebook
# import linkedin
from recon import port_scanner, robots
from utils import logger


def contains(masks, ip):
    while not masks.empty():
        if masks.get() == ip:
            return False
    return True


def main():
    # create logger
    logger.loggerInit(logging.DEBUG, logging.DEBUG)
    log.debug("Starting program...");

    robots.robots_get_robots_txt("http://www.ynet.co.il")
    # database init
    database.reset(comp)
    con = database.connect(comp + ".db")
    database.create_employees_table(con)
    #    facebook.main(comp)
    #    linkedin.main(comp)
    log.debug("Creating emails")
    # email.main()

    db = comp + ".db"
    con = database.connect(db)
    database.create_hosts_table(con)

    log.debug("Getting sub-domains and IPs")
    subdomains = get_subdomains.main(domain, comp)

    for key, value in subdomains.iteritems():
        database.insert_hosts_data(con, key, value, "")

    subdomains = dict_dns.main(domain)

    for key, value in subdomains.iteritems():
        database.insert_hosts_data(con, key, value, "")
    # #
    # #Bruteforcing domains c class
    # #
    # f = open("IPs.txt", "r").read()
    # ips = []
    # for i in f.split('\n'):
    #     ips.append(i)
    # masks = Queue()
    # pool = Pool(2)
    # for ip in ips:
    #     if not contains(masks, ips):
    #         masks.put_nowait(ip)
    # pool.spawn(bruteforce_dns.main, masks[:masks.qsize()/2]).join()
    # pool.spawn(bruteforce_dns.main, masks[masks.qsize()/2:]).join()

    log.info("Port Scanning")
    port_scanner.set_ip("10.0.0.15")
    port_scanner.set_range(0, 2)
    # j = open("IPs.txt", "r").read()
    # for i in j.split('\n'):
    ports = port_scanner.main(0)

    # port_scanner.set_ip("10.0.0.138")
    # port_scanner.set_range(78, 81)
    # j = open("IPs.txt", "r").read()
    # for i in j.split('\n'):
    # ports = port_scanner.main(0)

    log.info("Ping Scanning")
    for ip in range(0, 256):
        ping_scan.pingCheck("10.0.0." + str(ip))
        # ping_scan.pingCheck("10.0.0.138")

    #    database.update_hosts_ports(con, ports, i)

    # print '''
    #
    #     METADATA
    #
    # '''
    # db = comp + ".db"
    # con = database.connect(db)
    # database.create_metadata_table(con)
    # pdf_metadata.main(domain)

    # Finished
    log.debug("Finished all.")
    sys.exit(0)


if __name__ == "__main__":
    comp = 'ibm'
    # comp = raw_input("Enter company name: ")
    domain = 'ibm.com'
    # domain = raw_input("Enter company domain address(without http://www): ")
    log = logger.getLogger()
    main()

dirpath = os.path.dirname(os.path.realpath(__file__))
lst = open(dirpath + "/hostnames.txt", "r").read().split('\n')
for sub in lst:
    q.put_nowait(sub)


def bruteforce2(domain):
    for sub in range(40):
        if not q.empty():
            site = q.get() + "." + domain
            try:
                ip = socket.gethostbyname(site)
                print "[+]Found " + site + " >> " + ip + ""
                sub_domains_ip[site] = ip
            except socket.error:
                print "[+]Tried " + site
    return sub_domains_ip


def main(domain):
    #
    # BRUTE FORCE 2
    #
    pool1 = Pool(48)
    for i in range(48):
        pool1.spawn(bruteforce2, domain).join()
    return sub_domains_ip
