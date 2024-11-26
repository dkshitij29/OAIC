import numpy as np; np.random.seed(1)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
from scipy.io import loadmat
from scipy import stats
import os
import csv

def smooth_data(data, n):
    """
    Calculate the smoothed reward and smoothed variation (standard deviation)
    over every `n` steps from the given reward data array using a sliding window.

    Parameters:
        data (np.ndarray): Array of reward data.
        n (int): Number of steps to smooth over.

    Returns:
        smoothed_rewards (np.ndarray): Array of smoothed rewards (with the same length as input data).
        smoothed_variations (np.ndarray): Array of smoothed variations (standard deviation) (with the same length as input data).
    """
    if n <= 0:
        raise ValueError("The smoothing step n must be greater than 0.")
    
    # Length of the original data
    data_len = len(data)
    
    # Initialize arrays for storing smoothed values
    smoothed_rewards = np.zeros(data_len)
    smoothed_variations = np.zeros(data_len)
    
    # Pad the data to handle boundaries smoothly
    # padded_data = np.pad(data, (n//2, n-n//2-1), mode='mean')
    padded_data = np.pad(data, (n//2, 0), mode='minimum')
    padded_data = np.pad(data, (0, n-n//2-1), 'constant', constant_values=(np.mean(data[data_len-(n-n//2-1):])))
    # Calculate rolling mean and standard deviation
    for i in range(data_len):
        window = padded_data[i:i+n]
        smoothed_rewards[i] = np.mean(window)
        smoothed_variations[i] = np.std(window)
    
    return smoothed_rewards, smoothed_variations

def read_csv_files_from_folder_to_numpy(folder_path, filename):
    # List for storing csv data temporarily
    data_list = []

    file_path = os.path.join(folder_path, filename)
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # Reading the contents of the CSV file and appending to the list
        for row in csv_reader:
            data_list.append(row)

# Convert the list to a NumPy array
    data_array = np.array(data_list)
    
    return data_array

# Resource_capacity = [*range(250,850,50)]
# Resource_capacity = [*range(200,1100,100)]

# # Resource_capacity.append(900)
# Evaluation_test_list=[]
# Evaluation_test_no_adm_list=[]
# Evaluation_test_rand_list=[]
# Evaluation_test_static_list=[]
# Evaluation_test_base_list=[]

# for resource_capacity in Resource_capacity:
    # Define the path to the 'train' folder
# train_folder_path_base = 'resource'+str(resource_capacity)+"-b"
train_folder_path_test = 'test'
# train_folder_path_test_no_adm = 'resource'+str(resource_capacity)+'_no_adm'
# train_folder_path_rand= 'resource'+str(resource_capacity)+'_no_adm_rand'
# train_folder_path_static = 'resource'+str(resource_capacity)+'_no_adm_static'

# filename_base = 'delay_violation_rate_test.csv'     
filename_test = 'resource_allocation_test.csv'     
# filename_rand = 'delay_violation_rate_rand.csv'     
# filename_static = 'delay_violation_rate_static.csv'     
# filename_no_admin = 'delay_violation_rate_no_admin.csv'     

# Reading CSV data and converting to NumPy array
delay_violation_numpy_array_test = read_csv_files_from_folder_to_numpy(train_folder_path_test, filename_test)
delay_violation_numpy_array_test=delay_violation_numpy_array_test.astype(np.float32)


# Example data
time=np.array([*range(delay_violation_numpy_array_test.shape[0])])
data_rate_UE1=delay_violation_numpy_array_test[:,0]
data_rate_UE2=delay_violation_numpy_array_test[:,1]
data_rate_r_UE1=delay_violation_numpy_array_test[:,2]
data_rate_r_UE2=delay_violation_numpy_array_test[:,3]
# Plot with Seaborn
# sns.set(style="darkgrid")
plt.figure(figsize=(12.5, 9))
# Plot smoothed reward function
plt.plot(time,data_rate_UE1, '--b', markersize=15,linewidth=3,label='UE1 (Priority UE) measurement')
plt.plot(time,data_rate_UE2, 'c--', markersize=15,linewidth=3,label='UE2 measurement')
plt.plot(time,data_rate_r_UE1, 'r--', markersize=15,linewidth=3,label='UE1 (Priority UE) request')
plt.plot(time,data_rate_r_UE2, 'm--', markersize=15,linewidth=3,label='UE2 request')
# plt.plot(time,Evaluation_test_base_list, 'g>--', markersize=15,linewidth=3,label='Baseline (SARA)')


# plt.title('')
plt.xlabel('Time (s)', fontsize=38, labelpad=-4)
plt.ylabel('Mbps', fontsize=38, labelpad=6)
# plt.title('Average Delay Violation Rates')
# plt.xlim((0,epochs.shape[0]))
plt.grid()
# plt.title('pkt_drop during The training')
lgd=plt.legend(fontsize=28,loc='upper right')
plt.xticks(fontsize=28)
plt.yticks(fontsize=28)
lgd.get_frame().set_alpha(0)
plt.ylim((0,65))

plt.show()

