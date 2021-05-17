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


################ se1

# set up the new interface for the tunnel 
ip link add vxlan1 type vxlan id 100 local 10.0.20.10 remote 10.0.20.20 dev sta1-wlan0 dstport 4790
ip link set vxlan1 up

# mirror all the ingress traffic of sta1-eth2 to vxlan1

# estabilish qdisc to interfaces
tc qdisc add dev sta1-eth2 ingress

# create the filter who match all and send to vxlan1
tc filter add dev sta1-eth2 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev vxlan1

### the way back
# mirror all the ingress in vxlan1 to sta1-eth2

# estabilish qdisc to interfaces
tc qdisc add dev vxlan1 ingress

# create the filter who match all and send to sta1-eth2
tc filter add dev vxlan1 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev sta1-eth2

test=$(bridge link)
if [[ $test == *e1s1* ]];
then 
	# turn down legitimate bridge
	echo 'Turning down the legitimate bridge...'
	ip link set e1s1 down
	ip link set sta1-eth1 nomaster
	ip link set sta1-eth2 nomaster
	ip link delete e1s1 type bridge
fi

echo 'Done, EVExchange setted.'