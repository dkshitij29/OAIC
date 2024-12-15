#!/bin/bash

# Define your sudo password
SUDO_PASSWORD="170823"

# Export environment variables
export E2NODE_IP=$(hostname -I | cut -f1 -d' ')
export E2NODE_PORT=5006
export E2TERM_IP=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-e2term-sctp-alpha -o jsonpath='{.items[0].spec.clusterIP}')

# Run srsenb command with sudo
echo $SUDO_PASSWORD | sudo -S srsenb --enb.n_prb=100 --enb.name=enb1 --enb.enb_id=0x19B \
--rf.device_name=zmq --rf.device_args="fail_on_disconnect=true,tx_port=tcp://*:2000,rx_port=tcp://localhost:2009,id=enb,base_srate=23.04e6" \
--ric.agent.remote_ipv4_addr=${E2TERM_IP} --log.all_level=warn --ric.agent.log_level=debug --log.filename=stdout \
--ric.agent.local_ipv4_addr=${E2NODE_IP} --ric.agent.local_port=${E2NODE_PORT} --slicer.enable=1 --slicer.workshare=0