# cc → wc: results on the floor / survival / lattice handoff (2 Nov 2026)

Code is in `floor/`, logs in `floor/runs/`. All exponents are per n, log2.

## Headline (please check this first)

**Deeper filtered BBSS trees beat 0.2793.** This uses the same model (`gen_lsf.Model.lp`, BBSS accounting with type-class filters at every merge) that produced our parked 0.2793 at depth 3:

| {−1,0,1,2}, BBSS accounting | d=3 | d=4 | d=5 | d=6 |
|---|---|---|---|---|
| no filters (B1) | **0.2831** | 0.2841 | 0.2898* | 0.2897* |
| filters (B2) | 0.2793 (earlier `gen_opt`) | **0.2749** | **0.2734** | ≤ 0.2734 (warm start from d=5) |

\* These are optimiser failures. Deeper trees can't be worse in principle; the true values are ≤ 0.2831.

- **Without filters**, depth 4 doesn't help, which is BBSS's own finding.
- **With filters**, the deep merges become cheap. At d=4 the filtered-pairs cost binds at every level 1–4 (all ≈ 0.2749), and the level-1 list is 0.236.
  - d=4 split laws: levels 1–4 are 2:0.007/0.002/0.001/0.
  - Constraint bits c: 0.873 / 0.726 / 0.457 / 0.182, with reps ρ = 0.995 / 0.665 / 0.457 / 0.182. Level 2 has c > ρ, which BBSS Heuristic 1 permits.
  - Reproduce with `python3 floor/recursive_floor.py -1,0,1,2 4 B2`, or `M.report` on `floor/runs/rf_-1_0_1_2_d4_B2.npy`.
- **{−1,0,1} with filters, depth 4: 0.2814.** BCJ digits plus filters beat unfiltered BBSS (0.2829).
- `handoff_for_cc.md` said "depth 4 is untested", and that is exactly the gap these numbers fill.
- Polishing runs (`gen_opt`, warm start, 3 h each) are in progress for d=4, 5, 6 and for ternary d=4.

**My view:** this is a ~0.01 gain over BBSS, not 0.004. Nick's "non-result" verdict should be revisited, but **only after** someone independently re-checks that the filter cost (`filter_terms`: entries and passing) is still valid at the sparse deep levels. The levels where digit 2 almost vanishes (level 4, for example) are where I'd look for a hole. Heuristic 2 was only tested by simulation on HGJ-type merges (`sim_merge.py`). A depth-4 small-n simulation of a filtered merge between two sparse ternary levels would be the cheap test.

## Task 1: recursive floor, d = 1…6

Variants, each one adding a cost term (T is the max of all included terms):

| Variant | Accounting | What's included |
|---|---|---|
| F0 | strict (c_j ≤ ρ_j, nested) | list sizes only, your "floor" |
| F0L | strict | lists plus leaf build H_d/2 |
| F1 | strict | lists, leaf build, and unfiltered merge pairs |
| F2 | strict | F1 with type-class filters |
| B1 | BBSS | merges, no filters |
| B2 | BBSS | merges with filters |

| D | var | d=1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| {0,1} | F0 | .3113 | .3113 | .3113 | .3113 | .3113 | .3113 |
| | F0L | .4056 | .3113 | .3113 | .3113 | .3113 | .3113 |
| | F1 = B1 | .4056 | **.3371** | .3371 | .3371 | .3371 | .3371 |
| | F2 = B2 | .4056 | .3269 | .3269 | .3269 | .3269 | .3269 |
| {−1,0,1} | F0 | .1728 | .2020 | .2034 | .2034 | .2034 | .2075* |
| | F0L | .4056 | .2916 | .2555 | .2359 | .2244 | .2178 |
| | F1 | .4056 | .3034 | **.2909** | .2913 | .2914 | .2913 |
| | F2 | .4056 | .3037 | .2898 | .3241* | .2895 | .3024* |
| | B1 | .4056 | .3122 | .2892 | .2896 | .2896 | .2898 |
| | B2 | .4056 | .3122 | .2852 | **.2814** | .2821* | .2829* |
| {−1,0,1,2} | F0 | .1701 | .1979 | .2016 | .2012 | .2028 | .2088* |
| | F0L | .4056 | .2916 | .2555 | .3113* | .2522 | .2331 |
| | F1 | .4056 | .3025 | .2873 | .2889* | .2949* | .3298* |
| | F2 | .4056 | .3042 | .2888 | .2955* | .2993* | .3159* |
| | B1 | .4056 | .3025 | **.2831** | .2841 | .2898* | .2897* |
| | B2 | .4056 | .3029 | (crashed; 0.2793 from earlier) | **.2749** | **.2734** | ≤ .2734 |

\* Optimiser failure (the value rises with d). Read the true value as ≤ the best shallower value. The minimal d=1 tree has no merge to build its lists, so the d=1 rows of F0L–B2 are just the cost of the leaf build.

Sanity checks:
- d=1 F0 reproduces your table (0.3113 / 0.1728 / 0.1701).
- {0,1} F1 gives HGJ 0.3371, {−1,0,1} F1 d=3 gives BCJ 0.2909, and {−1,0,1,2} B1 d=3 gives BBSS 0.2831 (published 0.2829).

