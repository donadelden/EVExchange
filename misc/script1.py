from socket import socket
from scapy.all import *
import netifaces as ni


bufsize = 1024 # Modify to suit your needs
listenHost = "::"
other_sta = "11.0.0.2"
my_sta = "11.0.0.1"
this_ip_ev = ni.ifaddresses('sta1-eth0')[ni.AF_INET6][0]['addr']
listenPort = 15118 # at least, at the begin
targetPort = 8787

evIP = ""
SDPport = 0

def forward(data, port):
    print("Forwarding: '%s' from port %s" % (data, port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_sta, port)) # Bind to the port data came in on
    sock.sendto(data, ("11.0.0.2", targetPort))

def listen6(host, port):
    global evIP, SDPport
    listenSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    listenSocket.bind((host, port, 0, 0))
    c = True
    while True:
        data, addr = listenSocket.recvfrom(bufsize)
        print(data)
        evIP = addr[0]
        SDPport = addr[1]
        print(evIP)
        forward(data, addr[1]) # data and port
        # after the reception of first SDP exit
        if b"\x01\xfe\x90\x00\x00\x00\x00\x02\x10\x00" in data:
            return

def listen(host, port):
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listenSocket.bind((host, port))
    while True:
        data, addr = listenSocket.recvfrom(bufsize)
        print(data, addr)
        print("SDP response received")
        sendp(Ether()/IPv6(src=this_ip_ev, dst=evIP)/UDP(sport=15118,dport=SDPport)/Raw(data), iface="sta1-eth0")
        #get and forward ICMP
        #sniff(...)
        #forward(...)

# listen for SDP first packet,
# return when received and forwarded
listen6("::", 15118)
# listen for SDP response. Then forward
print("Start listining on wlan")
listen(my_sta, targetPort)
# here tcp client initialization start... with a neighbor solicitation to the REAL se2 ip....
