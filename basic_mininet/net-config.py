from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def run():

    net = Mininet()

    dev1 = net.addHost( 'dev1', ip='10.0.0.1/24' )
    dev2 = net.addHost( 'dev2', ip='10.0.0.3/24' )


    ev1 = net.addHost( 'ev1', ip='10.0.0.101/24',
                       mac="00:00:00:00:00:01")
    ev2 = net.addHost( 'ev2', ip='10.0.0.102/24',
                       mac="00:00:00:00:00:02")
    se1 = net.addHost( 'se1', ip='10.0.0.111/24',
                       mac="00:00:00:00:00:11")
    se2 = net.addHost( 'se2', ip='10.0.0.112/24',
                       mac="00:00:00:00:00:12")

    net.addLink( ev1, dev1, intfName2='dev-eth1',
                  params2={ 'ip' : '10.0.0.1/24' } )
    net.addLink( se1, dev1, intfName2='dev-eth11',
                  params2={ 'ip' : '10.0.0.2/24' } )

    net.addLink( ev2, dev2, intfName2='dev-eth2',
                  params2={ 'ip' : '10.0.0.3/24' } )
    net.addLink( se2, dev2, intfName2='dev-eth12',
                  params2={ 'ip' : '10.0.0.4/24' } )

    net.addLink( dev1, dev2,
                  intfName1='dev-eth8',
                  params1={ 'ip' : '10.0.0.8/24'},
                  intfName2='dev-eth9',
                  params2={ 'ip' : '10.0.0.9/24' } )

    net.addLink( dev1, dev2,
                  intfName1='dev-eth6',
                  params1={ 'ip' : '10.0.0.6/24'},
                  intfName2='dev-eth7',
                  params2={ 'ip' : '10.0.0.7/24' } )

    net.start()

    #info( '*** Routing Table on Router:\n' )
    #info( net[ 'dev' ].cmd( 'route' ) )

    info( '*** Bridge activation\n')
    dev1 = net.getNodeByName('dev1')
    dev2 = net.getNodeByName('dev2')
    setup(dev1, dev2, normal=True)


    #info( '*** Activate NFQUEUE\n')
    # warning! With this line pingall doesn't work!!!!
    #r0.cmd("iptables -I FORWARD -j NFQUEUE --queue-num 1")
    #info(dev.cmd("iptables -L FORWARD"))


    #for entity in ('ev1','ev2','se1','se2'):
    #    net.getNodeByName(entity).cmd('cd ' + entity)
    #info('*** cd to the right directory done.\n')


    CLI( net )
    net.stop()

def setup(dev1, dev2, normal=True):
    """ normal=True for no attack; normal=False for attack """
    if normal:
        # set up a bridge between 1s
        dev1.cmd('ip link add name e1s1 type bridge')
        dev1.cmd('ip link set e1s1 up')
        dev1.cmd('ip link set dev-eth1 master e1s1')
        dev1.cmd('ip link set dev-eth11 master e1s1')

        # set up a bridge between 2s
        dev2.cmd('ip link add name e2s2 type bridge')
        dev2.cmd('ip link set e2s2 up')
        dev2.cmd('ip link set dev-eth2 master e2s2')
        dev2.cmd('ip link set dev-eth12 master e2s2')
    else:
        # bridge between ev1 and dev2
        dev1.cmd('ip link add name e1d2 type bridge')
        dev1.cmd('ip link set e1d2 up')
        dev1.cmd('ip link set dev-eth1 master e1d2')
        dev1.cmd('ip link set dev-eth8 master e1d2')

        # bridge between dev1 and se2
        dev2.cmd('ip link add name d1s2 type bridge')
        dev2.cmd('ip link set d1s2 up')
        dev2.cmd('ip link set dev-eth9 master d1s2')
        dev2.cmd('ip link set dev-eth12 master d1s2')

        # set up a bridge between ev2 and dev1
        dev2.cmd('ip link add name e2d1 type bridge')
        dev2.cmd('ip link set e2d1 up')
        dev2.cmd('ip link set dev-eth7 master e2d1') #9
        dev2.cmd('ip link set dev-eth2 master e2d1')

        # set up a bridge between dev2 and se1
        dev1.cmd('ip link add name d2s1 type bridge')
        dev1.cmd('ip link set d2s1 up')
        dev1.cmd('ip link set dev-eth6 master d2s1') #8
        dev1.cmd('ip link set dev-eth11 master d2s1')

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
