# Mirroring for sta1

################ ev1

# set up the new interface for the tunnel 
ip link add vxlan0 type vxlan id 100 local 10.0.20.10 remote 10.0.20.20 dev sta1-wlan0 dstport 4789
ip link set vxlan0 up

# mirror all the ingress traffic of sta1-eth1 to vxlan0

# estabilish qdisc to interfaces
tc qdisc add dev sta1-eth1 ingress

# create the filter who match all and send to vxlan0
tc filter add dev sta1-eth1 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev vxlan0

### the way back
# mirror all the ingress in vxlan0 to sta1-eth1

# estabilish qdisc to interfaces
tc qdisc add dev vxlan0 ingress

# create the filter who match all and send to sta1-eth1
tc filter add dev vxlan0 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev sta1-eth1

