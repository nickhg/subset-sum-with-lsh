# wc → cc: handoff15. Research item: NTRU-style cliff + representation tree (Meet-LWE inside the tree)

**Priority:** spare cores only. The paper runs (handoff14) come first. This is exploratory and **not for the current paper**. Put everything in a new folder `cliff/`.

## Setup
Knapsack lattice basis (rows):
  [q, 0, …, 0], [a_1, 1, 0, …], [a_2, 0, 1, …], …, [a_n, 0, …, 1],   q = 2^n.
All of the determinant sits in the q-row. Take the **block** B = q-row + the first k = βn weight rows. After reduction its Gram–Schmidt (GS) mean is 2^{n/k} = 2^{1/β} (β = 0.1 gives 2^{10}). The other (1−β)n rows have GS = 1. That is the cliff, as in Nick's NTRU hybrid.

Given the "rest" coordinates x_R, the residual problem on the block is subset sum with k items and n-bit weights (density β), which lattice reduction solves for random instances.

## Part A. Cliff feasibility (model + small experiments)
1. Smallest GS length of the reduced block against k, for BKZ-b and HKZ, at n = 64…512. The cliff works while GS_min ≫ ½ (errors are ±½ centred, or {0,1}). Asymptotically, HKZ's profile spans ≈ Θ(log² k) bits, so we expect k ≲ n / log² n. **Measure the real crossover** (with fpylll/G6K): the largest β for which Babai on the block recovers x_B with probability ≥ 0.9 given the correct x_R, by n.
2. Cost of the reduction: BKZ/HKZ in dimension k+1. Report it at the crossover β.

## Part B. Baseline hybrid (no representations)
Meet in the middle over x_R using Babai additivity, with LSH for the boundary flips (the NTRU hybrid of HG07):
- Model: time ≈ 2^{(1−β)n/2} × LSH overhead, plus the reduction. At β = 0.1 that is ≈ 2^{0.45n}.
- Implement it at small n (40–64) and measure the additivity-failure rate and its LSH correction cost. This is a sanity check that the hybrid machinery works for knapsacks.

## Part C. The real question: combine the cliff with the filtered representation tree
**Obstruction:** the tree's inner levels need the root target modulo M_1 (≈ 2^{0.85n}) in order to set consistent residues τ. The true target is t − ⟨a_B, x_B⟩ with x_B unknown, so its residue mod M_1 takes up to 2^k values. Exact modular constraints can't absorb that. Guessing the residue costs the block's whole entropy: T ≈ 0.2726 + 0.73β, which is worse.

**Proposed fix (Meet-LWE style):** put the tree's constraints on **Babai residues in the block quotient group** G = Z^{k+1}/L_B instead of on integers mod M.
- The map s ↦ class of (K·s, 0) in G is exactly additive. Partial sums of x_R satisfy r(s_1 + s_2) = r(s_1) + r(s_2) in G.
- The unknown block part appears **only at the root**, as a small error vector e ∈ {0,−1}^k (in coordinates).
- Constraints are "r(s) lies in cell τ" on a grid of width w along some GS coordinates. The inner levels are exact up to grid carries. Only the root, and every level whose τ consistency depends on the root, sees the e-perturbation.

Model and compute:
1. **Information budget:** the bits available from cells = Σ over the used GS coordinates of log2(GS_i / w). Compare with the n − k bits needed for density 1 on (1−β)n coordinates.
2. **Tolerance cost:** e shifts the target across cell boundaries in each used coordinate with probability ≈ 1/w (or exactly, from the GS lengths). Compare three ways of handling it:
   - (a) repetition with random grid shifts;
   - (b) enumerating the ≤ 2^{#crossings} neighbouring cells;
   - (c) Dubiner/LSH tolerant matching at the affected merges (reuse `filter_terms`: the tolerance is a type-class condition on the cell offsets).
3. **Net exponent:** T(β, w, method) = (tree exponent on (1−β)n coordinates with the cell-constraint budget) + (tolerance cost) + (reduction cost). Optimise over β and w. My rough count for naive rounding (a): gain ≈ 0.2726β against cost ≈ 0.72β, a net loss. The question is whether (b) or (c) make the tolerance cheaper than 0.2726β.
4. Report T_min(β) for n → ∞ (within the cliff-feasibility limit of Part A, which may force β → 0) and also at concrete n = 128, 256, 512, using the measured crossover β from Part A.

## Deliverable
`cliff/cliff_reply_for_web_claude.md` with:
- the Part A crossover table;
- the Part B small-n results;
- the Part C model and the optimised exponents (asymptotic and concrete), with a clear verdict: no gain / concrete-only gain / asymptotic gain;
- anything that contradicts the analysis above.

References to check while modelling: Howgrave-Graham, "A hybrid lattice-reduction and meet-in-the-middle attack against NTRU" (CRYPTO 2007); May, "How to meet ternary LWE keys" (Meet-LWE, CRYPTO 2021); Kirshanova–May (IMACC 2021); Karenin–Kirshanova–May–Nowakowski, ePrint 2025/1910.
