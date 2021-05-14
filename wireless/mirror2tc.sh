# Mirroring for sta2

################ se2

# set up the new interface for the tunnel 
ip link add vxlan0 type vxlan id 100 local 10.0.20.20 remote 10.0.20.10 dev sta2-wlan0 dstport 4789
ip link set vxlan0 up

# take all the traffic from the tunnel and replay to sta2-eth2

# estabilish qdisc to interfaces
tc qdisc add dev vxlan0 ingress

# create the filter who match all and send to sta2-eth2
tc filter add dev vxlan0 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev sta2-eth2

### the way back
# mirror all the ingress in sta2-eth2 to vxlan0

# estabilish qdisc to interfaces
tc qdisc add dev sta2-eth2 ingress

# create the filter who match all and send to vxlan0
tc filter add dev sta2-eth2 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev vxlan0