import pandas as pd
import csv
import numpy as np
from os import listdir
from os.path import isfile, join
from scipy import stats
import matplotlib.pyplot as plt

#Cleanup all data
def clean_data(data_in):
    data_out = np.array(data_in)
    z = np.abs(stats.zscore(data_out))
    z_th = 2
    while(np.max(z) > z_th):
        data_out = data_out[z<z_th]
        #print(data_out)
        z = np.abs(stats.zscore(data_out))
    return data_out

path_m1 = "./mode1/"
path_m4 = "./mode4/"
path_m5 = "./mode5/"
path_modes = [path_m1, path_m4, path_m5]
path_times = ["00_41/", "00_62/", "00_94/", "01_42/", "01_89/", "02_84/", "03_79/", "05_69/", "11_38/", "56_89/"]

dataset = []

for i in range(3):
    mode_i_data = []

    for j in range(10):
        curr_path = path_modes[i]+path_times[j]
        files = [f for f in listdir(curr_path) if isfile(join(curr_path, f))]

        mode_i_time_j_data = []

        for k in range(len(files)):
            mode_i_time_j_sta_k_data = []

            with open(curr_path+files[k], 'r') as data:
                for line in csv.reader(data):
                    # print(float(line[0]))
                    mode_i_time_j_sta_k_data.append(float(line[0]))
                    # print(type(mode_i_time_j_sta_k_data))
                    # print(len(mode_i_time_j_sta_k_data))

            mode_i_time_j_data.append(mode_i_time_j_sta_k_data)

        mode_i_data.append(list(mode_i_time_j_data))
    
    dataset.append(mode_i_data)

# How to use dataset:
# dataset[mode][time][sta][0] is a unique value
# dataset[mode][time][sta] is a list of lists of all related measurements from a station

# convert input dataset from list to numpy array
dataset_np = np.array(dataset, dtype=object)
# print(dataset_np[0,0,0][0])

#Calculate results
results = []
average = []
error_bar = []
for i in range(3):
    results_mode_i = []
    average_mode_i = []
    error_bar_mode_i = []
    for j in range(10):
        results_mode_i_time_j = []
        for k in range(32):
            # print(np.mean(dataset_np[i,j,k]))
            # results[i,j,k] = np.mean(dataset_np[i,j,k])
            results_mode_i_time_j.append(np.mean(dataset_np[i,j,k]))
        # print(results_mode_i_time_j)
        results_mode_i.append(results_mode_i_time_j)
        average_mode_i.append(np.mean(results_mode_i_time_j))
        error_bar_mode_i.append(np.std(results_mode_i_time_j))
    # print(results_mode_i)
    results.append(results_mode_i)
    average.append(average_mode_i)
    error_bar.append(error_bar_mode_i)

# print(len(results))
# print(average[0]) # 3 lists each with 10 values
# print(error_bar[0]) # 3 lists each with 10 values

# Normalize
tcp_speed = 80
average = np.array(average)/tcp_speed
error_bar = np.array(error_bar)/tcp_speed

#plotting
max_interval = np.array([0.41, 0.62, 0.94, 1.42, 1.89, 2.84, 3.79, 5.69, 11.38, 56.89])
filesize = 300000*8
PHYrate = 86700000
tx_time = filesize/PHYrate
x = 32*filesize / (max_interval/2 + tx_time) / (4*PHYrate)
x = 100*x
print(x[0:7])

fig, ax = plt.subplots()
i = 7
ax.errorbar(x[0:i], average[0][0:i], yerr=error_bar[0][0:i])
ax.errorbar(x[0:i], average[1][0:i], yerr=error_bar[1][0:i])
ax.errorbar(x[0:i], average[2][0:i], yerr=error_bar[2][0:i])
ax.legend(['SU','MU-Reports','MU-Genie'])
ax.set(xlim=(0, 100), ylim=(0, 0.6))
ax.grid(color='k', linestyle='--', linewidth=1)
plt.title("Average TCP Download throughput of a 300kB file - 32 stations")
plt.xlabel('Aggregate traffic load in network, in % [Normalized by MIMO PHY rate]') 
plt.ylabel('Measured TCP Throughput for downloads\n[Normalized by the TCP speed test result]') 
plt.savefig('TCP-Throughput-Downloads-32sta.png')

fig2, ax2 = plt.subplots()
ax2.plot(x[0:i], 100*(average[1][0:i] / average[0][0:i] - 1), '*-', color='tab:orange')
ax2.plot(x[0:i], 100*(average[2][0:i] / average[0][0:i] - 1), '*-', color='tab:green')
ax2.legend(['MU-Reports / SU','MU-Genie / SU'])
ax2.set(xlim=(0, 100), ylim=(0, 70))
ax2.grid(color='k', linestyle='--', linewidth=1)
plt.title("Relative Gain of the 2 MU modes over the SU Uplink")
plt.xlabel('Aggregate traffic load in network, in % [Normalized by MIMO PHY rate]') 
plt.ylabel('Gain in Throughput for TCP downloads, in %') 
plt.savefig('MU-gains.png')
