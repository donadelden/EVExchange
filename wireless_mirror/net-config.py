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
    ap_arg = {'client_isolation': True}
    ap1 = net.addAccessPoint('ap1', ssid="ap1", mode="g",
                             channel="5",**ap_arg)
    sta1 = net.addStation('sta1', ip='11.0.0.1/24')#, position='10,10,0')
    sta2 = net.addStation('sta2', ip='11.0.0.2/24')#, position='20,20,0')

    c0 = net.addController('c0')


    ev1 = net.addHost( 'ev1', ip='10.0.0.10/24',
                        #defaultRoute='via 10.1.0.1',
                        mac="00:00:00:00:00:10")

    se2 = net.addHost( 'se2', ip='10.0.0.21/24',
                        #defaultRoute='via 10.1.0.2',
                        mac="00:00:00:00:00:21")


    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    net.addLink(ev1, sta1, intfName2='sta1-eth0',
                   params2={ 'ip' : '10.0.0.110/24'} )
    #sta1.setMac('00:00:00:00:01:10', 'sta1-eth0') # doesn't work, thank you mininet wifi!
    net.addLink(se2, sta2, intfName2='sta2-eth1',
                   params2={ 'ip' : '10.0.0.221/24'} )
    #sta2.setMac('00:00:00:00:02:21', 'sta2-eth1')



    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])


    ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,arp,in_port=1,'
            'actions=output:in_port,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,icmp,in_port=1,'
            'actions=output:in_port,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,udp,in_port=1,'
            'actions=output:in_port,normal"')
    ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,tcp,in_port=1,'
            'actions=output:in_port,normal"')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
