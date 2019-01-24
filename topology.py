from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
# from mininet.cli import CLI
from mininet.link import TCLink
from time import sleep


class Simple_Topology(Topo):
    def __init__(self):
        Topo.__init__(self)

        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
        s1 = self.addSwitch('s1')
        # s2 = self.addSwitch('s2')

        # TODO Decide link parameters
        # Use htb?
        # internet = dict(bw=10, delay='2.5ms', loss=2, max_queue_size=100)
        internet = dict(bw=1000, delay='0.1ms')
        # local = dict(bw=100, delay='0.1ms', loss=1, max_queue_size=1000)

        # Links
        self.addLink(h1, s1, **internet)
        # self.addLink(s1, s2, **local)
        self.addLink(s1, h2, **internet)


def main():
    topo = Simple_Topology()
    mn = Mininet(topo=topo, controller=None, link=TCLink)
    mn.addController(
        'c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    h1, h2, c0, s1 = mn.get('h1', 'h2', 'c0', 's1')

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

    c0.cmd('tcpdump -i lo -w logs/openflow.pcap port 6633 &')
    s1.cmd('tcpdump -i s1-eth1 -w logs/s1-eth1.pcap port not 53 &')
    s1.cmd('tcpdump -i s1-eth2 -w logs/s1-eth2.pcap port not 53 &')
    h1.cmd('tcpdump -i h1-eth0 -w logs/h1.pcap port not 53 &')
    h2.cmd('tcpdump -i h2-eth0 -w logs/h2.pcap port not 53 &')
    mn.start()
    h2.cmd('ping -c 1 10.0.0.1')
    # h1.cmd('python send_packet.py 1000000 h1-eth0 00:00:00:00:00:02')
    h1.cmd('tcpreplay -i h1-eth0 -t -k packets.pcap')
    sleep(2)
    s1.cmd('ovs-ofctl dump-flows s1 > logs/flows_s1.log 2>&1 &')
    c0.cmd('killall -2 tcpdump')
    mn.stop()


topos = {'simple_topo': (lambda: Simple_Topology())}

if __name__ == '__main__':
    setLogLevel('debug')
    main()
