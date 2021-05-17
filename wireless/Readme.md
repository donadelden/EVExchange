# Mirror + Tunnel

### Instructions

By running `net-config.py` you will run MiniV2G (which must be installed!) and create the topology (presented below). *EVExchange* is activated by default.

You can run simples test with `py net.simple_tests()` which will:
	
	- spawn two xterms with the two SEs ready to receive charges;
	- start charging from ev1 in a xterm;
	- start charging from ev2 in a xterm.

Furthermore, you can use `py net.toggle_attack()` to activate/deactivate *EVExchange*.


### Topology
![topology](https://github.com/donadelden/EVExchange/blob/main/pics/wifi-topology.png?raw=true)


### References

main ref: http://arthurchiao.art/blog/traffic-mirror-with-tc-and-tunneling/
other ref: https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/

 It also uses `qdisc` as a netfilterqueue to "select" certain packet in a certain interface