import time
import socket
import numpy as np
import random
import string
import os.path
import sys


def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


ITERATIONS = 1000

for _ in range(0, ITERATIONS):

    port = 5005

    # get socket info
    address = [addr for addr in socket.getaddrinfo("::", None) if socket.AF_INET6 == addr[0]]

    # Create socket for server
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, 0)
    s.bind(address[0][-1])
    print("Sending hello message...")

    s.sendto(bytes("Ehy! I wanna start DB protocol! Are you up, SE?", "utf-8"), ("ff02::1", port, 2, 0))

    print("Waiting for response...")
    data = ""
    while data != b"Ok! Here I am!":
        data, addr = s.recvfrom(1024)

    print("Got the address!")
    print("Starting...")
    total_start = time.time()
    deltas = []

    TRIES = 102
    DATA_SIZE = 1

    data_to_be_sent = get_random_string(TRIES * DATA_SIZE)
    s_ev = b""

    # Let's send data through UDP protocol
    for i in range(0, TRIES):
        # retrieve the data to be sent
        to_be_sent = data_to_be_sent[i * DATA_SIZE:(i + 1) * DATA_SIZE].encode()

        # rapid exchange
        start = time.time()
        s.sendto(to_be_sent, addr)
        data, _ = s.recvfrom(4)
        end = time.time()

        # create the final string
        s_ev += to_be_sent + data
        deltas.append(end - start)

    # receive the string and check the correctness
    s_se, _ = s.recvfrom(2024)
    assert s_se == s_ev

    # close the socket
    s.close()

    mu = np.mean(deltas[1:-1])
    std = np.std(deltas[1:-1])
    var = np.var(deltas[1:-1])
    elapsed = time.time() - total_start
    print(f"t: {elapsed}")
    print(mu)
    print(std)

    BASE_PATH = "results_2/"
    # PROP MODE DIST EXP
    if sys.argv[1] == "LNS":
        filename = BASE_PATH + f"attack-dist{sys.argv[3]}-exp{sys.argv[4]}-var{sys.argv[5]}-{sys.argv[1]}-{sys.argv[2]}.csv"
    elif sys.argv[1] == "LDPL":
        filename = BASE_PATH + f"attack-dist{sys.argv[3]}-exp{sys.argv[4]}-{sys.argv[1]}-{sys.argv[2]}.csv"
    else:
        filename = BASE_PATH + f"{sys.argv[1]}.csv"
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            f.write("mean,std,variance,time_elapsed\n")

    with open(filename, "a") as f:
        f.write(f"{mu},{std},{var},{elapsed}\n")

    time.sleep(0.3)
