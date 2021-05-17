# Activate Bridges on sta1

test=$(ip link)
if [[ $test == *vxlan0* ]];
then 
	echo 'Removing qdisc and vxlans'
	################ remove ev1
	tc qdisc del dev sta1-eth1 ingress

	tc qdisc del dev vxlan0 ingress

	ip link del vxlan0


	################ remove se1
	tc qdisc del dev sta1-eth2 ingress

	tc qdisc del dev vxlan1 ingress

	ip link del vxlan1

fi

echo 'Setting up the legitimate bridge...'
ip link add name e1s1 type bridge
ip link set e1s1 up
ip link set sta1-eth1 master e1s1
ip link set sta1-eth2 master e1s1

echo 'Done, it is all normal.'