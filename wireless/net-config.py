#!/usr/bin/python

'EVExchange over wifi'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

from mn_wifi.v2g import EV, SE

from time import sleep



class Mininet_wifi_ext(Mininet_wifi):

	attack = True

	def toggle_attack(self):
		#global self.attack
		if self.attack: 
			info("*** EVExchange is active.\n")
			info("*** Deactivating it...\n")
			self.stations[0].cmd("./bridge1.sh")
			self.stations[1].cmd("./bridge2.sh")
			self.attack = False
			info("*** EVExchange deactivated.\n")
		else:
			info("*** EVExchange is NOT active.\n")
			info("*** Activating it...\n")
			self.stations[0].cmd("./mirror1tc.sh")
			self.stations[1].cmd("./mirror2tc.sh")
			self.attack = True
			info("*** EVExchange activated.\n")

	def simple_tests(self):

		self.terms.append(self.hosts[1].startCharge())
		self.terms.append(self.hosts[3].startCharge())

		sleep(5)

		self.terms.append(self.hosts[0].charge(True))

		sleep(7)

		self.terms.append(self.hosts[2].charge(True))

		sleep(7)



def topology():
	"Create a network."
	net = Mininet_wifi_ext()

	info("*** Creating nodes\n")
	ap_arg = {'client_isolation': True, 'position': '10,10,0'}
	ap1 = net.addAccessPoint('ap1', ssid="ap1", mode="g", 
							 channel="5", **ap_arg)
	sta1 = net.addStation('sta1', position='10,10,0')
	sta2 = net.addStation('sta2', position='200,10,0')

	c0 = net.addController('c0')


	ev1 = net.addHost( 'ev1', cls=EV, ip='10.1.10.1/24',
						mac="00:00:00:00:00:11")

	se1 = net.addHost( 'se1', cls=SE, ip='10.1.20.1/24',
						mac="00:00:00:00:00:12")	

	ev2 = net.addHost( 'ev2', cls=EV, ip='10.2.10.1/24',
						mac="00:00:00:00:00:21")

	se2 = net.addHost( 'se2', cls=SE, ip='10.2.20.1/24',
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

	info("*** Starting network\n")
	net.build()
	c0.start()
	ap1.start([c0])

	# 1s side
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
	
	if net.attack:
		info("*** Starting mirrors+tunnels (EVExchange activated)\n")
		sta1.cmd("./mirror1tc.sh")
		sta2.cmd("./mirror2tc.sh")
	else:
		info("** Starting bridges (EVExchange NOT activated")
		sta1.cmd("./bridge1.sh")
		sta2.cmd("./bridge2.sh")
	

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology()
