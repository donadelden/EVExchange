#!/bin/sh

# ALK 2014-10-23
# De-provision mirroring config (See mirror-up.sh for provisioning)

# Normally called by boot process or ifdown. i.e.
# --/etc/network/interfaces--
#   iface eth0 inet static
#     address X.X.X.X
#     netmask Y.Y.Y.Y
#     pre-down /etc/network/mirror-down.sh;:

source_if=sta1-eth0

# de-provision ingress mirroring
tc qdisc del dev $source_if ingress;:

# de-provisoin egress mirroring
tc qdisc del dev $source_if root;:
