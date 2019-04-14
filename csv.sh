#!/bin/bash

echo "experiment,h1_arp,h1_pkt_in,h1_pkt_out,h1_flow_mod,h2_arp,h2_pkt_in,h2_pkt_out,h2_flow_mod,s1_eth0_arp,s1_eth0_pkt_in,s1_eth0_pkt_out,s1_eth0_flow_mod,s1_eth1_arp,s1_eth1_pkt_in,s1_eth1_pkt_out,s1_eth1_flow_mod,s2_eth0_arp,s2_eth0_pkt_in,s2_eth0_pkt_out,s2_eth0_flow_mod,s2_eth1_arp,s2_eth1_pkt_in,s2_eth1_pkt_out,s2_eth1_flow_mod,enp1s0_arp,enp1s0_pkt_in,enp1s0_pkt_out,enp1s0_flow_mod" > sheet.csv
for controller in ODL ONOS Ryu
do
    directories=$(ls ../$controller/)
    for directory in $directories
    do
        openflow_v="openflow_v4"
        if [ $controller == "ONOS" ]
        then
            openflow_v="openflow_v5"
        fi
        echo "Reading ${controller}: $directory"

        arp="eth.dst == 00:00:00:00:00:02 and arp and not $openflow_v"
        packet_in="eth.dst == 00:00:00:00:00:02 and arp and $openflow_v.type == 10"
        packet_out="eth.dst == 00:00:00:00:00:02 and arp and $openflow_v.type == 13"
        flow_mod="$openflow_v.oxm.value_etheraddr == 00:00:00:00:00:02 and $openflow_v.type == 14"

        line="${controller}_$directory"

        for file in h1 h2 s1-eth0 s1-eth1 s2-eth0 s2-eth1 enp1s0
        do
            file_arp=$(tshark -Y "$arp" -r ../$controller/$directory/$file.pcap -T fields -e frame.number | wc -l)
            file_pkt_in=$(tshark -Y "$packet_in" -r ../$controller/$directory/$file.pcap -T fields -e frame.number | wc -l)
            file_pkt_out=$(tshark -Y "$packet_out" -r ../$controller/$directory/$file.pcap -T fields -e frame.number | wc -l)
            file_flow_mod=$(tshark -Y "$flow_mod" -r ../$controller/$directory/$file.pcap -T fields -e frame.number | wc -l)
            line="$line,$file_arp,$file_pkt_in,$file_pkt_out,$file_flow_mod"
        done

        echo $line >> sheet.csv

    done
done
