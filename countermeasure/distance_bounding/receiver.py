import string
import time
import socket
import random


def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


port = 5005

# Create a UDP socket
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ("::", port, 0, 2)
s.bind(server_address)

TRIES = 102
DATA_SIZE = 1

count = 0
# always listening (skip the first delta ;) )
while True:
    print("####### Receiver is listening #######")
    data_to_be_sent = get_random_string(TRIES * DATA_SIZE)
    s_se = b""

    for i in range(0, TRIES):
        # retrieve the data to be sent
        to_be_sent = data_to_be_sent[i * DATA_SIZE:(i + 1) * DATA_SIZE].encode()

        # rapid exchange
        start = time.time()
        data, address = s.recvfrom(4)
        s.sendto(to_be_sent, address)
        end = time.time()

        # create the final string
        s_se += data + to_be_sent

    # send the final string
    s.sendto(s_se, address)


s.close()
