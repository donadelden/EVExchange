# this code is able to take all the traffic from the tunnel and replay to sta2-eth1

# set up the new interface for the tunnel 
ip link add vxlan0 type vxlan id 100 local 10.0.20.20 remote 10.0.20.10 dev sta2-wlan0 dstport 4789
ip link set vxlan0 up

# estabilish qdisc to interfaces
tc qdisc add dev vxlan0 ingress

# create the filter who match all and send to sta2-eth1
tc filter add dev vxlan0 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev sta2-eth1
