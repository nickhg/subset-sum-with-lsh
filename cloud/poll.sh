#!/bin/bash
# Pull results every 15 min while the instance is alive; log the best per depth.  usage: poll.sh
cd "$(dirname "$0")/.."; NAME=${NAME:-a}; export NAME; read -r id ip _ < cloud/INSTANCE_$NAME
while :; do
    st=$(timeout 60 aws ec2 describe-instances --instance-ids $id --query 'Reservations[0].Instances[0].State.Name' --output text 2>/dev/null)
    echo "$(date -u +%FT%TZ) $st $(bash cloud/launch.sh pull 2>/dev/null | tr '\n' ' ')" >> cloud/poll_$NAME.log
    case $st in running|pending) sleep 900 ;; *) echo "$(date -u +%FT%TZ) instance $st: stop polling" >> cloud/poll_$NAME.log; exit 0 ;; esac
done
