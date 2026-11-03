# cc → wc: handoff18 reply (3 Nov 2026)

1. **bias_sim_sparse:** already filled in (a12108f). You probably saw the file before that push.

   | filter | planted survival | mean σ |
   |---|---|---|
   | off | 0.5975 ± 0.0245 | 0.6106 |
   | on | 0.4375 ± 0.0248 | 0.4446 |

   The paper states the agreement.

2. **Best over basins.** `make_numbers.py` already takes the min over every saved point at each depth. I extended it to d = 8. Current best values, {−1,0,1,2} filtered:

   | d | T | source |
   |---|---|---|
   | 3 | 0.2793 | |
   | 4 | 0.2744 | |
   | 5 | 0.2730 | |
   | 6 | 0.27223 | from the {−2..2} basin, −2 projected out |
   | 7 | **0.27212** | |
   | 8 | ≤ 0.27212 | |

   Both new points (d6 0.27223, d7 0.27212) give identical values under B2 and S2, so they pass the survival recursion.

   **Re-polish runs, launched about 30 min ago with 6 h limits:**
   - d4 and d5 from the projected mm5 points: projected T is 0.2750 and 0.2740, worse than the current starts but a different basin;
   - d7 from the d6-0.27223 point extended by one level: start 0.2814;
   - d8 from the d7 best extended: start 0.27212.

   I stopped the stale runs: the old-basin d8, {−2..2} d6 ×2, and {−2..2} d7. The last one had not completed a single round in 10 h, and the −2 question is settled.

   **Fit** T_d = T∞ + A r^d over subsets of d = 3..7:

   | depths fitted | T∞ | r |
   |---|---|---|
   | 3–7 | 0.27204 | 0.34 |
   | 4–7 | 0.27183 | 0.45 |
   | 3–6 | 0.27206 | 0.34 |
   | 3,4,5,7 | 0.27211 | 0.33 |
   | 3,5,6,7 | 0.27189 | 0.39 |

   The fit is unstable in the 4th decimal (0.2718–0.2721), so the paper says "converges to about 0.272" and gives the best computed point.

**Paper (Nick asked not to wait for the runs):**

| Place | Now states |
|---|---|
| Title | 2^{0.2721n} |
| Abstract | depth 4 gives 0.2744; best computed 0.2721 at depth 7; converges to about 0.272 |
| Table 1 | rows d = 3, 4, best (d = 7) |
| Contributions | d ≤ 8 |
| Theorem | \Tbest at \Tbestdepth, plus depth 4 |

- **Program paragraph:** warm starts from all basins, best over starts; fixed depth with per-level constants.
- **Saturation:** depth table d = 2..8, fit range 0.2718–0.2721, and "deeper trees alone do not lead to subexponential time within this accounting".
- **Structure paragraph:** updated to the new d6 point (bottom δ_6(1) = 0.0049, δ_6(2) = 0.0112, δ_6(−1) = 0.0194, last-merge I = 0.27).
- **Conclusion:** one sentence saying that what remains is merge cost and that a structural change is needed (no floor numbers; floor still excluded).
- **Appendix:** adds the d = 7 parameter table.
- **Todos:** no red todos remain. I dropped the "Commit: [hash]" line; add it at ePrint time.

If the re-polish runs improve anything, `make_numbers.py` + rebuild picks it up with no text changes. The only exception is the hand-quoted d6 bottom-level masses in the Structure paragraph.
