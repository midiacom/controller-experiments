#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from time import sleep

def ovsns():

    "Create an empty network and add nodes to it."

    mn = Mininet( topo=None,
                   build=False)

    h1 = mn.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
    s1 = mn.addHost( 's1', ip='0.0.0.0' )
    s2 = mn.addHost( 's2', ip='0.0.0.0' )
    h2 = mn.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
    #c0 = mn.addHost( 'c0', ip='10.0.0.13' ) # This is a host!

    mn.addLink( h1, s1 )
    mn.addLink( s1, s2 )
    mn.addLink( h2, s2 )
    #mn.addLink( c0, s2 )

    mn.start()

    #c0.cmd('/home/juan/.local/bin/ryu-manager ryu.app.simple_switch > logs/ryu.log 2>&1 &')
    h1.cmd('/home/juan/.local/bin/ryu-manager ryu.app.simple_switch > logs/ryu.log 2>&1 &')
    
    s1.cmd('bash sw_config_script.sh s1 100 > logs/s1.log')
    s2.cmd('bash sw_config_script.sh s2 101 > logs/s2.log')

    s1.cmd('tcpdump -i s1-eth1 -w logs/s1-eth1.pcap port not 53 &')
    s2.cmd('tcpdump -i s2-eth0 -w logs/s2-eth0.pcap port not 53 &')
    h1.cmd('tcpdump -i h1-eth0 -w logs/h1.pcap port not 53 &')
    h2.cmd('tcpdump -i h2-eth0 -w logs/h2.pcap port not 53 &')

    h2.cmd('ping -c 1 10.0.0.1')

    #h1.cmd('tcpreplay -i h1-eth0 -K --mbps 2 packets.pcap > logs/tcpreplay_info.txt')
    #sleep(30)
    #s1.cmd('ovs-ofctl dump-flows s1 > logs/flows_s1.log 2>&1 &')
    #s2.cmd('ovs-ofctl dump-flows s1 > logs/flows_s1.log 2>&1 &')

    s1.cmd('killall -2 tcpdump')

    CLI( mn )

    h1.cmd('rm -rf /tmp/mininet-s*')
    mn.stop()



if __name__ == '__main__':
    setLogLevel( 'info' )
    ovsns()