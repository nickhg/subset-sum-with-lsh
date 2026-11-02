#!/bin/bash
# runs one job line: DIGITS d VARIANT restarts
cd "$(dirname "$0")"
set -- $1
tag="${1//,/_}_d$2_$3"
timeout 7200 python3 recursive_floor.py "$1" "$2" "$3" "$4" 0 > "runs/rf_$tag.log" 2>&1
