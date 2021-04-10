import subprocess
import json

def run_iperf(server_ip, filesize):
    return subprocess.check_output(["iperf3", "-c", server_ip, "-J", "-M 1460", "-n "+str(filesize)])

json_out = run_iperf("192.168.0.102", 146000)

def extract_bps(json_out):
    dict_out = json.loads(json_out)
    return dict_out["end"]["streams"][0]["receiver"]["bits_per_second"]

mbps_out = extract_bps(json_out)/1024/1024
print(mbps_out)
