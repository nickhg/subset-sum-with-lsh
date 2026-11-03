# wc → cc: handoff3 (2 Nov 2026, evening)

Thanks. Task A and the symmetry argument look solid. Please write the symmetry argument up as a lemma: P(planted parent survives) = E[σ] exactly, given the τ's at the node. Three new items:

## 1. Fill in the bias_sim table  [quick]
In the reply, RESULT_OFF / RESULT_ON / RESULT_CLASS are still placeholders. Please paste in the numbers (mean σ, P(planted survives), and the passing-pair class split), with filter off and on.

## 2. Joint survival of the solution's two siblings  [HIGH]
Symmetry gives the marginals, not the joint. At the d=4 optimum the root is exactly tight (+0.128 = 2 × 0.064), so what matters is whether
  log2 P(both planted siblings survive) ≈ 2 · log2 P(one survives)
holds to first order in n. The earlier survival run at c=2 already showed correlated root-sibling failures (0.50–0.65 found vs 0.77 predicted).
- In bias_sim (or a two-sibling variant), plant the full split of a parent into two children. Record P(A* survives), P(B* survives) and P(both), over many draws, at a few n (e.g. 24, 32, 40).
- Report log2 P(both) − log2 P(A*) − log2 P(B*) as a function of n. If it stays bounded, the correlation is a constant factor and harmless. If it grows linearly, estimate the slope. The optimum would then need that much extra root excess.

## 3. Task D: wider digit sets under B2  [MEDIUM, cheap]
Lattice-style digit laws: mostly 0/±1 with a thin tail of larger digits.
- Run B2 at d = 4 and 5 with digit sets {−2,…,2}, {−1,…,3} and {−4,…,4}, warm-started from the {−1,0,1,2} optima (new digits at a small seed mass).
- Report T and the optimal masses on digits beyond {−1,0,1,2}. Do they go to 0, or stay positive?
- At the d=4 {−1,0,1,2} optimum, report the marginal ∂T/∂(mass on 3) (and on −2): the marginal value of the tail.
- Goal: does anything move T noticeably below 0.2733? If the total gain from wider digits is < ~0.005, that suggests 0.25 needs a structurally new merge.

## 4. Block hybrid write-up note
The 0.276 lattice + guessing figure (β ≈ 0.945, memory 0.197) deserves a short literature check, e.g. search "subset sum randomized slicer", "CVPP subset sum density 1", and work by Ducas–Laarhoven–van Woerden or Kirchner–Fouque. Then a one-paragraph remark with the heuristic caveats.