**Answer to the key question:**
- **List sizes alone never get near 0.28.** F0 sits at 0.20–0.21 for every depth and digit set.
- **Lists plus leaf build go down with depth**, to 0.22–0.23 at d=6.
- **Merges supply the cost.** The 0.21 → 0.28–0.29 gap is entirely merge cost; the lists don't account for it.
- With unfiltered merges the floor really does climb to 0.287 (strict) and 0.283 (BBSS) for {−1,0,1,2}, so unfiltered BBSS is essentially optimal among representation trees.
- **With filters it does not stop at 0.2793.** It keeps falling with depth (above).
- **Binding level:** at the B2 optima the filtered merge cost is tied across levels 1–4. At B1/F1 optima it is levels 1–2 (the h-hump) plus the leaf build.

**Flag against the chat claims:** "uniform drops (σ < 1) never help" is true for the first-level floor, but false for the full tree. B1 < F1 from d=3 on (0.2831 vs 0.2873) only because BBSS accounting allows c_j > ρ_j.

## Task 2: survival in a real HGJ tree

`floor/survival.py`: depth 3, weights n/2 → n/4 → n/8 → n/16, leaf c ≈ 3.9, internal c ∈ {1,2,3,4}. Leaves are complete enumerations.

| n | c | σ lvl2 (Poisson) | σ lvl1 (Poisson) | P(S found) (Poisson) | log2 work | log2 work / success |
|---|---|---|---|---|---|---|
| 48 (40 draws) | 1 | .953 (.98) | .593 (.618) | .15 (.32) | 18.6 | 21.3 |
| | 2 | .954 | .823 (.856) | .65 (.77) | 19.9 | 20.5 |
| | 3 | .943 | .906 (.943) | .975 (.93) | 20.8 | 20.8 |
| | 4 | .957 | .957 (.979) | 1.00 (.98) | 21.4 | 21.4 |
| 64 (10 draws) | 1 | .963 | .602 (.617) | .30 (.32) | 23.5 | 25.3 |
| | 2 | .967 | .841 (.853) | .50 (.77) | 25.0 | 26.0 |
| | 3 | .953 | .928 (.944) | .90 (.93) | 25.9 | 26.1 |
| | 4 | .964 | .972 (.978) | 1.00 (.98) | 26.6 | 26.6 |

- **Poisson is slightly optimistic everywhere.**
  - At level 2, σ is 0.95–0.97 against a predicted 0.98, at every c.
  - At level 1 it is 0.01–0.04 low.
  - The c=2 success rate is clearly low (0.50–0.65 vs 0.77), so failures are correlated across the two root siblings.
- **c=3 does not decay.** It plateaus at 0.91–0.93, so there is no evidence of strong sibling-split correlation.
- **Conservation holds to within about 1 bit.** Work per success is flat between c=2 and c=4, so raising c buys nothing, as you predicted.
- **Caveats:**
  - The tree is only depth 3, so this is not a deep-plateau test.
  - At n=64, N is capped at 2^56 (density 1.14), so "any solution" is always 1.

## Task 3: lattice at density 1 (fpylll only, no G6K)

`floor/lattice_baseline.py` uses the centred CJLOSS embedding on the **integer** instance. A modular row (0 | K·2^n) is wrong here: it puts (2e_i | 0) into the lattice. The pipeline is BKZ-30 followed by enumeration of every vector with norm² ≤ n.

| n | solved | enum time (median) | short vectors ±, mean (odd λ / even λ) |
|---|---|---|---|
| 50 | 10/10 | 3.3 s | 1.8 (1.5 / 0.3) |
| 55 | 10/10 | 40 s | 2.9 (2.3 / 0.6) |
| 60 | 10/10 | 440 s | 2.5 (1.6 / 0.9) |
| 65+ | running | | |

- **Decoys are a handful**, consistent with 2^{0.047n} (5–7 at these n) for the coset. There is no sign of the 2^{0.063n} kernel count, which is the λ = 0 count around the origin, not the ½-centred coset.
- **Flag:** your "1.0629" is the Mazo–Odlyzko count of Z^n points with λ = 0 and origin centre. For the coset centred at ½ the Z^n count is 1.0 and the Gaussian heuristic gives 1.047.
- **Time** grows as about 2^{0.7n}, the cost of enumeration with weak preprocessing. That says nothing about the sieve exponent.
- **Literature:** I found no paper that states a density-1 sieving exponent. My own derivation is that the target is about 1.033·GH with polynomially many to 2^{0.047n} decoys, so the cost is that of SVP/CVP in dimension n: 0.292 time and 0.2075 memory (BDGL). Your claim is plausible, but it is a back-of-envelope estimate, not a citation.

## Task 4: per-level hybrid (model only, `floor/hybrid_model.py`)

- A node built by lattice instead of merging costs at least max(0.292, lattice points − m). Lattice points is the larger of the GH count and the Mazo–Odlyzko Z^n count.
- **That is ≥ 0.292 at every level and every m**, so a full-dimension lattice step never beats BCJ (0.2909), let alone 0.2793 or 0.273.
- Decoy excess over the true list is 0.03–0.05 across p.
- **Only a block hybrid could help:** a lattice step in dimension βn costs 0.292β. I haven't modelled that yet.
- I skipped the small-n G6K test, since the model shows no gain.

## Task 5

Skipped. Task 1 shows no sharp drop in α at ω ≠ ½ that would justify it.

## What I'd like from you

1. A sanity check that nothing in `filter_terms` / `lp` is unsound at deep, sparse levels. If it's sound, d=4 at 0.2749 is a real improvement over the parked note within the same heuristics.
2. Your view on whether the d ≥ 4 gain survives under strict accounting. F2 is noisy, so I'll re-run it with warm starts.
