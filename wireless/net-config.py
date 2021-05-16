#!/usr/bin/python

'This example creates a simple network topology with 1 ap1 and 2 stations'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology():
	"Create a network."
	net = Mininet_wifi()

	info("*** Creating nodes\n")
	ap_arg = {'client_isolation': True, 'position': '10,10,0'}
	ap1 = net.addAccessPoint('ap1', ssid="ap1", mode="g", 
							 channel="5", **ap_arg)
	sta1 = net.addStation('sta1', position='10,10,0')
	sta2 = net.addStation('sta2', position='200,10,0')

	c0 = net.addController('c0')


	ev1 = net.addHost( 'ev1', ip='10.1.10.1/24',
						mac="00:00:00:00:00:11")

	se1 = net.addHost( 'se1', ip='10.1.20.1/24',
						mac="00:00:00:00:00:12")	

	ev2 = net.addHost( 'ev2', ip='10.2.10.1/24',
						mac="00:00:00:00:00:21")

	se2 = net.addHost( 'se2', ip='10.2.20.1/24',
						mac="00:00:00:00:00:22")	

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	info("*** Associating Stations\n")
	net.addLink(sta1, ap1)
	net.addLink(sta2, ap1)
	net.addLink(ev1, sta1)
	net.addLink(se1, sta1)
	net.addLink(ev2, sta2)
	net.addLink(se2, sta2)
	#net.addLink(ev1, sta1, intfName2='sta1-eth0', params2={ 'ip' : '10.0.0.110/24'} )
	#sta1.setMac('00:00:00:00:01:10', 'sta1-eth0')
	#net.addLink(se2, sta2, intfName2='sta2-eth1', #params2={ 'ip' : '10.0.0.221/24'} )
	#sta2.setMac('00:00:00:00:02:21', 'sta2-eth1')

	info("*** Starting network\n")
	net.build()
	c0.start()
	ap1.start([c0])

	# 1s sode
	sta1.cmd('ifconfig sta1-wlan0 10.0.20.10 netmask 255.255.255.0 up')

	sta1.cmd('ifconfig sta1-eth1 10.1.10.10 netmask 255.255.255.0 up')
	ev1.cmd('route add default gw 10.1.10.10')

	sta1.cmd('ifconfig sta1-eth2 10.1.20.10 netmask 255.255.255.0 up')
	se1.cmd('route add default gw 10.1.20.10')

	# 2s side
	sta2.cmd('ifconfig sta2-wlan0 10.0.20.20 netmask 255.255.255.0 up')

	sta2.cmd('ifconfig sta2-eth1 10.2.10.10 netmask 255.255.255.0 up')
	ev2.cmd('route add default gw 10.2.10.10')

	sta2.cmd('ifconfig sta2-eth2 10.2.20.20 netmask 255.255.255.0 up')
	se2.cmd('route add default gw 10.2.20.20')
	
	# wifi
	ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,arp,in_port=1,'
			'actions=output:in_port,normal"')
	ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,icmp,in_port=1,'
			'actions=output:in_port,normal"')
	ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,udp,in_port=1,'
			'actions=output:in_port,normal"')
	ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,tcp,in_port=1,'
			'actions=output:in_port,normal"')

	info("*** Starting mirrors+tunnels\n")
	sta1.cmd("./mirror1tc.sh")
	sta2.cmd("./mirror2tc.sh")

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology()
