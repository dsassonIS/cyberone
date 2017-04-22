#!/usr/bin/python
import time

from scapy.all import *

ip = "127.0.0.1"
pk = IP(src=ip, dst=ip) / UDP(dport=53)  # /DNS()
pck_ok = pk / DNS(rd=1, qd=DNSQR(qname="OK"))
path = "/home/mrrobot/Desktop/"
dir_list = "/home/mrrobot/Desktop/dns_files/*.txt"
num = 0


def isDnsQuery(pck):
    return pck.haslayer("IP") and \
           pck[IP].dst == ip and \
           pck.haslayer("UDP") and \
           pck.haslayer("DNSQR") and pck[UDP].dport == 53


def p_filter(pck):
    return isDnsQuery(pck) and "LAST" not in pck[DNSQR].qname


def f_filter(pck):
    return isDnsQuery(pck) and "LAST." in pck[DNSQR].qname


def n_filter(pck):
    return isDnsQuery(pck) and "FIRST" in pck[DNSQR].qname


def build_file(pcks, file_name):
    cks = 1
    print "Creating {}".format(file_name)
    f = open(str(path + "/" + file_name), "w")
    for pck in pcks:
        h = pck[DNSQR].qname[:-1].split('|')
        print h
        if h[0] == str(cks):
            f.write(h[1].decode("hex"))
            cks += 1
        else:
            print "Packet number {} didnt recived".format(cks)

    f.close()


def receiveFiles(num):
    print "Getting files"
    for i in range(num):
        print "Waiting for Packet Length per file"
        n = sniff(count=1, lfilter=n_filter)[0]
        name = n[DNSQR].qname[:-1].split("|")[1]
        c = n[DNSQR].qname[:-1].split("|")[2]
        print "Getting {0} packets of {1}".format(c, name)

        numberOf = int(c)

        if numberOf == 0:
            numberOf = 1
        print numberOf

        pcks = sniff(count=numberOf, lfilter=p_filter)
        print "received all wanted packets waiting for LAST"
        sniff(count=1, lfilter=f_filter)[0]
        build_file(pcks, name)
        print "Received file - sending Ack"
        send(pck_ok, verbose=0)
        print "Finished"
        time.sleep(2)
