#!/bin/bash

test=$(bridge link)
if [[ $test == *e1d2* ]];
then
  echo 'Turning down the malicious bridge...'
  # bridge between ev1 and dev2
  ip link set e1d2 down
  ip link set dev-eth1 nomaster
  ip link set dev-eth8 nomaster
  ip link delete name e1d2 type bridge

  # set up a bridge between dev2 and se1
  ip link set d2s1 down
  ip link set dev-eth6 nomaster #8
  ip link set dev-eth11 nomaster
  ip link delete name d2s1 type bridge

  echo 'Setting up the legitimate bridge...'
  ip link add name e1s1 type bridge
  ip link set e1s1 up
  ip link set dev-eth1 master e1s1
  ip link set dev-eth11 master e1s1

  echo 'Done, it is all normal.'

else
  echo 'Turning down the legitimate bridge...'
  ip link set e1s1 down
  ip link set dev-eth1 nomaster
  ip link set dev-eth11 nomaster
  ip link delete e1s1 type bridge

  echo 'Setting up the malicious bridge...'
  # bridge between ev1 and dev2
  ip link add name e1d2 type bridge
  ip link set e1d2 up
  ip link set dev-eth1 master e1d2
  ip link set dev-eth8 master e1d2

  # set up a bridge between dev2 and se1
  ip link add name d2s1 type bridge
  ip link set d2s1 up
  ip link set dev-eth6 master d2s1 #8
  ip link set dev-eth11 master d2s1

  echo 'Done, the attack is setted up.'

fi
