#!/bin/bash

# Define your sudo password
SUDO_PASSWORD="170823"
SLEEPINT=30

# Navigate to the target directory
# cd ~/oaic/ss-xapp

# Make the script executable
# echo $SUDO_PASSWORD | sudo -S chmod +x zmqtwoue.sh

# # Execute the script
# echo $SUDO_PASSWORD | sudo -S ./zmqtwoue.sh

# sleep $SLEEPINT

cd ~/script
echo $SUDO_PASSWORD | sudo -S chmod +x only_create_env.sh

echo $SUDO_PASSWORD | sudo -S ./only_create_env.sh

sleep $SLEEPINT

echo $SUDO_PASSWORD | sudo -S chmod +x only_throttle_and_unthrottle.sh

echo $SUDO_PASSWORD | sudo -S ./only_throttle_and_unthrottle.sh