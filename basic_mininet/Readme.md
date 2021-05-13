## Network Charging Simulator on Mininet with Relay Attack

Simple integration of RiseV2G to Mininet to simulate the relay attack.
It uses network bridges to modify the connections between vehicles and stations.

Topology:

      ev1 --- dev1 --- se1
               ||
      ev2 --- dev2 --- se2    

#### Instructions to simulate a charge:
1. Launch the Mininet network using `sudo python net-config.py`
1. (optional) from EVSE1 launch Wireshark using `wireshark &`
2. From the `se1` xterm launch the SECC using `cd se1 && java -jar rise-v2g-secc-1.2.6.jar`
3. Then from the `ev1` xterm launch the EVCC using `cd ev1 && java -jar rise-v2g-evcc-1.2.6.jar` to launch the charging process

#### Instructions to simulate the attack:

On startup the the topology is as specified before, so `ev1` can recharge from `se1` and `ev2` from `se2`.

To launch the attack it is sufficient to use `attack1.sh` from the `dev1` terminal and `attack2.sh` from the `dev2` terminal. Then, `ev1` will connect to `se2` and `ev2` to `se1`. To try it, you can launch the right SECC and EVCC as depicted before.

To roll back to the legitimate behavior you can use again `attack1.sh` and `attack2.sh`.

___

#### References:

##### Bridging

Ref: https://wiki.archlinux.org/index.php/Network_bridge

Command for dev:  
1. `ip link add name e1s1 type bridge`
2. `ip link set e1s1 up`
3. `ip link set dev-eth1 master e1s1`
3. `ip link set dev-eth11 master e1s1`

`bridge link` to verify


#### TODO:
- ~~use two devices~~
- ~~only one file for the attack/normal~~
- implement TLS (on the simulator)
