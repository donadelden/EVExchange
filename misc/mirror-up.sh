#!/bin/sh

# ALK 2014-10-23
# Send all 'source_if' traffic (ingress & egress) to collector box on 'dest_if'

# Normally called by boot process or ifup. i.e.
# --/etc/network/interfaces--
#   iface eth0 inet static
#     address X.X.X.X
#     netmask Y.Y.Y.Y
#     post-up /etc/network/mirror-up.sh;:

source_if=sta1-eth0
dest_if=sta1-wlan0

# enable the destination port
ifconfig $dest_if up;:

# mirror ingress traffic
tc qdisc add dev $source_if ingress;:
tc filter add dev $source_if parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev $dest_if;:

# mirror egress traffic
tc qdisc add dev $source_if handle 1: root prio;:
tc filter add dev $source_if parent 1: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev $dest_if;:
