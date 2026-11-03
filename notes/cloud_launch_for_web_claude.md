# cc → wc: cloud polish run launched (3 Nov 2026, 23:30 UTC)

Two c7a.24xlarge spot instances (96 vCPU each), both in us-east-1d, at about $1.25/h each. Each runs for 8 h. Each instance shuts itself down, and so terminates, at 9 h, around 08:30 UTC 4 Nov. Expected total about $20, capped at about $23. Both run code commit b64847d.

| machine | workers by depth | jitter scales | seeds |
|---|---|---|---|
| a (refine) | d4 ×12, d5 ×16, d6–8 ×22 each (94) | 0.1, 0.3, 0.6, 1, 2 | 1001… |
| b (explore) | d4 ×6, d5 ×12, d6–8 ×22 each, **d9 ×12** (96) | **0.3, 1, 2, 3, 5** | 1501… |

**Sharing:**
- `cloud/poll_all.sh` (local, every 15 min) pulls both machines.
- It then copies each depth's global best (d4–d9) to any machine that lacks it.
- Every worker restarts from the best file in its own results directory, or grafts from the best at d−1. A d5 improvement on either machine therefore reaches the other's d6 grafts within 15 min.
- d9 starts by grafting the d8 best.

**Spot safeguards (isodual):**
- self-shutdown on the instance;
- results rsynced every 15 min, so a reclaim loses at most 15 min;
- all AWS calls under a timeout;
- I terminate both instances by hand as soon as the 8 h are up.

**Post-run checklist:**
1. Per depth, the global best over both machines.
2. `floor/recost.py` (independent evaluator) and the S2 check on each best.
3. Corner flags.
4. Copy the bests into `floor/runs/polish/`, then run make_numbers.py.
5. Refit only if d6–9 converge.
6. Paper wording per handoff21, then a new dated PDF.
7. Heads-up to Alex if the headline is about 0.270 or below.
