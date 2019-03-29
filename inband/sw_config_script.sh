#!/bin/bash

# - Run Mininet topology with all switches as hosts, assign an IP to each host. (Switches should have IP 0.0.0.0) - topo.py
# - Open host (controller) xterm and start the controller (e.g., Ryu)
# - Run this script in the xterm for each switch started as a host. Param: <switchname> Ex: s1

echo Starting OVSDB for $1
mkdir -p /tmp/mininet-$1

if [ -e /tmp/mininet-$1/conf.db ]; then
   echo DB already exists
else
   echo Creating OVSDB
   ovsdb-tool create /tmp/mininet-$1/conf.db /usr/share/openvswitch/vswitch.ovsschema
fi

ovsdb-server /tmp/mininet-$1/conf.db \
-vconsole:emer \
-vsyslog:err \
-vfile:info \
--remote=punix:/tmp/mininet-$1/db.sock \
--private-key=db:Open_vSwitch,SSL,private_key \
--certificate=db:Open_vSwitch,SSL,certificate \
--bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
--no-chdir \
--log-file=/tmp/mininet-$1/ovsdb-server.log \
--pidfile=/tmp/mininet-$1/ovsdb-server.pid \
--detach \
--monitor

ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock --no-wait init

echo Starting OVS for $1
ovs-vswitchd unix:/tmp/mininet-$1/db.sock \
-vconsole:emer \
-vsyslog:err \
-vfile:info \
--mlockall \
--no-chdir \
--log-file=/tmp/mininet-$1/ovs-vswitchd.log \
--pidfile=/tmp/mininet-$1/ovs-vswitchd.pid \
--detach \
--monitor

echo Configure OVS for $1
ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock add-br $1
ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock add-port $1 $1-eth0
ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock add-port $1 $1-eth1
# TODO: Adicionar porta do switch s2
ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock set-fail-mode $1 secure
# Set the controller in the specified IP and Port
ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock set-controller $1 tcp:10.0.0.1:6633
# ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock set-controller $1 tcp:10.0.0.13:6633
ovs-vsctl --db=unix:/tmp/mininet-$1/db.sock show

ifconfig $1 inet 10.0.0.$2/8
