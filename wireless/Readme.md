# Mirror + Tunnel

main ref: http://arthurchiao.art/blog/traffic-mirror-with-tc-and-tunneling/
other ref: https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/

The mirrors+tunnels are created directly by default on the `net-config.py` file using: 

 - on `sta1` using `mirror1tc.sh`
 - on `sta2` using `mirror2tc.sh`

 It also uses `qdisc` as a netfilterqueue to "select" certain packet in a certain interface


### Topology
![topology](https://github.com/donadelden/EVExchange/blob/main/pics/wifi-topology.png?raw=true)
