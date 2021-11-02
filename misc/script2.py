from socket import socket
from scapy.all import *
import netifaces as ni

# get_if_hwaddr("sta2-eht1")

bufsize = 1024 # Modify to suit your needs
other_sta = "11.0.0.1"
my_sta = "11.0.0.2"
#this_ip_se = 'fe80::e060:a7ff:feb8:a629'
this_ip_se = ni.ifaddresses('sta2-eth1')[ni.AF_INET6][0]['addr']
#this_ip_se = 'fe80::200:ff:fe00:10' #ip ev1
listenPort = 8787
targetPort = 8787

seIP = ""

ni.ifaddresses

def forward(data, port):
    print("Forwarding: '%s' from port %s" % (data, port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_sta, port)) # Bind to the port data came in on
    sock.sendto(data, (other_sta, targetPort))

def listen6(host, port, data=False):
    global seIP
    listenSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    listenSocket.bind((host, port, 0, 0))
    if data!=False: # this is needed to be more fast, change with thread?
        sendp(Ether()/IPv6(src=this_ip_se, dst="ff02::1")/UDP(sport=port,dport=15118)/Raw(data), iface="sta2-eth1")
    while True:
        data, addr = listenSocket.recvfrom(bufsize)
        print(data)
        seIP = addr[0]
        print(seIP)
        forward(data, addr[1]) # data and port

def listen(host, port):
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listenSocket.bind((host, port))
    print("starting listen")
    while True:
        data, addr = listenSocket.recvfrom(bufsize)
        print(data, addr)
        if b"\x01\xfe\x90\x00\x00\x00\x00\x02\x10\x00" in data:
            #sendp(Ether()/IPv6(src=this_ip_se, dst="ff02::1")/UDP(sport=addr[1],dport=15118)/Raw(data), iface="sta2-eth1")
            return (addr[1], data)
        # else: #useless



# waiting for the first SDP packet
(SDPport, data) = listen(my_sta, targetPort)
# listen for the response to the SDP discovery req
print("Starting listen6")
listen6(seIP, SDPport, data)
