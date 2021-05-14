# this code is able to mirror all the ingress traffic to sta1-eth0 to wlan0

# set up the new interface for the tunnel 
ip link add vxlan0 type vxlan id 100 local 10.0.20.10 remote 10.0.20.20 dev sta1-wlan0 dstport 4789
ip link set vxlan0 up


# estabilish qdisc to interfaces
tc qdisc add dev sta1-eth1 ingress

# create the filter who match all and send to vxlan0
tc filter add dev sta1-eth1 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev vxlan0

