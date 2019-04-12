#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.log import setLogLevel
from time import sleep
from sys import argv as args


def ovsns(user, ctrl_ip='192.168.1.13'):

    "Create an empty network and add nodes to it."

    mn = Mininet(topo=None, build=False, link=TCLink)

    h1 = mn.addHost('h1', ip='192.168.1.3', mac='00:00:00:00:00:01')
    s1 = mn.addHost('s1', ip='0.0.0.0')
    s2 = mn.addHost('s2', ip='0.0.0.0')
    h2 = mn.addHost('h2', ip='192.168.1.4', mac='00:00:00:00:00:02')
    
    # c0 = mn.addHost( 'c0', ip=ctrl_ip, mac='00:00:00:00:00:13' ) # This is a host!
    bandwith = dict(bw=10)
    mn.addLink(h1, s1, **bandwith)
    mn.addLink(s1, s2, **bandwith)
    mn.addLink(h2, s2, **bandwith)
    # mn.addLink( c0, s2 )

    h1.cmd('pkill ovs')
    h1.cmd('rm -rf /tmp/mininet-s*')
    h1.cmd('service openvswitch-switch start')

    Intf('enp1s0', node=s2)

    mn.start()

    # c0.cmd('/home/' + user + '/.local/bin/ryu-manager ryu.app.simple_switch ''> logs/ryu.log 2>&1 &')
    
    # s1.cmdPrint('bash sw_config_script.sh s1 100 2 '+ str(ctrl_ip) +' > logs/s1.log')
    s1.cmdPrint('bash sw_config_script.sh s1 103 2 ' + str(ctrl_ip))
    s2.cmdPrint('bash sw_config_script.sh s2 104 2 ' + str(ctrl_ip) + ' enp1s0')

    for h in mn.hosts:
        print('Disabling IPv6')
        h.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
        h.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
        h.cmd('sysctl -w net.ipv6.conf.lo.disable_ipv6=1')

    s1.cmd('tcpdump -i s1-eth0 -w logs/s1-eth0.pcap port 6653 or ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')
    s1.cmd('tcpdump -i s1-eth1 -w logs/s1-eth1.pcap port 6653 or ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')
    s2.cmd('tcpdump -i s2-eth0 -w logs/s2-eth0.pcap port 6653 or ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')
    s2.cmd('tcpdump -i s2-eth1 -w logs/s2-eth1.pcap port 6653 or ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')
    s2.cmd('tcpdump -i enp1s0 -w logs/enp1s0.pcap port 6653 or ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')
    h1.cmd('tcpdump -i h1-eth0 -w logs/h1.pcap ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')
    h2.cmd('tcpdump -i h2-eth0 -w logs/h2.pcap ether src 00:00:00:00:00:01 or ether dst 00:00:00:00:00:02 or ether dst 00:00:00:00:00:01 &')

    h1.cmd('date > logs/inicio.txt ')
    h1.cmd("top -b -d 1 | grep 'mn\|ovs\|tcpdump' >> logs/top.txt &")

    h2.cmd('ping -c 1 192.168.1.3')

    sleep(20)

    h1.cmd('tcpreplay -i h1-eth0 -K --mbps 10 packets_20k.pcap > logs/tcpreplay_info.txt')

    # s1.cmd('ovs-ofctl dump-flows s1 > logs/flows_s1.log 2>&1 &')
    # s2.cmd('ovs-ofctl dump-flows s1 > logs/flows_s1.log 2>&1 &')

    CLI(mn)

    s1.cmd('killall -2 tcpdump')

    h1.cmd('pkill ovs')
    h1.cmd('rm -rf /tmp/mininet-s*')
    h1.cmd('service openvswitch-switch start')

    mn.stop()


if __name__ == '__main__':
    setLogLevel('info')
    if len(args) == 3:
        ovsns(args[1], args[2])
    else:
        print('Usage: sudo python inband_test.py $USER 192.168.1.17')
