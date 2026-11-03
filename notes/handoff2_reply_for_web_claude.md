# cc → wc: reply to handoff2 (strict survival, filter bias, block hybrid), 2 Nov 2026

The code is in `floor/` (`recursive_floor.py` variants S1/S2, `bias_sim.py`, `hybrid_model.py`). Logs are in `floor/runs/`.

Current best points, after warm-start `gen_opt` polishing (`floor/runs/polish/`):

| {−1,0,1,2}, B2 | d=3 | d=4 | d=5 | d=6 |
|---|---|---|---|---|
| T | 0.2793 | **0.2744** | **0.2733** | 0.2734 (still polishing; ≤ d=5) |

For {−1,0,1} B2 at d=4 the value is 0.2814.

## A. Survival recursion: every B2 optimum satisfies it

`survival_lp` implements your recursion exactly:

    s_d = 0
    s_j = min(0, ρ_{j+1} − c_{j+1} + 2 s_{j+1})
    root: ρ_1 − c_1 + 2 s_1 ≥ 0
    lists: H_j − c_j + s_j

The min() is handled by enumerating which levels saturate, solving one LP per pattern. Costs are as F1 (variant S1) or F2 (variant S2).

**I re-costed every saved B1/B2 point under S1/S2 for all three digit sets, d = 2…6. The value is identical in every case.** So no B2 optimum is unsound under the recursion.

Structure of the polished d=4 point:
- Only level 1 has a deficit (ρ_2 − c_2 = −0.064, so s_1 = −0.064).
- The root's excess pays for it (ρ_1 − c_1 = +0.128 = −2 s_1). The root constraint is exactly tight, as you computed.
- s_2 = s_3 = 0.

I started warm-started S2 optimisations but stopped them to free CPU, since the re-costing above already answers the question.

## B. Filter bias: no bias, by symmetry and by simulation

**1. An artefact, and what it shows.** At the d=4 optimum, the levels 2–3 bucket law π had drifted to corners (π_N ≈ 0 and ≈ 1). The conditionals didn't follow, which gave code rates r12 = 34n and 128n.

This is harmless. Only codewords whose type equals Q_λ = Σ_t τ_t·cond_t ever contain anything. Setting π = Q_λ leaves entries, passing and T **unchanged** (0.27454 → 0.27454), and the code rates become r12 = 0.146 / 0.128 / 0.007 / 0.0002 at levels 1–4. So **the sparse deep merges (levels 3–4) are essentially unfiltered.** The filtering that matters is at levels 1–2, which are dense. The gain from depth comes from smaller lists in a deeper tree, with filters making the level-1/2 merges cheap.

**2. Symmetry argument.** The real filter's pass rule (bucket membership by the joint (digit, label) type of (x, λ), with random iid codewords) is invariant under coordinate permutations. Outputs are kept only if they have the exact parent type. All parents of that exact type are images of each other under permutations, and their representation sets map onto each other, joint types included. Over the random instance a and the random code, every valid parent therefore has the same survival distribution. So:
- P(planted parent survives) = E[σ] exactly, at every n.
- Atypical joint types can change list sizes, and the worst-case passing bound covers that. They cannot make the solution's parent survive less often than the average valid parent.

**3. Simulation** (`floor/bias_sim.py`, n = 32):
- The setup is the level-2 merge shape: children have one −1 and five +1, the parent has one −1 and nine +1, with one (+1,−1) cancellation.
- R = 5544 reps, M = R/2, complete coset lists of about 1930 elements each.
- The filter uses the integer-rounded level-2 conditionals of the optimum, with K codewords and K·p_pair = 1.

| 300 draws | mean σ | P(planted survives) |
|---|---|---|
| filter off (control) | 0.8638 | 0.8633 ± 0.020 |
| filter on | 0.7150 | 0.7200 ± 0.026 |

Passing pairs split 0.5000 / 0.5000 between the two mirror pair classes (0.5000 before filtering). The filtered/unfiltered output ratio is 0.828. Planted survival matches σ within noise in both arms.

**4. The `filter_terms` items you asked about:**
- **Entries ≤ T.** Rows (L + r12 − r1, L + r12 − r2) ≤ T are in the LP at every level. Bucket decoding is the open item. It needs list-decodable codes (Dubiner/BDGL-style product codes) with decoding cost ≈ output. That's standard asymptotically, but with r12 ≤ 0.15 after the π fix the codes are small anyway.
- **Pass probability at the solution's type.** r12 = Σ_t τ*_t·KL(cond_t‖π) is the exponent at the valid pair type τ* of the level. K = 2^{r12 n} gives Θ(1) expected common buckets for a τ*-type pair, so it is evaluated at the solution's joint type, not at an averaged or optimised one.
- **Digit-2 mass → 0.** At level 4 the digit-2 mass is exactly 0. At levels 2–3 it is 0.001, which is empty at small n. The filter there is nearly trivial (r12 ≤ 0.007 at level 3), so empty or non-integral type classes don't affect the result. The asymptotic formula only needs non-empty classes of positive mass.

## C. Block hybrid: 0.276, which beats BBSS (0.283) but not 0.2733

Model: guess (1−β)n coordinates, giving 2^{(1−β)n} completions (there is nothing to exploit to prune them). Each guess is one CVP on the fixed βn-dimensional block lattice {y : ⟨a_B, y⟩ ≡ 0 mod 2^n}, of determinant 2^n.
- The centred target distance relative to GH is 2.066·2^{−1/β}. That is 1.033 at β = 1 (decoys) and drops below 1 for β < 0.954.
- I used Ducas–Laarhoven–van Woerden, *The randomized slicer for CVPP* (PKC 2020, ePrint 2020/120), Heuristic claim 4. A batch of ≥ 2^{0.058m} CVP instances on one lattice costs 2^{0.292m} time and 2^{0.208m} memory in total, with one sieve as preprocessing and 2^{0.234m} amortised per instance.
- T(β) = max(0.292β, (1−β) + 0.234β), minimised where the batch condition is tight, (1−β) = 0.058β: **β = 1/1.058 = 0.945, T = 0.292/1.058 = 0.2760, memory 0.197.** The target there sits at 0.99·GH.

So a lattice hybrid beats unfiltered BBSS (0.2829) and BCJ, but loses to deep filtered BBSS (0.2733). As far as I can tell nobody has written down the "lattice + guessing" density-1 figure of 0.276. It deserves a sentence if we ever write this up, with the heuristic caveats: the Gaussian heuristic and the slicer's rerandomisation heuristic.

Two refinements I haven't done:
1. The DLvW red curve: larger memory (up to 2^{0.5m}) with larger batches lowers the amortised query cost, but needs a list longer than (4/3)^{m/2}, which a single sieve does not give.
2. Guessing only part of the residual, i.e. combining a representation tree on the guessed coordinates with the lattice. MitM on the guess needs Babai additivity, which fails here because det^{1/m} = 2^{1/β} is constant.

## Lattice baseline update

The fpylll BKZ-30 + enumeration runs for n = 50/55/60 are done (10/10 solved each). n=65 is running. They grow as about 2^{0.7n}, the cost of enumeration, so they say nothing about the sieve exponent.
