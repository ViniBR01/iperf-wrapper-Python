import subprocess
import json

json_out = subprocess.check_output(["iperf3", "-c", "192.168.0.102", "-M 1460", "-n 146000", "-J"])

dict_out = json.loads(json_out)
bps_out = dict_out["end"]["streams"][0]["receiver"]["bits_per_second"]
print(bps_out/1024/1024)
