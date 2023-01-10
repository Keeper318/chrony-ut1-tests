# VM address: 192.168.122.55
# chrony in VM is started by "sudo ./chronyd -d"
# chrony on host is started by "sudo ./chronyd"
# chrony on host is stopped by "sudo ./chronyc shutdown"
# Monitoring is performed by "sudo ./chronyc ntpdata 192.168.122.55"
# chrony.conf in virtual machine:
#
# server 188.225.9.167 iburst
# server 91.207.136.55 iburst
# server 213.141.154.170 iburst
# server 91.209.94.10 iburst
# driftfile /var/lib/chrony/drift
# allow
# ut1 bulletina.csv
#
# chrony.conf on host machine:
#
# server 188.225.9.167 iburst
# server 91.207.136.55 iburst
# server 213.141.154.170 iburst
# server 91.209.94.10 iburst
# server 192.168.122.55 iburst noselect
# driftfile /var/lib/chrony/drift
import json
import os
import re
import sys
import time
from subprocess import call, check_output

JSON_FILE = "vm-test.json"
SAVE_EVERY_N_MEASUREMENTS = 20
SECS_BETWEEN_MEASUREMENTS = 3
MEASUREMENTS = 3600 // SECS_BETWEEN_MEASUREMENTS
VM_ADDRESS = "192.168.122.55"


def receive(index, expected_length):
    tokens = check_output(["./chronyc", "-c", "ntpdata", VM_ADDRESS], text=True).split(',')
    if len(tokens) != expected_length:
        print(check_output(["./chronyc", "-c", "ntpdata", VM_ADDRESS], text=True))
        print("Error: can't access virtual machine")
        exit(1)
    return tokens[index]


def save(offset_list):
    with open(JSON_FILE, "w") as file:
        json.dump(offset_list, file)
    print(f"Saved results to '{JSON_FILE}'")


if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        print("Error: linux system is required")
        exit(1)
    if os.getuid() != 0:
        print("Error: root privileges are required")
        exit(1)
    call("./chronyd")
    while True:
        if receive(7, 34) == "Server":
            print("VM is up!")
            break
        print("Waiting for VM data...")
        time.sleep(5)

    result = []
    try:
        for i in range(MEASUREMENTS):
            time.sleep(SECS_BETWEEN_MEASUREMENTS)
            offset = float(receive(18, 34))
            print("Offset:", offset)
            result.append(offset)
            if len(result) % SAVE_EVERY_N_MEASUREMENTS == 0:
                save(result)
        print("Finished!", end=' ')
    finally:
        save(result)
        call(["./chronyc", "shutdown"])
