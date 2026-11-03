# cc → wc: handoff19 + 19b reply (3 Nov 2026)

## A
1. **Strict {−1,0,1} value.**
   - 0.2864 is right. I fixed the strict-accounting split law at your ε = (0.0274, 0.0203, 0.0053) and optimised only the filters under recursive_floor's F2 (strict) model. That gives 0.28653.
   - So the earlier F2 runs (0.2893 at d3, 0.2890 at d4) were optimiser failures (wrong basin), not a different model.
   - Warm F2 runs at d3 and d4 from this point are running (`floor/runs/rf_bcj_d{3,4}_F2wc.log`).
   - Until the d4 run finishes, the caption states only 0.2864 at d3 and makes no depth-4 claim. The morning summary is corrected too.
2. **Gain bookkeeping:** §5 now says "(from our recomputed 0.2831)".
3. **Prop 5:** now a full proof.
   - Hoeffding for sampling without replacement [Hoe63, §6], applied per block and per joint type: 2e^{−2sε²} = n^{−Θ(log n)}.
   - A union bound over O(√n) events gives o(1). It is needed only for valid pairs, since atypical vectors enter nothing.
   - "Proof sketch" is now "Proof", and the concentration step is gone from the open problems.
   - Bibitem Hoe63 added.
4. **Memory:** `make_numbers.py` computes max(H_d/2, ℓ_j, ℓ_j + entries gap) and adds it to the last line of every parameter table.
   - It is 0.2738 at d4 and 0.2721 at d7, equal or nearly equal to T, because the entry terms tie with the passing terms at the optimum.
   - Added a short Memory paragraph and the open problem "quantum (walk or Grover) versions of filtered merges, as in [BBSS20]".
5. **p_j column** added to all parameter tables, plus a "Where filters pay" paragraph. At d7, p_j is:

   | merge | top 1 | top 2 | middle 3 | middle 4 | 5 | sparse 6 | 7 |
   |---|---|---|---|---|---|---|---|
   | p_j | −0.33 | −0.09 | −0.05 | −0.005 | −0.03 | −0.18 | −0.04 |

   Savings follow the same profile, which supports your explanation. I left out the Meet-LWE sentence because it depends on Nick's C2 decision.
6. **Table 1:** added an \addlinespace before the BBSS row.
7. **Repository link and commit hash:** to be added at ePrint time.

## B
Applied "may be competitive".

## C (Nick)
Nick chose the defaults: C1 drops the 0.39 sentence; C2 adds the Meet-LWE no-gain clause to the open problem. Both applied.
- **C1:** the "0.39" line came from re-costing with ter_honest.py (your script). I have not independently re-derived Li's cost accounting from the paper.
- **C2:** the open problem is unchanged.

## 19b
1. **"What is proved"** paragraph added at the end of §1. §5 Saturation now says that each value is a computed point, not a proven optimum, so 0.2721 is not a lower bound for the model.
2. **TikZ figure** (Fig. 1, in §3): unfiltered and filtered merges side by side, with grey waste lines.
3. **Abstract:** final clause added: "The filters pay exactly at the merges where most matched pairs have the wrong split pattern."

## New numbers (re-polish from other starts, handoff18)

| d | T | source | survival recursion |
|---|---|---|---|
| 4 | **0.27378** (was 0.27440) | {−2..2} basin, −2 projected out | passes, B2 = S2 |
| 5 | 0.27305 | | |
| 6 | 0.27223 | | |
| 7 | 0.27212 | | |
| 8 | **0.27210** (now Tbest) | | passes, B2 = S2 |

- I hand-edited the d4 Structure sentence. Savings are now 0.066 / 0.049 / 0.009 at levels 1–3, and the last merge is unfiltered.
- **Refit:** T∞ comes out between 0.2719 and 0.2724, with r between 0.14 and 0.52, depending on which depths are fitted. The paper says "about 0.272".
- **Appendix:** gains a d8 parameter table.
- The d5 and d7 re-polish runs are still going.
