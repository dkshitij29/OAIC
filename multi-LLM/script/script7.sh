#!/bin/sh

#!/bin/bash

# Define your sudo password
SUDO_PASSWORD="170823"

# Run iperf3 command in ue1 network namespace
# echo $SUDO_PASSWORD | sudo -S ip netns exec ue1 iperf3 -c 172.16.0.1 -p 5006 -i 1 -t 36000 -R -b 40M
rm -rf ~/ue1_data.log
echo $SUDO_PASSWORD | sudo -S stdbuf -oL ip netns exec ue1 iperf3 -c 172.16.0.1 -p 5006 -i 1 -t 36000 -R -b 40M 2>&1 | stdbuf -oL tee -a ~/ue1_data.log
