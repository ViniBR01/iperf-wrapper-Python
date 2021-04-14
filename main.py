import subprocess
import json
import time
import random
import sys, getopt

def run_iperf_DL(server_ip, filesize):
    return subprocess.check_output(["iperf3", "-c", server_ip, "-J", "-M 1460", "-n "+str(filesize)])

def run_iperf_UL(server_ip, filesize):
    return subprocess.check_output(["iperf3", "-c", server_ip, "-J", "-M 1460", "-n "+str(filesize), "-R"])

def extract_bps(json_out):
    dict_out = json.loads(json_out)
    return dict_out["end"]["streams"][0]["receiver"]["bits_per_second"]

def get_interval(min_interval, max_interval):
    return random.random()*(max_interval - min_interval) + min_interval

def main(argv):
    size = 500000 #bytes
    min_interval = 0.0 #seconds
    max_interval = 1.5 #seconds
    t_end = time.time() + 10
    server_ip = "192.168.0.102"
    upload_ratio = 0

    usage_str = 'main.py -i <server-ip> -f <file-size> -l <time-length> -t <max-interval> -g <min-interval> -m <ratio-of-uploads>'
    
    try:
        opts, args = getopt.getopt(argv,"hf:l:i:t:g:m:",["file-size=","length=","server-ip=","max-interval=","min-interval="])
    except getopt.GetoptError:
        print(usage_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage_str)
            sys.exit()
        elif opt in ("-f", "--file-size"):
            size = int(arg)
        elif opt in ("-l", "--length"):
            t_end = time.time() + int(arg)
        elif opt in ("-t", "--max-interval"):
            max_interval = float(arg)
        elif opt in ("-g", "--min-interval"):
            min_interval = float(arg)
        elif opt in ("-i", "--server-ip"):
            server_ip = arg
        elif opt in ("-i", "--server-ip"):
            upload_ratio = int(arg)

    if (upload_ratio == 0):
        while time.time() < t_end:
            interval = get_interval(min_interval, max_interval)
            time.sleep(interval)
            try:
                json_out = run_iperf_DL(server_ip, size)
            except:
                continue
            else:
                mbps_out = extract_bps(json_out)/1024/1024
                print(mbps_out)

    elif (upload_ratio == 1):
        while time.time() < t_end:
            interval = get_interval(min_interval, max_interval)
            time.sleep(interval)
            try:
                json_out = run_iperf_UL(server_ip, size)
            except:
                continue
            else:
                mbps_out = extract_bps(json_out)/1024/1024
                print(mbps_out)
    
    else:
        print("Mixed Traffic is not coded yet.")
        pass

if __name__ == "__main__":
    main(sys.argv[1:])