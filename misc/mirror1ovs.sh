# https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/


# create a bridge to a dummy





# create the mirroring
ovs-vsctl \
  -- --id=@m create mirror name=mymirror \
  -- add bridge ovsbr0 mirrors @m \
  -- --id=@eth0 get port sta1-eth0 \
  -- --id=@eth1 get port sta1-eth1 \
  -- set mirror mymirror 'select_src_port=[@eth0,@eth1]' 'select_dst_port=[@eth0,@eth1]' \
  -- --id=@wlan get port sta1-wlan0 \
  -- set mirror mymirror output-port=@wlan
