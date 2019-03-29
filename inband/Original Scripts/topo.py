#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import setLogLevel, info

class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
        return

def ovsns():

    "Create an empty network and add nodes to it."

    net = Mininet( topo=None,
                   build=False)

    #c0 = net.addController('c0', controller=InbandController, ip='10.0.0.1', port=6633)

    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    s1 = net.addHost( 's1', ip='0.0.0.0' )
    s2 = net.addHost( 's2', ip='0.0.0.0' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )

    net.addLink( h1, s1 )
    net.addLink( s1, s2 )
    net.addLink( h2, s2 )

    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    ovsns()