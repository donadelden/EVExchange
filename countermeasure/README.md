# Countermeasures against _EVExchange_

## `/distance_bounding`
The distance bounding protocol can be testbed using the two files `receiver_se.py` and `sender_ev.py`.

In particular, the first one must be run before inside the Supply Equipment which will start listing for packet request.
When running `sender_ev.py` from the vehicle, a simple handshake is used to exchange IP addresses.
Then, the fast pack exchange starts and a file is generated inside the `/results` folder.

#### Usage
While the receiver do not need any arguments, the sender needs one or more arguments:
- one argument which will be the filename for results

or you can generate a name based on the following information:
- `\<LNS|LDNP> <ac|g> distance [exponent] [variance]` 
