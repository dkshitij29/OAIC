#!/bin/sh

SLEEPINT=10;

echo "Starting the script..."
echo "Fetching the SS_XAPP service IP..."

export SS_XAPP=`kubectl get svc -n ricxapp --field-selector metadata.name=service-ricxapp-ss-rmr -o jsonpath='{.items[0].spec.clusterIP}'`
if [ -z "$SS_XAPP" ]; then
    export SS_XAPP=`kubectl get svc -n ricxapp --field-selector metadata.name=service-ricxapp-ss-rmr -o jsonpath='{.items[0].spec.clusterIP}'`
fi
if [ -z "$SS_XAPP" ]; then
    echo "ERROR: Failed to find ss-xapp NBI service; aborting!"
    exit 1
fi

echo "Getting Slice details:"
curl -i -X GET http://${SS_XAPP}:8000/v1/slices
echo;echo;echo

sleep $SLEEPINT

echo "Throttling the targeted Slice (fast2):"
echo
curl -i -X PUT -H "Content-type: application/json" -d '{
    "allocation_policy": {
        "type": "proportional",
        "share": 0,
        "throttle": true,
        "throttle_threshold": -1,
        "throttle_period": 10000,
        "throttle_share": 10,
        "throttle_target": 1
    }
}' http://${SS_XAPP}:8000/v1/slices/fast2
echo;echo;echo

SLEEPINT=10;
sleep $SLEEPINT 
echo "Getting Slice details (fast2):"
curl -i -X GET http://${SS_XAPP}:8000/v1/slices
echo

echo "UnThrottling the targeted Slice (fast1):"
curl -i -X PUT -H "Content-type: application/json" -d '{
    "allocation_policy": {
        "type": "proportional",
        "share": 1024,
        "throttle": false,
        "throttle_threshold": -1,
        "throttle_period": 1800,
        "throttle_share": 10,
        "throttle_target": 1
    }
}' http://${SS_XAPP}:8000/v1/slices/fast2
echo;echo;echo

echo "Getting Slice details (fast2):"
curl -i -X GET http://${SS_XAPP}:8000/v1/slices
echo
echo "Script completed successfully!"

