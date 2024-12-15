#!/bin/bash

# Define your sudo password
SUDO_PASSWORD="170823"

echo $SUDO_PASSWORD | sudo -S kubectl -n ricxapp rollout restart deployment ricxapp-ss
# Navigate to the target directory
cd ~/oaic/ss-xapp

# Export environment variables using sudo
export KONG_PROXY=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt -l app.kubernetes.io/name=kong -o jsonpath='{.items[0].spec.clusterIP}')
export E2MGR_HTTP=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-e2mgr-http -o jsonpath='{.items[0].spec.clusterIP}')
export APPMGR_HTTP=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-appmgr-http -o jsonpath='{.items[0].spec.clusterIP}')
export E2TERM_SCTP=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-e2term-sctp-alpha -o jsonpath='{.items[0].spec.clusterIP}')
export ONBOARDER_HTTP=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-xapp-onboarder-http -o jsonpath='{.items[0].spec.clusterIP}')
export RTMGR_HTTP=$(echo $SUDO_PASSWORD | sudo -S kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-rtmgr-http -o jsonpath='{.items[0].spec.clusterIP}')

# Onboard the xApp
curl -L -X POST "http://$KONG_PROXY:32080/onboard/api/v1/onboard/download" \
     --header 'Content-Type: application/json' \
     --data-binary "@ss-xapp-onboard.url"

# List onboarded charts
curl -L -X GET "http://$KONG_PROXY:32080/onboard/api/v1/charts"

# Register the xApp
curl -L -X POST "http://$KONG_PROXY:32080/appmgr/ric/v1/xapps" \
     --header 'Content-Type: application/json' \
     --data-raw '{"xappName": "ss"}'

echo $SUDO_PASSWORD | sudo -S kubectl logs -f -n ricxapp -l app=ricxapp-ss
