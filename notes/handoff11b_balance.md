# wc → cc: addendum to handoff11 (Nick: the "balance" point)

Nick would like to highlight, if the results support it, that the optimal filtered tree uses **both 2 and −2**: the digit set comes out symmetric, unlike BBSS's {−1,0,1,2}. For the {−2,…,2} runs at d = 4, 5 and 6, please report:

1. **−2 and 2 mass by level** at the optimum, from both warm starts. Is the −2 mass clearly positive (say ≥ 10⁻³ at some level), or a trace?
2. **Robustness:** T for {−2,…,2} against {−1,0,1,2} at the same depth, from ≥ 2 independent warm starts each, so we can see whether the gain (~0.0003 so far) exceeds the optimiser noise.
3. **Mechanism:** which splits generate −2 (0 → (2,−2), −1 → (−2,1), …), and at which levels. Is the use of 2 and −2 roughly symmetric in mass, or only nominally?

If 1–2 hold at d=6, we'll add one clause to the abstract, along the lines of "the optimal tree uses the balanced digit set {−2,…,2}", and a sentence explaining the mechanism in §5.
