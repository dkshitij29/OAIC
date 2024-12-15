#!/bin/bash

# Define your sudo password
SUDO_PASSWORD="170823"

# Run iperf3 command in ue2 network namespace
# echo $SUDO_PASSWORD | sudo -S ip netns exec ue2 iperf3 -c 172.16.0.1 -p 5020 -i 1 -t 36000 -R -b 10M
rm -rf ~/ue2_data.logs
echo $SUDO_PASSWORD | sudo -S stdbuf -oL ip netns exec ue2 iperf3 -c 172.16.0.1 -p 5020 -i 1 -t 36000 -R -b 10M 2>&1 | stdbuf -oL tee -a ~/ue2_data.log