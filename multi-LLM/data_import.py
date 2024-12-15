import streamlit as st
import os
# from utils import UpdateMaliciousBandwidthValue, UpdateUsersDatabase, KillProcess, PreProcessLogFile
import time
import subprocess
import stat
import matplotlib.pyplot as plt
from utils import read_user_data
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


SecureSlicingDeploymentTime = 20

try:
    st.markdown("""
        <style>
            body {
                background-color: #ffffff;
                color: #d9534f;
            }
            .stButton>button {
                background-color: #d9534f;
                color: white;
                border-radius: 8px;
                border: 1px solid #d43f3a;
                margin: auto; /* Center the buttons */
                width: 50%; /* Match the layout width */
                display: block;
                text-align: center;
            }
            .stButton>button:hover {
                background-color: #c9302c;
            }
            .custom-title {
                font-size: 36px;
                color: #d9534f;
                text-align: center;
                margin-bottom: 20px;
            }
            .custom-subtitle {
                font-size: 24px;
                color: #d9534f;
                text-align: center;
                margin-top: 30px;
            }
            .custom-description {
                font-size: 18px;
                color: #555555;
                text-align: justify;
                margin: 20px auto;
                line-height: 1.8;
                width: 75%;
            }
            .highlight {
                color: #d9534f;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        st.markdown("<div class='custom-title'>OAIC Made Easy</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='custom-description'>
        Welcome to <span class='highlight'>OAIC Made Easy</span>. This platform simplifies the exploration of deployed xAPPs in the context 
        of developing Artificial Intelligence models for 5G networks within the O-RAN ecosystem. Users can 
        seamlessly test and interact with these xAPPs in just a few clicks, bypassing the complexities of 
        installation and setup associated with OAIC.
    
        This initiative was developed by <span class='highlight'>Dhia Neifar</span> and <span class='highlight'>Xing Wu</span> as part of the <span class='highlight'>EC 528</span> course project.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='custom-subtitle'>Available xApps</div>", unsafe_allow_html=True)

        xapps = ["Secure Slicing", "Traffic Monitoring", "Resource Allocation", "Fault Detection"]
        for xapp in xapps:
            if st.button(xapp, key=xapp):
                if xapp == "Secure Slicing":
                    st.session_state.page = "Secure Slicing"

    if st.session_state.page == "Secure Slicing":
        st.markdown("<div class='custom-title'>Secure Slicing</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='custom-description'>
        This page is dedicated to exploring and configuring secure slicing features in the O-RAN ecosystem.
        Use this tool to manage and test secure slicing functionalities for 5G networks.
        </div>
        """, unsafe_allow_html=True)

        num_users = st.number_input("Enter the number of users (1 to 5):",
                                    min_value=1, max_value=5, value=1, step=1)
        bandwidthlist=[]

        users = {}
        amf_values = ['9001', '8000', '8002', '8003', '8004']
        imsi_values = ['001010123456789', '001010123456780', '001010123456781', '001010123456782', '001010123456783']
        sqn_values = ['000000001656', '000000001590', '000000001488', '000000001446', '000000001467']
        bandwidth_values = ['40', '10']
        for user_id in range(1, num_users + 1):
            st.markdown(f"### User {user_id}")
            name = st.text_input(f"Name (User {user_id}):", value=f"ue{user_id}")
            auth_imsi = st.text_input(f"Auth IMSI (User {user_id}):", value="xor")
            imsi = st.text_input(f"IMSI (User {user_id}):", value=imsi_values[user_id - 1])
            key = st.text_input(f"Key (User {user_id}):", value="00112233445566778899aabbccddeeff")
            op_type = st.text_input(f"OP Type (User {user_id}):", value="opc")
            op_opc = st.text_input(f"OP/OPc (User {user_id}):", value="63bfa50ee6523365ff14c1f45f88737d")
            amf = st.text_input(f"AMF (User {user_id}):", value=amf_values[user_id - 1])
            sqn = st.text_input(f"SQN (User {user_id}):", value=sqn_values[user_id - 1])
            qci = st.text_input(f"QCI (User {user_id}):", value="7")
            ip_alloc = st.text_input(f"IP Alloc (User {user_id}):", value="dynamic")
            time_period = st.text_input(f"Time Period (User {user_id}):", value="36000")
            bandwidth_request = st.text_input(f"Bandwidth Request in Mbps (User {user_id}):", value=bandwidth_values[user_id - 1])
            bandwidthlist.append(bandwidth_request)

            users[name] = {'auth_imsi': auth_imsi, 'imsi': imsi, 'key': key, 'op_type': op_type, 'op_opc': op_opc,
                           'amf': amf, 'sqn': sqn, 'qci': qci, 'ip_alloc': ip_alloc, 'time_period': time_period,
                           'bandwidth_request': bandwidth_request}
        st.markdown("<div class='custom-title'>Global Variables</div>", unsafe_allow_html=True)
        malicious_threshold = st.text_input(f"Malicious Threshold in Mbps:", value="20")


        if st.button("Submit", key="Submit"):
            # UpdateMaliciousBandwidthValue(malicious_threshold)
            # UpdateUsersDatabase(users)
            st.success("User data submitted successfully!")
            script(bandwidthlist[0], bandwidthlist[1])

            # placeholder = st.empty()
            # Message = "Setting up 5G Network..."
            # placeholder.markdown(f"<p style='color:gray; font-size:12px;'>{Message}</p>", unsafe_allow_html=True)
            # time.sleep(SleepingTime)

            # placeholder = st.empty()
            # Message = "Checking RIC State..."
            # placeholder.markdown(f"<p style='color:gray; font-size:12px;'>{Message}</p>", unsafe_allow_html=True)
            # time.sleep(SleepingTime)

            # for user in range(1, num_users + 1):
            #     placeholder = st.empty()
            #     user_id = f"ue{user}"
            #     UserData = users[user_id]
            #     Message = f"Setting up user {user_id}..."
            #     placeholder.markdown(f"<p style='color:gray; font-size:12px;'>{Message}</p>", unsafe_allow_html=True)
            #     time.sleep(SleepingTime)
            
            # placeholder = st.empty()
            # Message = "Running Python Script..."
            # placeholder.markdown(f"<p style='color:gray; font-size:12px;'>{Message}</p>", unsafe_allow_html=True)
            # time.sleep(SleepingTime)

            # placeholder = st.empty()
            # Message = "Measuring Network Performance on Server Side..."
            # placeholder.markdown(f"<p style='color:gray; font-size:12px;'>{Message}</p>", unsafe_allow_html=True)
            # for user in range(1, num_users + 1):
            #     placeholder = st.empty()
            #     user_id = f"ue{user}"
            #     Message = f"Setting up Server side for user {user_id}..."
            #     placeholder.markdown(f"<p style='color:gray; font-size:8px;'>{Message}</p>", unsafe_allow_html=True)
            #     time.sleep(SleepingTime)

            # placeholder = st.empty()
            # Message = "Measuring Network Performance on Client Side..."
            # placeholder.markdown(f"<p style='color:gray; font-size:12px;'>{Message}</p>", unsafe_allow_html=True)
            # for user in range(1, num_users + 1):
            #     placeholder = st.empty()
            #     user_id = f"ue{user}"
            #     Message = f"Setting up Client side for user {user_id}..."
            #     placeholder.markdown(f"<p style='color:gray; font-size:8px;'>{Message}</p>", unsafe_allow_html=True)
            #     time.sleep(SleepingTime)




            time.sleep(4)
            START = time.time()
            DataLength = None
            SecureSlicingVerticalX = None
            MaxValue = None
            MinValue = None
            FirstTime = False
            Message = "Plotting BitRate For Users..."
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
                while True:
                    ax.clear()
                    max_ = [0, 0]
                    min_ = [0, 0]
                    DataLengths = [0, 0]
                    for user in range(1, num_users + 1):
                        user_id = f"ue{user}"
                        log_file = os.path.join('/home/xingqi/', f"{user_id}_data.log")
                        data = read_user_data(log_file)
                        
                        DataLengths[user - 1] = len(data)
                        max_[user - 1] = max(data)
                        min_[user - 1] = min(data)
                        if data:
                            ax.plot(range(len(data)), data, label=f"User {user_id}")
                    if time.time() - START > SecureSlicingDeploymentTime and not FirstTime:
                        FirstTime = True
                        SecureSlicingVerticalX = min(DataLengths)
                    if FirstTime:
                        MaxValue = max(max_)
                        MinValue = min(min_)
                        ax.plot([SecureSlicingVerticalX, SecureSlicingVerticalX], [MinValue, MaxValue], marker='o', color='red', label="Secure Slicing Deployed!")
                    ax.set_title("Live Data Visualization")
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel("Value")
                    ax.legend()
                    placeholder.pyplot(fig)
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Killing Processes")



        if st.button("Back to Main Page", key="Return Main Page"):
            print("Killing Processes")
            # for process in Processes:
            #     KillProcess(process)
            st.session_state.page = "main"
except KeyboardInterrupt:
    print("Killing Processes")
    # for process in Processes:
    #     KillProcess(process)
