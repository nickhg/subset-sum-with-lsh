#!/bin/sh
# handoff16c grid: Meet-LWE tree model, unfiltered vs filtered, may vs surv accounting
for om in 0.5 0.3 0.667; do
  for D in -1,0,1 -2,-1,0,1,2; do
    for d in 3 4 5 6; do
      for acc in may surv; do
        for f in p filt; do
          nice -n 15 timeout 3600 python3 meetlwe_model.py $D $d $om $acc $f 4
        done
      done
    done
  done
done
