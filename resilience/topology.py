from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from time import sleep
from sys import argv
from functools import partial

CONVERTER = {
    1: {'pps': 1, 'length': '30k'},
    5: {'pps': 0.2, 'length': '6k'},
    100: {'pps': 1, 'length': '100'},
    10: {'pps': 0.1, 'length': '3k'}
}

CONTROLLER = {
    'odl': 'arp',
    'onos': 'goose'
}


class Simple_Topology(Topo):
    def __init__(self, switches=1):
        Topo.__init__(self)

        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')

        switch_list = []
        for switch in range(1, switches + 1):
            switch_list.append(self.addSwitch('s' + str(switch)))

        # Links
        internet = dict(bw=10)
        self.addLink(h1, switch_list[0], **internet)
        for switch in range(switches - 1):
            sA = switch_list[switch]
            sB = switch_list[switch + 1]
            self.addLink(sA, sB, **internet)
        self.addLink(switch_list[-1], h2, **internet)


def main(remote_ip, switches, interval, name):
    topo = Simple_Topology(switches)
    of13 = partial(OVSSwitch, protocols='OpenFlow13')
    mn = Mininet(topo=topo, controller=None, link=TCLink, switch=of13)
    mn.addController(
        'c0', controller=RemoteController, ip=remote_ip, port=6633)
    h1, h2, c0 = mn.get('h1', 'h2', 'c0')

    for h in mn.hosts:
        # disable ipv6
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

    for sw in mn.switches:
        # disable ipv6
        sw.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        sw.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        sw.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

    c0.cmd('rm -rf logs')
    c0.cmd('mkdir -p logs')

    c0.cmd("top -b -d 1 | grep 'load\|KiB Mem' >> ", 'logs/top_geral.txt &')
    c0.cmd("top -b -d 1 | grep 'sudo\|ovs\|tcpdump' >>", 'logs/top.txt &')

    c0.cmd('tcpdump -i enp1s0 -w logs/openflow.pcap port 6633 &')
    for sw in mn.switches:
        intf1 = str(sw.intfs[1])
        sw.cmd(
            'tcpdump -i', intf1, ' -w logs/' + intf1 + '.pcap port not 53 &')
        intf2 = str(sw.intfs[2])
        sw.cmd(
            'tcpdump -i', intf2, ' -w logs/' + intf2 + '.pcap port not 53 &')
    h1.cmd('tcpdump -i h1-eth0 -w logs/h1.pcap port not 53 &')
    h2.cmd('tcpdump -i h2-eth0 -w logs/h2.pcap port not 53 &')
    mn.start()

    sleep(2)
    h2.cmd('ping -c 1 10.0.0.1')

    pps = CONVERTER[interval]['pps']
    length = CONVERTER[interval]['length']
    pcap = CONTROLLER[name]
    h1.cmd(
        'tcpreplay -i h1-eth0 -K -p', pps,
        'packets/' + pcap + length + '.pcap >',
        'logs/tcpreplay_info.txt')
    sleep(2)
    for sw in mn.switches:
        sw.cmd(
            'ovs-ofctl -O OpenFlow13 dump-flows', str(sw),
            '> logs/flows_' + str(sw) + '.log')
    c0.cmd('chmod 777 -R logs')
    c0.cmd('killall -2 tcpdump')
    mn.stop()


topos = {'simple_topo': (lambda: Simple_Topology())}

if __name__ == '__main__':
    setLogLevel('debug')
    if len(argv) != 5:
        print(
            'Usage: sudo python topology.py <controller-ip> '
            '<number-of-switches> <interval-in-seconds> <controller-name>\n'
            'e.g.: sudo python topology.py 127.0.0.1 1 100 odl')
        exit(-1)
    switches = int(argv[2])
    interval = int(argv[3])
    if switches < 1:
        print('ERROR the topology needs at least 1 switch')
        exit(-1)
    if interval not in CONVERTER:
        print('ERROR unknown interval')
        exit(-1)
    main(argv[1], switches, interval, argv[4].lower())
