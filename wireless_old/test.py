from scapy.all import *

a = rdpcap("2nd_udp.pcap")
a = Ether()/a[10][IPv6]

def response(pkt):
    global a
    a[UDP].dport = pkt[UDP].sport
    sendp(a, iface="sta1-eth0")

sniff(iface="sta1-eth0", filter="udp", count=10, prn=response)
