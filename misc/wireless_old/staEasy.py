from scapy.all import *
import sys

THIS_IP = ''
OTHER_IP = ''
STA_NAME = ''

EV1_IP_LOCAL = 'fe80::200:ff:fe00:10'
EV1_MAC = '00:00:00:00:00:10'

pkts = []

def set_IPs(num):
    # TODO: to be fixed in the end
    """
    EV1_MAC = '00:00:00:00:00:10'
    SE1_MAC = '00:00:00:00:00:11'

    EV1_IP = '2001:DB8:1::10/64'
    SE1_IP = '2001:DB8:1::11/64'
    EV1_IP_LOCAL = 'fe80::200:ff:fe00:10'

    EV2_IP = '2001:DB8:2::20/64'
    SE2_IP = '2001:DB8:2::21/64'

    EV1_MAC = '00:00:00:00:00:20'
    SE1_MAC = '00:00:00:00:00:21'
    """
    STA1_IP = '192.168.0.1'
    STA2_IP = '192.168.0.2'
    global THIS_IP, OTHER_IP
    if(num==1):
        THIS_IP = STA1_IP
        OTHER_IP = STA2_IP
    elif(num==2):
        THIS_IP = STA2_IP
        OTHER_IP = STA1_IP
    else:
        print("There are only station 1 or 2")
        exit(1)

# docs: 2015_Bookmatter_UnderstandingNetworkHacks.pdf
def response(pkt):
    global pkts
    #print(pkt.summary())
    # craft response to Neighbor Discovery Request
    # it is needed otherwise SE will not send the second UDP packet
    if(pkt not in pkts and ICMPv6ND_NS in pkt and pkt[ICMPv6ND_NS].tgt==EV1_IP_LOCAL):
        print("*** Crafting ICMPv6ND_NA")
        # TODO: do this dynamically by looking at the first UDP packet
        # and exclude not related requests
        r = Ether(dst=pkt[Ether].src, src=EV1_MAC)
        r /= IPv6(dst=pkt[IPv6].src, src=EV1_IP_LOCAL)
        r /= ICMPv6ND_NA(tgt=EV1_IP_LOCAL, R=0, S=1, O=1, res=0x0)
        r /= ICMPv6NDOptDstLLAddr(type=2, len=1, lladdr=EV1_MAC)
        pkts.append(r)
        # TODO: it is useless to send the packet on both the interfaces,
        # find a way to select the right one
        sendp(r, iface=STA_NAME+'-eth0')
        sendp(r, iface=STA_NAME+'-eth1')
    # responde to a tunneled pkt
    elif(UDP in pkt and pkt[UDP].dport==15119):
        print("*** Pkt decapsulated and ready to be sent:")
        r = bytes(pkt[Raw])
        r = Ether(r)
        print(r.summary())
        pkts.append(r)
        sendp(r, iface=STA_NAME+'-eth0')
        sendp(r, iface=STA_NAME+'-eth1')
    # pick the packet and tunnel it (if not sended nefore)
    elif(pkt not in pkts and ((UDP in pkt) or (TCP in pkt))):
        print("*** Pkt received and ready to be tunneled:")
        p = IP(dst=OTHER_IP)/UDP(dport=15119, sport=55555)/Raw(load=raw(pkt))
        print(p.summary())
        send(p, iface=STA_NAME+'-wlan0')

    # save the already seen packets to avoid retransmissions
    pkts.append(pkt)


if __name__ == '__main__':
    if len(sys.argv)<=1:
        print("*** You need to pass the station number!\nExit.")
        exit(1)
    STA_NAME = 'sta'+str(sys.argv[1])
    STA_NUMBER = int(STA_NAME[3])
    set_IPs(STA_NUMBER)
    print("My IP: {}; other device IP: {}".format(THIS_IP, OTHER_IP))
    print("*********************************************")
    print("*** Station " + str(STA_NUMBER) + " (" + STA_NAME +")")

    sniff(iface=[STA_NAME+'-eth0', STA_NAME+'-eth1', STA_NAME+'-wlan0'], prn=response, filter="udp or tcp or icmp6")
