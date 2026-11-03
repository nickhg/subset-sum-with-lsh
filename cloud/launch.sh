#!/bin/bash
# One spot instance running cloud/polish_worker.py on every core (pattern of isodual/cloud_instances/aws/launch_phi65.sh).
#   launch.sh create TYPE HOURS      request the instance (spends money: needs Nick's approval); writes cloud/INSTANCE
#   launch.sh deploy HOURS           copy the committed code + cloud/seed, start the workers (worker split: SPLIT)
#   launch.sh pull                   rsync results and logs into cloud/results/ (run from poll.sh every 15 min)
#   launch.sh stop                   terminate the instance
# The instance shuts itself down (and so terminates) after HOURS + 1 h whatever happens.
set -u
CMD=$1
AMI_ID=ami-080e1f13689e07408; KEY_NAME=subset-sum-key; SEC_GROUP=sg-0aa75b716a6092f71
SSHOPT="-o StrictHostKeyChecking=no -o ConnectTimeout=20 -i $HOME/.ssh/$KEY_NAME.pem"
ROOT=$(cd "$(dirname "$0")/.." && pwd); INST=$ROOT/cloud/INSTANCE
SPLIT=${SPLIT:-"4:12 5:16 6:22 7:22 8:22"}            # depth:workers (96 in total)
case $CMD in
create)
    TYPE=$2; HOURS=$3; UD=$(mktemp)
    printf '#!/bin/bash\nshutdown -h +%d\napt-get update\nDEBIAN_FRONTEND=noninteractive apt-get install -y python3-numpy python3-scipy python3-pip rsync screen\npip3 install "scipy>=1.10" "numpy<2"\ntouch /var/tmp/ready\n' \
        $(( (${HOURS%.*} + 1) * 60 )) > "$UD"
    id=$(timeout 120 aws ec2 run-instances --image-id $AMI_ID --instance-type "$TYPE" --key-name $KEY_NAME \
        --security-group-ids $SEC_GROUP --instance-market-options '{"MarketType":"spot"}' \
        --instance-initiated-shutdown-behavior terminate \
        --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=subset-sum-polish}]" \
        --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":20,"VolumeType":"gp3"}}]' \
        --user-data "file://$UD" --query 'Instances[0].InstanceId' --output text) || exit 1
    rm -f "$UD"; timeout 600 aws ec2 wait instance-running --instance-ids $id
    ip=$(timeout 60 aws ec2 describe-instances --instance-ids $id --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
    echo "$id $ip $TYPE $(date -u +%FT%TZ)" > "$INST"; cat "$INST" ;;
deploy)
    HOURS=$2; read -r id ip _ < "$INST"
    (cd "$ROOT" && git diff --quiet HEAD -- gen_lsf.py cloud/polish_worker.py cloud/seed) || { echo "commit first"; exit 1; }
    until ssh -n $SSHOPT ubuntu@$ip 'test -e /var/tmp/ready'; do sleep 20; done
    ssh -n $SSHOPT ubuntu@$ip 'mkdir -p ss/cloud ss/res ss/logs'
    scp $SSHOPT "$ROOT/gen_lsf.py" ubuntu@$ip:ss/
    scp $SSHOPT "$ROOT/cloud/polish_worker.py" ubuntu@$ip:ss/cloud/
    scp $SSHOPT "$ROOT"/cloud/seed/*.npy ubuntu@$ip:ss/res/
    git -C "$ROOT" rev-parse HEAD | ssh $SSHOPT ubuntu@$ip 'cat > ss/VERSION'
    w=0; cmds=""
    for p in $SPLIT; do d=${p%:*}; k=${p#*:}
        for i in $(seq 1 $k); do w=$((w+1)); cmds="$cmds nohup python3 cloud/polish_worker.py res $d $w $HOURS $((1000+w)) > logs/w$w.log 2>&1 &"; done
    done
    ssh -n $SSHOPT ubuntu@$ip "cd ss && $cmds sleep 1; pgrep -fc polish_worker"
    echo "started $w workers on $ip" ;;
pull)
    read -r id ip _ < "$INST"; mkdir -p "$ROOT/cloud/results"
    timeout 300 rsync -az -e "ssh $SSHOPT" ubuntu@$ip:ss/res/ "$ROOT/cloud/results/res/" &&
    timeout 300 rsync -az -e "ssh $SSHOPT" ubuntu@$ip:ss/logs/ "$ROOT/cloud/results/logs/" &&
    for d in 4 5 6 7 8; do ls "$ROOT/cloud/results/res" | grep "^d${d}_T" | sort | head -1; done ;;
stop)
    read -r id ip _ < "$INST"; timeout 120 aws ec2 terminate-instances --instance-ids $id --output text ;;
*) echo "usage: $0 create TYPE HOURS | deploy HOURS | pull | stop"; exit 1 ;;
esac
