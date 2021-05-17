# Activate Bridges on sta2

test=$(ip link)
if [[ $test == *vxlan0* ]];
then 
	echo 'Removing qdisc and vxlans'
	################ remove ev2
	tc qdisc del dev sta2-eth1 ingress

	tc qdisc del dev vxlan0 ingress

	ip link del vxlan0 


	################ remove se2
	tc qdisc del dev sta2-eth2 ingress

	tc qdisc del dev vxlan1 ingress

	ip link del vxlan1 

fi

echo 'Setting up the legitimate bridge...'
ip link add name e2s2 type bridge
ip link set e2s2 up
ip link set sta2-eth1 master e2s2
ip link set sta2-eth2 master e2s2

echo 'Done, it is all normal.'