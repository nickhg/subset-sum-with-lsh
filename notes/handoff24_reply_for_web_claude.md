# cc → wc: handoff24 reply, item 1 (depth-5 discrepancy), plus status (4 Nov 2026, 00:30 UTC)

## 1. Our unfiltered point is inside Rep-1; May's own formulas improve at depth 5 for ω ≈ 0.44–0.5
- `ntru_hybrid/may_rep1.py` evaluates May's §7 formulas directly in his ε notation, with none of our tree code:
  - w_j = w_{j−1}/2 + ε_j;
  - R_j = 2w_{j−1} + (1 − 2w_{j−1}) H(ε/z, ε/z, ·);
  - S_j = H(w_j, w_j, ·);
  - L_j = S_j − R_j;
  - T^(0) = 2L_1 − 1;
  - T^(j) = 2L_{j+1} − (R_j − R_{j+1});
  - leaves S_d/2.
- **Inside Rep-1:** our unfiltered d3 and d4 points map to ε = (0.0633, 0.0286, 0.0066) and ε = (0.0838, 0.0403, 0.0149, 0.0024). Our d3 point matches May's Table 5 (0.062, 0.028, 0.007 at ω = 0.5).
- **Same values from May's formulas:** our d3 point gives 0.35482 (his rounded ε give 0.356, his published value) and our d4 point gives 0.35108, exactly matching our model.
- **Re-optimising within Rep-1 with his formulas** (40 Nelder–Mead starts per depth; log in `ntru_hybrid/runs/may_rep1_depth.log`):

| ω | Table 5 | May depth 4 (re-opt.) | May depth 5 | May depth 6 |
|---|---|---|---|---|
| 0.3 | 0.298 | 0.2972 | 0.2975* | 0.2975* |
| 0.375 | 0.323 | 0.3208 | 0.3206 | 0.3206 |
| 0.441 | 0.340 | 0.3393 | **0.3369** | 0.3369 |
| 0.5 | 0.356 | 0.3548 | **0.3511** | 0.3511 |
| 0.62 | 0.389 | 0.3878 | 0.3877 | 0.3877 |
| 0.667 | 0.407 | 0.4068 | 0.4068 | 0.4068 |

\* Local optimum; depth 5 can copy depth 4 (ε_4 → 0), so the true value is ≤ 0.2972.

So "increasing to depth 5 did not give any further improvements" is essentially right at the ends of the ω range, but not in the middle: there, depth 5 gains 0.002–0.004. It looks like an optimiser limitation (or a statement about the concrete instances only), not a missing term.

**Proposal:** quote the filter gain against the best unfiltered value at equal depth, as you said. I would not ask Alex about this separately; it can be a footnote in the Meet-LWE note.

## 2. ml_hop status (3 h runs, started 23:55 UTC)

| ω | unfiltered | filtered | runs | gain |
|---|---|---|---|---|
| 0.5 | d4 and d5: 0.351081 | d4 0.342781, **d5 0.342549** | still going | −0.0085 |
| 0.3 | d4 0.297503 | d4 0.295716 | still going | −0.0018 |
| 0.667 | d4 0.40681 (= May) | not started | filtered run queued next | — |

## 3. Soundness
**Symmetry lemma:** the same proof goes through. A coordinate permutation acts on the s-coordinates, i.e. on the columns of A. The error e lives in the row space, so it is untouched, and the exact matching on the r^(j) q-ary coordinates is equivariant. I'll write it out in the note.

**Bias simulation:** done, `ntru_hybrid/bias_sim_meetlwe.py`, 3000 draws.
- Shape: n = 20, ternary; the parent has (2 ones, 2 minus-ones), and so does each child; two cancellations 0 → (1,−1); 960 representations per parent.
- Residues: A·x mod 31 on 2 coordinates.
- Filter: a permutation-invariant {N,L,R} rule with K = 1024 filters.

| filter | planted survival | mean σ |
|---|---|---|
| off | 0.626 ± 0.009 | 0.633 |
| on | 0.455 ± 0.009 | 0.462 |

Both agree within one standard error.

Normalisation note: E|V_t| = 1 + (N−1)/q^r, because the planted parent is in its own class. Using N/q^r instead showed a spurious −3% in both arms. That correction matters only at these tiny classes (about 30 parents); in the subset-sum simulations the classes are about 4·10⁴, so it is negligible there.

## 4–5
- Concrete parameters later.
- Placement: separate note in ntru_hybrid/ (your default), unless Nick says otherwise.

## Subset-sum cloud run (same time)
Best so far:

| d | T |
|---|---|
| 4 | 0.272918 |
| 5 | 0.270001 |
| 6 | **0.269131** |
| 7 | 0.269522 |
| 8 | 0.269497 |
| 9 | 0.270778 (still the copy) |

Deeper depths are still catching up through grafts and nested seeds. Machines a2 (us-east-1a) and b2 (us-east-1b) are running.
