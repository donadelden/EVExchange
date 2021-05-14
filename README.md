# EVExchange

## Implementations:

  - `/basic_mininet`: first implementation using Mininet (which must be installed) and a cabled connection employing two different interfaces in order to set-up two bridges;
  - `/basic_MiniV2G`: cabled as before, but implemented over MiniV2G _--> to be done, but it is easy;_
  - `/wireless`: to be done using MiniV2G and two MitM devices connected using a wireless channels _--> to be done, really problematic. See below._

### Possible approaches and information for the wireless case:

  - it is possible to connect the two devices without a router using:
    - `WiFiDirect`: sometime it does not work, take a while at the startup, not advised;
    - `adhoc` wifi: more simple, advised (but not yet fully tested)
    - standard connection using an access point that in real-life will be integrated into one of the two devices. It works but it is one more device so probably not the perfect solution.
  - Bridging over wifi seem to be NOT possible, at least not in the simple way of the wired connection. Nice try!
  - keep in mind that RiseV2G (and ISO 15118 in general) employs **IPv6** and in particular it requires a link-local connections between EVs and SEs
    - IPv6 does NOT use ARP but instead uses a system of Neighbors Discovery and Router Solicitations.
  - The target topology for the attack is the following:
  ```
     ev1 --- dev1 --- se1
              :
          (wireless)
              :     
     ev2 --- dev2 --- se2
  ```
  - However...
    - can be useful to insert a malicious switch connected to ev1, dev1, se1 (and the same for 2) to redirect everything from ev1 to dev1?
    - ...or is it better to route everything inside dev1 itself?
  - Ruffly, the communication is composed of:
    1. the EV send an UDP SECC Discovery request in broadcast from a _random_port_ev_0_ to 15118;
    2. SE respond sending its ipv6 with an unicast packet from 15118 to _random_port_ev_0_
    3. EV starts the TCP handshake from _random_port_ev_1_ to _random_port_se_1_ and the communication starts
  - We DOES NOT need to read the packets, but only to forward them. We have (at least) two possible options to do so (specified for the flow EV-->SE, the reverse is almost the same):
    1. **never change IPs**: use the MitM devices to:
      - intercepts each packet (also the ones not directed to us) coming from the EV
      - sends to the other device
      - recreates the exact same packet sending it to the SE

      With this strategy IPs of the packets are leaved untouched.
    2. **dynamic change IPs**: the MitM tricks the EV into thinking that the MitM is the SE (and viceversa). So the MitM will:
      - receives each packet (which are sent to the MitM IP)
      - send the packets to the other device
      - the second MitM device change the source IP address to its own and send to the SE

  - Various things already tested/to be tested:
    - use Scapy/netfilterqueue to get packets from the EV interface of MitM, encapsulate them into UDP packets, send them to the other MitM, decapsulate and recreate on the SE interface --> Scapy seems to be too slow for TCP connections that gets timeout.   
    - use [mirroring](https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/) to copy all the ingress traffic of the MitM to the wireless interface --> seems that the packets does not arrive on the other side of the wireless connection (using an ap, maybe worth trying with adhoc wifi?)
    - Mauro suggested to use sockets.  
