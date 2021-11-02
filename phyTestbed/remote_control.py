"""
Tool to remote start and configure devices
"""
import argparse
import subprocess
import sys
import json
import time
import multiprocessing

# IPs
with open("config.json") as f:
    config = json.load(f)

if config:
    ev1_ip = config["ev1"]
    ev2_ip = config["ev2"]
    se1_ip = config["se1"]
    se2_ip = config["se2"]
    dev1_ip = config["dev1"]
    dev2_ip = config["dev2"]
else:
    print("Error in config.json")
    exit(1)

names = {
    ev1_ip : "ev1",
    ev2_ip : "ev2",
    se1_ip : "se1",
    se2_ip : "se2",
    dev1_ip : "dev1",
    dev2_ip : "dev2"
}

# other config
ssh_key = "/home/denis/.ssh/raspberry"
user = "pi"
base = "/home/pi/EVExchange/phyTestbed/"


def exec_command(address, command):
    """
    Wrapper to exec commands in a certain Raspberry
    @param address: ip address
    @param command: command to be executed as a string
    @return: stdout of the result
    """
    sess = subprocess.Popen(["ssh", f"pi@{address}", command], shell=False, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    result = sess.stdout.readlines()
    #if not result:
    error = sess.stderr.readlines()
    if error:
        print(f"ERROR: {error}", file=sys.stderr)
    #return None
    #else:
    return result


def _async_cmd(address, command):
    """
    Wrapper to exec commands in a certain Raspberry and print the results asyncronously
    """
    sess = subprocess.Popen(["ssh", f"pi@{address}", command], shell=False,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=2)

    while sess.poll() is None:
        line = sess.stdout.readline()
        if line:
            print(f"{names[address]}: {line.decode('utf-8')[:-1]}")
    sess.wait()


def exec_command_async(address, command):
    return multiprocessing.Process(target=_async_cmd, args=(address, command)).start()


def pprint(results, dev_name):
    for i in results:
        print(f"{dev_name}: {i.decode('utf-8')[:-1]}")


def toggle_attack():
    get_ip_address_cmd = "ip addr show wlan0 | awk  '/inet /{print $2}' | awk -F/ '{print $1}'"

    s1_wlan0_ip = exec_command(dev1_ip, get_ip_address_cmd)[0].decode("utf-8")[:-1]
    s2_wlan0_ip = exec_command(dev2_ip, get_ip_address_cmd)[0].decode("utf-8")[:-1]
    #print(f"1: {s1_wlan0_ip} , 2:{s2_wlan0_ip}")

    res = exec_command(dev1_ip, f"sudo {base}configurations/toggle_attack.sh {s2_wlan0_ip} 1")
    pprint(res, names[dev1_ip])
    res = exec_command(dev2_ip, f"sudo {base}configurations/toggle_attack.sh {s1_wlan0_ip} 2")
    pprint(res, names[dev2_ip])


def is_attack_active():
    res_dev1 = str(exec_command(dev1_ip, "ip addr"))
    if "vxlan" in res_dev1:
        return True
    elif "legBridge" in res_dev1:
        return False
    else:
        print("Error: have you initialized the attack/legitimate bridge?")
        return None


def start_SEs(verbose=False):
    v = " -v" if verbose else ""
    exec_command_async(se1_ip, f"cd {base}/indicators/RiseV2G/; python3 start.py se{v}")
    exec_command_async(se2_ip, f"cd {base}/indicators/RiseV2G/; python3 start.py se{v}")


def start_charge(device_ip, verbose=False):
    v = " -v" if verbose else ""
    if "ev" in names[device_ip]:
        exec_command(device_ip, f"cd {base}/indicators/RiseV2G/; python3 start.py ev{v}")
    elif "se" in names[device_ip]:
        exec_command(device_ip, f"cd {base}/indicators/RiseV2G/; python3 start.py se{v}")
    else:
        print("Check the IP!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=
    """Remote Controller for EVExchange experiment.
    toggle: init/start/stop attack
    startSEs: start all the charging columns
    ev1/2 or se1/2: start a particular device""")
    parser.add_argument('command', type=str, choices=["toggle", "startSEs", "ev1", "ev2", "se1", "se2", "cmd"],
                        help='')
    parser.add_argument('-v', '--verbose',  dest='verbose', action='store_const',
                        const=True, default=False,
                        help='Print the log of RiseV2G (default: False)')

    args = parser.parse_args()
    verbose = args.verbose
    cmd = args.command

    if cmd == "toggle":
        toggle_attack()
    elif cmd == "startSEs":
        start_SEs(verbose)
    elif cmd in ["ev1", "ev2", "se1", "se2"]:
        start_charge(config[cmd], verbose)
    elif cmd == "cmd":
        command_for_everyone = "cd ~/EVExchange && git checkout * && git pull origin phyTestbed"
        #command_for_everyone = "sudo shutdown now"
        for i in names.keys():  # for each IP
            print(f"{names[i]} to be done...")
            exec_command(address=i, command=command_for_everyone)
            print(f"{names[i]} done.")
    else:
        print("Error")
        exit(1)