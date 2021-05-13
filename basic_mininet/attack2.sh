#!/bin/bash

test=$(bridge link)
if [[ $test == *d1s2* ]];
then
  echo 'Turning down the malicious bridge...'
  # bridge between dev1 and se2
  ip link set d1s2 down
  ip link set dev-eth9 nomaster
  ip link set dev-eth12 nomaster
  ip link delete name d1s2 type bridge

  # set up a bridge between ev2 and dev1
  ip link set e2d1 down
  ip link set dev-eth7 nomaster #9
  ip link set dev-eth2 nomaster
  ip link delete name e2d1 type bridge

  echo 'Setting up the legitimate bridge...'
  ip link add name e2s2 type bridge
  ip link set e2s2 up
  ip link set dev-eth2 master e2s2
  ip link set dev-eth12 master e2s2

  echo 'Done, it is all normal.'

else
  echo 'Turning down the legitimate bridge...'
  ip link set e2s2 down
  ip link set dev-eth2 nomaster
  ip link set dev-eth12 nomaster
  ip link delete e2s2 type bridge

  echo 'Setting up the malicious bridge...'
  # bridge between dev1 and se2
  ip link add name d1s2 type bridge
  ip link set d1s2 up
  ip link set dev-eth9 master d1s2
  ip link set dev-eth12 master d1s2

  # set up a bridge between ev2 and dev1
  ip link add name e2d1 type bridge
  ip link set e2d1 up
  ip link set dev-eth7 master e2d1 #9
  ip link set dev-eth2 master e2d1

  echo 'Done, the attack is setted up.'

fi
