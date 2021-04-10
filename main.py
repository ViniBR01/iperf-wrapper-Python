import subprocess
import json
import time
import random
import sys, getopt

def run_iperf(server_ip, filesize):
    return subprocess.check_output(["iperf3", "-c", server_ip, "-J", "-M 1460", "-n "+str(filesize)])

def extract_bps(json_out):
    dict_out = json.loads(json_out)
    return dict_out["end"]["streams"][0]["receiver"]["bits_per_second"]

def get_interval(min_interval, max_interval):
    return random.random()*(max_interval - min_interval) + min_interval

def main(argv):
    size = 100000
    min_interval = 0.5
    max_interval = 1.5
    t_end = time.time() + 10
    server_ip = "192.168.0.102"

    while time.time() < t_end:
        interval = get_interval(min_interval, max_interval)
        time.sleep(interval)
        json_out = run_iperf(server_ip, size)
        mbps_out = extract_bps(json_out)/1024/1024
        print(mbps_out)

if __name__ == "__main__":
    main(sys.argv[1:])