import subprocess
import time
import os
# Replace with the path to your shell script
def script(b1, b2):
    script_path_0 = "./script/script0.sh"
    script_path_1 = "./script/script1.sh"
    script_path_2 = "./script/script2.sh"
    script_path_3 = "./script/script3.sh"
    script_path_4 = "./script/script4.sh"
    script_path_5 = "./script/script5.sh"
    script_path_6 = "./script/script6.sh"
    script_path_7 = "./script/script7.sh"
    script_path_8 = "./script/script8.sh"
    script_path_9 = "./script/script9.sh"
    script_path_10 = "./script/script10.sh"
    # Open a new terminal window and run the script
    SUDO_PASSWORD = "170823"
    sleep_time = 8
    command7 = (f'echo {SUDO_PASSWORD} | sudo -S stdbuf -oL ip netns exec ue1 iperf3 '
            f'-c 172.16.0.1 -p 5006 -i 1 -t 36000 -R -b {b1}M 2>&1 | '
            f'stdbuf -oL tee -a ~/ue1_data.log')

    # Full script to run in terminal
    script_path_7 = (f'rm -rf ~/ue1_data.log && {command7}')

    command8 = (f'echo {SUDO_PASSWORD} | sudo -S stdbuf -oL ip netns exec ue2 iperf3 '
            f'-c 172.16.0.1 -p 5020 -i 1 -t 36000 -R -b {b2}M 2>&1 | '
            f'stdbuf -oL tee -a ~/ue2_data.log')

    # Full script to run in terminal
    script_path_8 = (f'rm -rf ~/ue2_data.log && {command8}')



    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', script_path_0])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', script_path_1])
    time.sleep(sleep_time)

    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_2])
    time.sleep(sleep_time)

    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_3])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_4])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_5])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_6])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_7])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_8])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_9])
    time.sleep(sleep_time)
    subprocess.Popen(['gnome-terminal', '--', '/bin/bash', '-c', script_path_10])


# # Replace with the path to your shell script
# script_paths = [
#     "./script/script0.sh",
#     "./script/script1.sh",
#     "./script/script2.sh",
#     "./script/script3.sh",
#     "./script/script4.sh",
#     "./script/script5.sh",
#     "./script/script6.sh",
#     "./script/script7.sh",
#     "./script/script8.sh"
# ]

# # Function to run a script in gnome-terminal
# def run_script_in_terminal(script_path):
#     if os.path.isfile(script_path):
#         # Try to open a new terminal window and run the script
#         try:
#             subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'{script_path}; exec bash'])
#             print(f"Successfully started: {script_path}")
#         except Exception as e:
#             print(f"Failed to start {script_path}: {e}")
#     else:
#         print(f"Script not found: {script_path}")

# # Iterate over script paths and run each one
# for script_path in script_paths:
#     run_script_in_terminal(script_path)