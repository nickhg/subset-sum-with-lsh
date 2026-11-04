# wc → cc: handoff24 (Meet-LWE filtered gain: next steps)

Nice result. It overturns the fixed-parameter no-go for exactly the reason seen in subset sum: re-optimised split laws create bottom-level waste (p_4 −0.006 → −0.045), and the filter removes it.

1. **Depth-5 discrepancy, first check:** is our *unfiltered* d4 point (0.351096, our convention = May's depth 5) inside May's Rep-1 parametrisation, i.e. split laws expressible with his ε^(j) structure and weights? Report its split laws next to the nearest Rep-1 point.
   - If it lies **outside** Rep-1: it's a generalisation, not a contradiction. Say so, and quote the filter gain against our unfiltered 0.3511 (−0.008).
   - If it lies **inside** Rep-1: re-run May's own optimisation at depth 5 within Rep-1 to see whether his "no improvement" was an optimiser limitation. Only then do we consider asking Alex.
2. **Robustness:** finish the ml_hop runs (ω = 0.3, 0.5, 0.667; d4, d5; ±filters). Report the filter gain against the best unfiltered value at equal depth, for each ω.
3. **Soundness, same as subset sum:** the symmetry lemma (coordinate permutations with the columns of A permuted) and one small-n planted bias simulation of a filtered Meet-LWE merge shaped like the binding bottom merge.
4. **Concrete parameters (later):** pick 1–2 of May's Table 6 instances and include integer r^(j) and the guessing cost, to see whether the asymptotic gain survives at real sizes.
5. **Placement:** Nick to decide. Default: a separate note (not the subset-sum ePrint), possibly a joint one later. Keep it in ntru_hybrid/, with no `\ifincludemeetlwe` section in paper/ for now.
