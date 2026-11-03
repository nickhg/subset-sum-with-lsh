# cc → wc: new optima after the email, and a cloud polish plan (3 Nov 2026, afternoon)

## 1. The email went out with the 08:00 PDF
- Nick sent it to Alex with rounded numbers only: 0.2830 → 0.2793 at BBSS depth; "depth 4 already gives about 0.274, and deeper trees converge to about 0.272". He dropped the "all merge costs tie" sentence; the tie holds only at d4.
- ePrint is planned for next week.

## 2. Since then the re-polish runs found better points
These are the runs started from other basins (handoff18). All pass the survival recursion (B2 = S2), and resetting π = Q_λ leaves T unchanged.

| d | in the sent PDF | now | source |
|---|---|---|---|
| 4 | 0.2738 | **0.27322** | gen_m4_4_f_73 |
| 5 | 0.2730 | **0.27078** | gen_m4_5_f_74, from the {−2..2} d5 point with −2 projected out |
| 6 | 0.27223 | 0.27223 | |
| 7 | 0.27212 | 0.27212 | |
| 8 | 0.2719 | **0.27152** | gen_m4_8_f_71 |

The d5 point looks clean:
- all five merges tie at 0.2708;
- the root condition is tight (excess +0.1029 = −2s_1);
- the list, pair and output identities check by hand.

**Consequences:**
- The email's rounded claims are now conservative, not wrong.
- The depth-limit story is broken for now. d5 beats d6–8, so the deeper runs are simply unconverged and the geometric fit (T∞ ≈ 0.272) means nothing until they are re-run from the new basin. The gain over BBSS becomes ≥ 0.0123.
- The paper still says 0.2719. The generated tables were reverted so that the source stays self-consistent. The new points are committed (8dd4a88).
- The "converges to about 0.272" wording, the Saturation fit and the hand-quoted d4/d6/d7 numbers (Structure, Where filters pay) will need redoing once the cloud run is in.

## 3. Why the old runs stalled
- `gen_opt.py` restarts jitter the raw logits by N(0, 0.3), but many logits have drifted to magnitudes of 10^3. For those, the jitter does nothing, so restarts never leave the basin.
- The new worker `cloud/polish_worker.py` canonicalises first: it re-expresses every softmax with logits bounded by log(10^12) ≈ 27.6, which gives the same laws to 10^−12 and the same T (checked on all five best points). Only then does it jitter, with a random scale in {0.1, 0.3, 0.6, 1, 2} on half the coordinates.
- Depth d+1 is seeded by **grafting**: a copy of one level of the best depth-d point is inserted, at whichever insertion position gives the lowest starting T. The old method copied the bottom level, which failed (start 0.2814).
  - Graft d5 → d6 starts at 0.2714.

## 4. Cloud plan
- Reuse the isodual AWS setup: us-east-1, Ubuntu 22.04 AMI, subset-sum-key, the same security group, spot, and a self-terminating `shutdown -h`.
- **One c7i.24xlarge (96 vCPU), about 8 h, roughly $15–25.** Nick approves before launch.
- The workers share one results directory. Each worker owns a depth; the split weights deeper depths: d4 ×12, d5 ×16, d6–8 ×22 each.
- Each worker restarts from the current best at its own depth (any worker's) or grafts from the current best at d−1. Improvements at d5 therefore propagate to d6–8 during the run.
- A local poller rsyncs the results every 15 min (isodual lesson: spot reclaims).
- Afterwards: an S2 check on every new best, then `make_numbers.py`, a refit, the paper text, and a new dated PDF.

## Questions for you
1. With d5 at 0.2708 and d6–8 unconverged, should the paper state "best computed point, depth d", give the limit only as "at most about 0.271", or drop the limit until the deep runs settle?
2. Alex has the 0.2719 PDF. If the final number is clearly lower (e.g. 0.270), should Nick send Alex a short heads-up before ePrint, or let the ePrint version speak for itself?
