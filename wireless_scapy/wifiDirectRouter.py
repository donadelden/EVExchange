#!/usr/bin/python

'Example for WiFi Direct - "no" switch'

import sys
from time import sleep

from mininet.node import UserSwitch
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, WifiDirectLink
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(link=wmediumd,
                       wmediumd_mode=interference,
                       configWiFiDirect=True)
    c10, c11, c20, c21 = net.addController('c10'), net.addController('c11'), net.addController('c20'), net.addController('c21')

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip='192.168.0.1/24', mac="00:00:00:00:11:11", position='10,10,0')
    sta2 = net.addStation('sta2', ip='192.168.0.2/24', mac="00:00:00:00:22:22", position='20,20,0')

    s10, s11, s20, s21 = net.addSwitch('s10'), net.addSwitch('s11'), net.addSwitch('s20'), net.addSwitch('s21')

    net.addLink(s10, sta1, intfName2='sta1-eth0',
                  params2={ 'ip' : '10.1.0.1/24' } )
    net.addLink(s11, sta1, intfName2='sta1-eth1',
                  params2={ 'ip' : '10.1.0.2/24' } )

    net.addLink(s20, sta2, intfName2='sta2-eth0',
                  params2={ 'ip' : '10.2.0.1/24' } )
    net.addLink(s21, sta2, intfName2='sta2-eth1',
                  params2={ 'ip' : '10.2.0.2/24' } )

    ev1 = net.addHost( 'ev1', ip='10.1.0.10/24',
                        defaultRoute='via 10.1.0.1',
                        mac="00:00:00:00:00:10")
    ev2 = net.addHost( 'ev2', ip='10.2.0.20/24',
                        defaultRoute='via 10.2.0.1',
                        mac="00:00:00:00:00:20")

    se1 = net.addHost( 'se1', ip='10.1.0.11/24',
                        defaultRoute='via 10.1.0.2',
                        mac="00:00:00:00:00:11")
    se2 = net.addHost( 'se2', ip='10.2.0.21/24',
                        defaultRoute='via 10.2.0.2',
                        mac="00:00:00:00:00:21")

    net.addLink(ev1, s10)
    net.addLink(se1, s11)

    net.addLink(ev2, s20)
    net.addLink(se2, s21)


    #if '-p' not in args:
    #    net.plotGraph(max_x=200, max_y=200)


    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Starting WiFi Direct\n")
    net.addLink(sta1, intf='sta1-wlan0', cls=WifiDirectLink)
    net.addLink(sta2, intf='sta2-wlan0', cls=WifiDirectLink)

    info("*** Starting network\n")
    net.build()

    info( '*** Starting things\n')
    for controller in net.controllers:
        controller.start()
    s10.start([c10])
    s11.start([c11])
    s20.start([c20])
    s21.start([c21])

    info( '*** Setting up wifi direct (can take up to 10 seconds)\n')
    sta1.cmd('wpa_cli -ista1-wlan0 p2p_find')
    sta2.cmd('wpa_cli -ista2-wlan0 p2p_find')
    sta2.cmd('wpa_cli -ista2-wlan0 p2p_peers')
    sleep(3)
    sta1.cmd('wpa_cli -ista1-wlan0 p2p_peers')
    sleep(3)
    pin = sta1.cmd('wpa_cli -ista1-wlan0 p2p_connect %s pin auth'
                   % sta2.wintfs[0].mac)
    sleep(3)
    sta2.cmd('wpa_cli -ista2-wlan0 p2p_connect %s %s'
             % (sta1.wintfs[0].mac, pin))

    info('*** Setting up IPv6 on interfaces\n')
    ev1.cmd('ip -6 address add 2001:DB8:1::10/64 dev ev1-eth0')
    se1.cmd('ip -6 address add 2001:DB8:1::11/64 dev se1-eth0')
    ev2.cmd('ip -6 address add 2001:DB8:2::20/64 dev ev2-eth0')
    se2.cmd('ip -6 address add 2001:DB8:2::21/64 dev se2-eth0')
    sta1.cmd('ip -6 address add 2001:DB8:1::100/64 dev sta1-eth0')
    sta2.cmd('ip -6 address add 2001:DB8:2::200/64 dev sta2-eth0')
    sta1.cmd('ip -6 address add 2001:DB8:1::101/64 dev sta1-eth1')
    sta2.cmd('ip -6 address add 2001:DB8:2::201/64 dev sta2-eth1')


    info('*** Enabling routing\n')
    sta1.cmd('sysctl net.ipv4.ip_forward=1')
    sta2.cmd('sysctl net.ipv4.ip_forward=1')
    """
    sta1.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')
    sta2.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')
    """

    info('*** Setting routing stuffs\n')
    sta1.cmd('route add -net 10.2.0.0/24 gw 192.168.0.2')
    sta2.cmd('route add -net 10.1.0.0/24 gw 192.168.0.1')
    sta1.cmd('route add -net 192.168.0.0/24 gw 192.168.0.2')
    sta2.cmd('route add -net 192.168.0.0/24 gw 192.168.0.1')

    """
    sta1.cmd('ip -6 route add 2001:db8:2::/64 via 2001::2 dev sta1-wlan0')
    sta2.cmd('ip -6 route add 2001:db8:1::/64 via 2001::1 dev sta2-wlan0')

    ev1.cmd('ip -6 route add default via 2001:db8:1::101 dev ev1-eth0')
    se1.cmd('ip -6 route add default via 2001:db8:1::101 dev se1-eth0')
    ev2.cmd('ip -6 route add default via 2001:db8:2::201 dev ev2-eth0')
    se2.cmd('ip -6 route add default via 2001:db8:2::201 dev se2-eth0')
    """

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
