# wc → cc: handoff19. Final polish before ePrint

Items marked **[Nick]** need Nick's decision; leave those for him.

## A. Fixes
1. **Table 1 dagger caption:** it says strict-accounting filtered {−1,0,1} is 0.2864 at d=3 and that d=4 did not improve. The morning summary had 0.2893 / 0.2890 for strict {−1,0,1} at d=3/4. Check which is right and make the caption and the logs agree.
2. **Gain bookkeeping:** the intro uses the published 0.2830 (gain 0.0109); §5 uses the recomputed 0.2831 (gain 0.0110). Say once in §5 "(from our recomputed 0.2831)".
3. **Proposition 5: turn the sketch into a proof.** Use Hoeffding for sampling without replacement (Hoeffding 1963, §6; or Serfling 1974). After the random permutation, each block of size s = ⌈√n⌉ is a sample without replacement. For each (digit, label) class, Pr[|count − s·freq| > ε s] ≤ 2 exp(−2 s ε²) = 2 exp(−2 log² n) with ε = n^{−1/4} log n. A union bound over b ≈ √n blocks and O(1) classes gives o(1). This is needed only for the planted valid pair (a single fixed pair), since atypical vectors enter no filter. Then remove "a full proof of the concentration step" from the open problems, and change "Proof sketch" to "Proof".
4. **Memory:** add a memory exponent to each reported optimum (max over lists of ℓ_j, and over filtered merges of the entry terms ℓ + I(XY;Λ) − I(X;Λ) etc.). Put it as a column or line in Tables 3, 5–7 and one sentence in §5. Add a one-line open problem: quantum (walk / Grover) versions of filtered merges, as in BBSS.
5. **Why filtering is strong at the top and bottom levels but weak in the middle:** add a p_j column (log-probability that a random matched pair is a valid split) to the parameter tables, and one paragraph in §5. Filters pay where 2^{p_j} ≪ 1:
   - at the dense top levels, overlapping supports;
   - at the sparse bottom levels, 1 → (2, −1) splits, which need a 2 and a −1 at the same coordinate;
   - in the middle levels, supports are sparse and splits are mostly 1 → (1, 0), so random pairs are almost always valid and there is nothing to filter.
   The same mechanism explains why filters gave nothing for Meet-LWE (see C.2).
6. **Table 1:** add a light rule or spacing between the {−1,0,1} "this work" row and the BBSS row.
7. **Appendix A:** add the public repository link and the commit hash at ePrint time.

## B. Lattice sentence  [Nick, optional]
Conclusion: "Lattice-based hybrids … are competitive at density one" → "may be competitive" (Nick prefers not to assert anything definitive about lattices).

## C. [Nick] decisions
1. **Li sentence:** the second sentence ("Charging each three-list merge … we obtain 0.39") goes beyond the short neutral line Nick asked for, and its referent is unclear. Either drop it (default), or, if you have verified Li's cost accounting, make it explicit: "In our reading of [15], the 0.24 charges each three-list merge by its output size; charging for the pairs it enumerates gives about 0.39." Report in your reply what exactly was checked.
2. **Ternary-LWE open problem:** we tested it (handoff16/16c) and found no gain at the published Meet-LWE optima (HKLS sparse and May dense), because the binding merges have little pattern waste. Either restrict the open problem to decoding, or (default) add: "for Meet-LWE we found no gain at the published optima, where the binding merges have little split-pattern waste (cf. item A5)".
