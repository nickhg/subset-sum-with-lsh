#!/bin/bash
# Every 5 min: pull every instance listed in cloud/INSTANCE_*, then copy each depth's global best point to every
# instance that lacks it (so grafts on one machine start from the other's improvements).  Stops when none is running.
cd "$(dirname "$0")/.."; SSHOPT="-o StrictHostKeyChecking=no -o ConnectTimeout=20 -i $HOME/.ssh/subset-sum-key.pem"
while :; do
    alive=0
    for f in cloud/INSTANCE_*; do
        n=${f#cloud/INSTANCE_}; read -r id ip _ < "$f"
        st=$(timeout 60 aws ec2 describe-instances --instance-ids $id --query 'Reservations[0].Instances[0].State.Name' --output text 2>/dev/null)
        [ "$st" = running ] && { alive=1; NAME=$n bash cloud/launch.sh pull > /dev/null 2>&1; }
        echo "$(date -u +%FT%TZ) $n $st" >> cloud/poll.log
    done
    best=""
    for d in 4 5 6 7 8 9; do
        b=$(ls cloud/results/*/res/d${d}_T*.npy 2>/dev/null | awk -F/ '{print $NF" "$0}' | sort | head -1 | cut -d' ' -f2)
        [ -n "$b" ] && best="$best $b"
    done
    echo "$(date -u +%FT%TZ) best:$(for b in $best; do printf ' %s' "$(basename $b .npy)"; done)" >> cloud/poll.log
    for f in cloud/INSTANCE_*; do
        n=${f#cloud/INSTANCE_}; read -r id ip _ < "$f"
        for b in $best; do
            [ -e "cloud/results/$n/res/$(basename $b)" ] || timeout 60 scp -q $SSHOPT "$b" ubuntu@$ip:ss/res/ 2>/dev/null
        done
    done
    [ $alive = 0 ] && { echo "$(date -u +%FT%TZ) no instance running: stop" >> cloud/poll.log; exit 0; }
    sleep 300
done
