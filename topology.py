from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
# from mininet.cli import CLI
from mininet.link import TCLink


class Simple_Topology(Topo):
    def __init__(self):
        Topo.__init__(self)

        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # TODO Decide link parameters
        # Use htb?
        internet = dict(bw=10, delay='2.5ms', loss=2, max_queue_size=100)
        local = dict(bw=100, delay='0.1ms', loss=1, max_queue_size=1000)

        # Links
        self.addLink(h1, s1, **internet)
        self.addLink(s1, s2, **local)
        self.addLink(h2, s2, **internet)


def main():
    topo = Simple_Topology()
    mn = Mininet(topo=topo, controller=None, link=TCLink)
    mn.addController(
        'c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    mn.start()
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

    c0.cmd('tcpdump -i lo -w openflow.pcap port 6633 &')
    h1.cmd('tcpdump -i h1-eth0 -w h1.pcap port not 53 &')
    h2.cmd('tcpdump -i h2-eth0 -w h2.pcap port not 53 &')
    h1.cmd('ping -c 5 10.0.0.2')
    h2.cmd('ping -c 5 10.0.0.1')

    mn.stop()


topos = {'simple_topo': (lambda: Simple_Topology())}

if __name__ == '__main__':
    # setLogLevel('debug')
    setLogLevel('critical')
    main()
