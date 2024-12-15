#!/bin/sh
# echo 170823 | sudo -S ip netns add ue1
# echo 170823 | sudo -S ip netns add ue2
# echo 170823 | sudo -S ip netns list
# echo 170823 | sudo -S srsepc

#!/bin/bash

# Define your sudo password
SUDO_PASSWORD="170823"

# Add UEs to Network Namespace
echo $SUDO_PASSWORD | sudo -S ip netns add ue1
echo $SUDO_PASSWORD | sudo -S ip netns add ue2

# List Network Namespaces
echo $SUDO_PASSWORD | sudo -S ip netns list

# Start Core Network
echo $SUDO_PASSWORD | sudo -S srsepc
