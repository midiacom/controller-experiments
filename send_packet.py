from scapy.all import ARP
from sys import argv as args
from scapy.layers.inet import Ether
from scapy.config import conf
from time import time


def pingMultiple(limit, initial_mac='00:00:00:00:00:03', iface='h1-eth0', mac_dst="00:00:00:AA:BB:CC"):
    modified_mac = initial_mac
    with conf.L2socket(iface=iface) as s:
        # pkt_list = []
        start = time()
        for _ in range(limit):
            # pkt_list.append(Ether(src=modified_mac, dst=mac_dst)/ARP(pdst="8.8.8.8"))
            pkt = Ether(src=modified_mac, dst=mac_dst)/ARP(pdst="8.8.8.8")
            s.send(pkt)
            modified_mac = modify_mac(modified_mac, 1)
        print('Total {}s'.format(time() - start))
        # for pkt in pkt_list:


def modify_mac(initial_mac, increment):
    mac_int = int(initial_mac.translate(None, ":.- "), 16)
    new_mac = "{:012X}".format(mac_int + increment)
    return ':'.join([new_mac[i:i+2] for i in range(0, len(new_mac), 2)])


if __name__ == '__main__':
    if len(args) == 4:
        pingMultiple(int(args[1]), iface=args[2], mac_dst=args[3])
    else:
        pingMultiple(limit=1000)
