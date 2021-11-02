# Mirror + Tunnel

### Instructions

By running `net-config.py` you will run MiniV2G (which must be installed!) and create the topology (presented below). *EVExchange* is activated by default.

You can run simple tests using `py net.simple_tests()` which will:
	
 - spawn two xterms with the two SEs ready to receive charges;
 - start charging from ev1 in a xterm;
 - start charging from ev2 in a xterm.

Furthermore, you can use `py net.toggle_attack()` to activate/deactivate *EVExchange*.


### Topology
![topology](../misc/pics/wifi-topology.png?raw=true)


### References

main ref: http://arthurchiao.art/blog/traffic-mirror-with-tc-and-tunneling/

other ref: https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/

 It also uses `qdisc` as a netfilterqueue to "select" certain packet in a certain interface

### Some information useless at this point, but maybe it worth keeping them here.

  - it is possible to connect the two devices without a router using:
    - `WiFiDirect`: sometime it does not work, take a while at the startup, not advised;
    - `adhoc` wifi: working on the hybrid testbed, not perfectly working on MiniV2G;
    - standard connection using an access point that in real-life will be integrated into one of the two devices. It works but it is one more device so probably not the perfect solution.
  - Bridging over wifi seem to be NOT possible, at least not in the simple way of the wired connection. Nice try!
  - keep in mind that RiseV2G (and ISO 15118 in general) employs *IPv6* and in particular it requires a link-local connections between EVs and SEs
    - IPv6 does NOT use ARP but instead uses a system of Neighbors Discovery and Router Solicitations.
  - The target topology for the attack is the following:
  ```
     ev1 --- dev1 --- se1
              :
          (wireless)
              :     
     ev2 --- dev2 --- se2
  ```
  - Ruffly, the communication is composed of:
    1. the EV send an UDP SECC Discovery request in broadcast from a _random_port_ev_0_ to 15118;
    2. SE respond sending its ipv6 with an unicast packet from 15118 to _random_port_ev_0_
    3. EV starts the TCP handshake from _random_port_ev_1_ to _random_port_se_1_ and the communication starts
  - Various things already tested/to be tested:
    - use Scapy/netfilterqueue to get packets from the EV interface of MitM, encapsulate them into UDP packets, send them to the other MitM, decapsulate and recreate on the SE interface --> Scapy seems to be too slow for TCP connections that gets timeout.   
    - use [mirroring](https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/) to copy all the ingress traffic of the MitM to the wireless interface --> seems that the packets does not arrive on the other side of the wireless connection (using an ap, maybe worth trying with adhoc wifi?)
    - use sockets.
    - **Adopted idea: vxlan**.