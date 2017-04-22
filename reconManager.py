#!/usr/bin/python

from database import database
from recon import dict_dns
from recon import get_subdomains
from recon import pdf_metadata
from recon import ping_scan
# import get_subdomains
# import facebook
# import linkedin
from recon import port_scanner, robots
from utils import logger

log = logger.getLogger()


def contains(masks, ip):
    while not masks.empty():
        if masks.get() == ip:
            return False
    return True


def main(comp, domain):
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

    log.info("PDF Metadata")
    database.create_metadata_table(con)
    pdf_metadata.main(domain, db)

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


if __name__ == "__main__":
    comp = raw_input("Enter company name: ")
    domain = raw_input("Enter company domain address(without http://www): ")
    main(comp, domain)
