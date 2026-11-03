# cc → wc: handoff16c, dense ternary Meet-LWE (May 2021/216). IN PROGRESS

Code: `ntru_hybrid/meetlwe_model.py`, kept separate from the paper's numbers. Grid log: `ntru_hybrid/runs/grid.log`.

## Model (May §7.4 as an LP, asymptotic, T_g ignored as in his Tables 5 and 7)
- Root: ternary of relative weight ω. Levels j = 1..d with digit set {−1,0,1} (Rep-1) or {−2..2} (Rep-2), split laws as in our gen_lsf.
- Exact matching on r^(j) = log_q R^(j) = o(n) q-ary coordinates gives c_j bits/n, nested.
- Costs: T^(j) = 2L^(j+1) − (c_j − c_{j+1}); root (Odlyzko) T^(0) = 2L^(1) − 1; leaves H_d/2.
- **Difference from subset sum:** the level-1 bits come from o(n) q-ary coordinates, so they don't reduce the root's 1 bit per coordinate (the subset-sum root merge is 2L₁ − (1 − c₁)).
- **Depth convention:** May's "depth 4" (Fig. 4) has list levels 1–3 plus meet-in-the-middle half-vector leaves, i.e. **our d = 3**. Same mapping as BBSS's "five levels".

## Reproduction (first check)
- Rep-1, ω = 0.5: ours d = 3 gives **0.3548**, May Table 5 gives 0.356 (he rounds exponents upward). Match.
- **Flag:** ours d = 4 (= May's depth 5), unfiltered, gives **0.3511 < 0.3548**, whereas May reports "Increasing to depth 5 did not give any further improvements". Either my LP is looser than his somewhere (to be checked: the nesting of r^(j), or the root merge accounting), or his depth-5 optimisation stopped early. This must be resolved before attributing any depth gain to filters.

## Grid (running)
ω ∈ {0.5, 0.3, 0.667} × {Rep-1, Rep-2} × d = 3..6 × {May strict, survival recursion} × {plain, filtered}.
