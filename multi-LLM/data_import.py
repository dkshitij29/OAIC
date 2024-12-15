import data_import as st
import os
# from utils import UpdateMaliciousBandwidthValue, UpdateUsersDatabase, KillProcess, PreProcessLogFile
import time
import subprocess
import stat
import matplotlib.pyplot as plt
# from utils import read_user_data
from test import script
import re

SleepingTime = 2.5
Processes = []
TMP_PATH = "/tmp/"

def read_user_data(file_path):
    """Read generated data from a log file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = f.readlines()
        bitrate_pattern1 = r'(\d+\.\d+|\d+) Mbits/sec'
        bitrate_pattern2 = r'(\d+\.\d+|\d+) bits/sec'

        bitrate_values = []
        for line in data:
            matches1 = re.findall(bitrate_pattern1, line)
            matches2 = re.findall(bitrate_pattern2, line)
            matches=matches1+matches2
            if matches:
                matches = [float(match) for match in matches]
                bitrate_values.extend(matches)
        return bitrate_values
    return []




def get_data_rate():

    # script(40, 10)


    # time.sleep(4)
    # START = time.time()
    num_users=2
    # DataLength = None
    # SecureSlicingVerticalX = None
    # MaxValue = None
    # MinValue = None
    # FirstTime = False
    # Message = "Plotting BitRate For Users..."
    # placeholder.markdown(f"<p style='color:gray; font-size:20px;'>{Message}</p>", unsafe_allow_html=True)
    log_files = []
    # Start subprocesses
    for user in range(1, num_users + 1):
        user_id = f"ue{user}"
        # log_file = os.path.join(TMP_PATH, f"{user_id}_data.log")
        log_file = os.path.join(os.getcwd(), f"{user_id}_data.log")
        log_files.append(log_file)

    fig, ax = plt.subplots()
    placeholder = st.empty()
    try:
        # while True:
            UE_DATA_RATE=[]
            # ax.clear()
            max_ = [0, 0]
            min_ = [0, 0]
            DataLengths = [0, 0]
            for user in range(1, num_users + 1):
                user_id = f"ue{user}"
                log_file = os.path.join('~/', f"{user_id}_data.log")
                data = read_user_data(log_file)
                UE_DATA_RATE.append(data)
                # DataLengths[user - 1] = len(data)
                # max_[user - 1] = max(data)
                # min_[user - 1] = min(data)
                # if data:
                    # ax.plot(range(len(data)), data, label=f"User {user_id}")

            # ax.set_title("Live Data Visualization")
            # ax.set_xlabel("Time (s)")
            # ax.set_ylabel("Value")
            # ax.legend()
                #  time.sleep(1)
            return UE_DATA_RATE
    except KeyboardInterrupt:
        print("Killing Processes")




