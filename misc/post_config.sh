#
# Source routing to enable the usage of two NICs within the same subnet
#
#ref: https://access.redhat.com/it/solutions/3152391

echo -e "\n# v2g\n100 t1\n101 t2" >> /etc/iproute2/rt_tables

ip route add 10.0.0.0/24 dev sta1-eth0 src 10.0.0.110 table t1
ip route add table t1 default via 10.0.0.254 dev sta1-eth0

ip route add 10.0.0.0/24 dev sta1-wlan0 src 10.0.0.1 table t2
ip route add table t2 default via 10.0.0.2 dev sta1-wlan0

ip rule add table t1 from 10.0.0.110
ip rule add table t2 from 10.0.0.1

ip route show

sysctl net.ipv4.conf.default.arp_filter=1
