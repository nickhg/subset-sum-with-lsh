# cc → wc: handoff16 / 16b, first results (3 Nov, night)

HKLS estimator: `git clone https://github.com/yonghaason/PrimalMeetLWE ntru_hybrid/hkls_code` (not tracked here).

## Verdict so far: in HKLS's sparse-key regime the filters have almost nothing to remove

Reading notes and literature: `ntru_hybrid/reading_notes.md`.
- **Literature:** nobody in the Meet-LWE line (May 2021/216, KM21, HKLS 2022/1473, Bi et al. 2022/1330, KKMN 2025/1910) filters on the representation coordinates. All of them check the ternary pattern after a value match.
- **Depth optima:** 4 for May, 2 for HKLS.

**Fixed-parameter re-costing of HKLS's own logged optima with the product bucket** (value-LSH bucket × type-class label; `filtered_hkls.py`, using their estimator's cost formulas; log in `runs_filtered_hkls_14_426_256.log`):

| HKLS optimum | merge | weights | log S | log N_col | merge cost (HKLS → filtered) | pair saving |
|---|---|---|---|---|---|---|
| (2^14, 2^426, 256), t=3 | 1→0 | 20→26 | 93.0 | 95.7 | 105.63 → 104.01 | 2^−3.69 |
| | 2→1 (binding) | 10→20 | 89.0 | 100.4 | 110.77 → 110.74 | 2^−0.04 |
| | 3→2 | 5→10 | 49.9 | 89.6 | 95.26 → 95.24 | 2^−0.02 |
| (2^14, 2^426, 256), t=2 | 1→0 | 20→26 | 93.8 | 96.5 | 107.38 → 105.74 | 2^−3.69 |
| | 2→1 (binding) | 10→20 | 89.8 | 94.5 | 110.33 → 110.33 | 0 |

- Guess cost: 115.73 → 115.67 (t = 3) and 111.59 → 111.48 (t = 2).
- **The final cost is unchanged (121.21, 120.91)**, because the lattice side (116.6) is the max at these points.

**Why.** At HKLS's binding merges the split has **no cancellations** (w′ = w/2, e.g. 10 → 20). A valid pair just needs disjoint supports, and two random weight-10 vectors in d ≈ 2000 coordinates are disjoint with probability about 1. So nearly every value near-collision passes the weight check: the representation-pattern waste is 2^{−0.04}.

HKLS's real waste is in the **value domain**: near-collisions on the r^{(i−1)} projected coordinates that do not continue to the next level. That is what their LSH-NCF and repetition costs are about. Pattern waste only appears at merges with cancellations (the top merge, 20 → 26 with 7 cancellations), where the filter saves 3.7 bits on pairs, but that merge isn't binding.

**This contradicts the handoff16 expectation** ("HKLS has the waste that filters target"). The check exists (Alg. 4, lines 6–8), but in the sparse regime it rejects almost nothing. Subset sum at density 1 is the opposite regime: dense digit laws, so most matched pairs overlap badly.

## Caveats and what's not done

- **Fixed parameters only.** A full re-optimisation (β, d, w_g, w^{(i)}) could choose more cancellations once they become cheaper. The asymptotic type-class exponents are also optimistic with 5–26 nonzeros. Neither changes the qualitative picture at the binding merges, where w′ = w/2 is what HKLS's optimiser chose.
- **Part 2 (the floor against β, i.e. the "subexponential?" question):** not done. Given the above, the natural regime for filters would be **denser** keys (non-sparse ternary, e.g. NTRU or Kyber-like), which HKLS explicitly don't target. I suggest Part 2 there, if anywhere.
- I only re-costed the (2^14, 2^426, 256) logs so far. The other five parameter sets have the same structure (w′ = w/2 at the lower levels), so I expect the same result. Happy to run them if you want the table complete.
