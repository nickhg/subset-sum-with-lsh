# cc → wc: handoff16c / 17, dense ternary Meet-LWE (May 2021/216)

**Verdict: NO-GO** (checked at fixed parameters; full re-optimisation with filters still running at low priority, preliminary).

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

## Go/no-go (handoff17 step 1): May's own optimum, Rep-1, ω = 0.5, our d = 3 (his depth 4), split laws fixed

| merge | pattern waste 2^{p_j} | pairs (unfiltered) | binding? |
|---|---|---|---|
| root (Odlyzko) | 2^−0.130 | −0.405 | no |
| level 2 | 2^−0.057 | 0.3548 | yes |
| level 3 | 2^−0.015 | 0.3548 | yes |
| leaves H₃/2 | n/a | 0.3548 | yes |

Re-optimising only the filters gives T = 0.35482 → **0.35482** (log `runs/gonogo_rep1_d3_w0.5.log`).

**Why it is the opposite of subset sum.**
- In subset sum the root has only n bits (c₀ = 1). The top merges bind, and they carry heavy pattern waste (BBSS d = 3: 2^{p₁} ≈ 2^{−0.28} at the root). Filters remove it, and then depth pays.
- In Meet-LWE the exact constraints use o(n) q-ary coordinates, and Odlyzko's approximate root matching supplies a fresh bit per coordinate. So the root merge costs 2L₁ − 1, far below T.
- The binding terms are the leaf build H_d/2 and the deep merges, whose split laws have almost no cancellations: waste ≤ 2^{−0.06}. Filters cannot reduce the leaf build, and there is almost nothing to filter at the deep merges.

**Caveat (why "preliminary" for the re-optimised case).**
- In subset sum, re-optimising with filters moved to split laws with more cancellations. Here it would have to do so while the leaf build and the deep merges still bind, and filters don't help those. I expect at most a marginal gain.
- The grid (`run_grid.sh`, `runs/grid.log`) is still running at low priority to confirm. At 1 h per run on the loaded machine it won't finish tonight.

## Open flag (unrelated to filters)
- Ours, unfiltered, at d = 4 (= May's depth 5) gives 0.3511, below his depth-4 value 0.3548. That is a ~0.004 depth gain he reports as absent ("Increasing to depth 5 did not give any further improvements").
- Either my LP is looser than his model in some constraint I haven't spotted, or his depth-5 optimisation stopped early. This is worth checking before anyone cites it, but it has nothing to do with filters.

## Soundness note (if this is ever revived)
The symmetry lemma carries over: permuting the secret's coordinates together with A's columns leaves the law of (A, b) invariant for uniform A, and the filters are i.i.d. So planted-survival = mean σ holds per node, exactly as for subset sum.
