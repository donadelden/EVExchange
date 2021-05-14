# this code is able to mirror all the ingress traffic to sta1-eth0 to wlan0
# but it does not arrive to sta2
# ref: https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/

# estabilish qdisc to interfaces
tc qdisc add dev sta1-eth0 ingress
#tc qdisc add dev sta1-eth1 ingress

# create the filter who match all and send to wlan0
tc filter add dev sta1-eth0 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev sta1-wlan0

#tc filter add dev sta1-eth1 parent ffff: \
#    protocol all \
#    u32 match u8 0 0 \
#    action mirred egress mirror dev sta1-wlan0
