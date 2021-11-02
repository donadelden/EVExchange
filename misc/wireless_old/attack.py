from scapy.all import *

EV1_MAC = '00:00:00:00:00:10'
SE1_MAC = '00:00:00:00:00:11'

EV1_IP = '2001:DB8:1::10/64'
SE1_IP = '2001:DB8:1::11/64'

EV2_IP = '2001:DB8:2::20/64'
SE2_IP = '2001:DB8:2::21/64'

DUMP_NAME = 'start_udp_ev1se1.pcap'

def sdp_response(pkt):
    if (pkt[IPv6].dst=='ff02::1' and pkt[UDP].dport==15118):
        print("gotcha")

        #resp = Ether(dst=EV1_MAC, src=SE1_MAC, type="IPv6")
        #resp = resp/IPv6(src=EV1_IP, dst=SE1_IP)
        #resp = resp/UDP(sport=15118, dport=pkt[UDP].sport)

        resp = rdpcap(DUMP_NAME)
        resp[1][UDP].dport=pkt[UDP].sport
        resp[1][Raw] = resp[0][Raw]
        sendp(resp[1])

if __name__ == '__main__':
    sniff(count=1, filter="udp", prn=sdp_response)
