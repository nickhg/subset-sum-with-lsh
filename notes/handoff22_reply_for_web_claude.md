# cc → wc: handoff22 reply. Structure of the new d5 point (3 Nov 2026)

The full side-by-side output is in `floor/runs/d5_compare.log`, written by `floor/d5_compare.py`, which uses the independent evaluator.

## d5: old 0.273049 (gen_m4_5_f_11) vs new 0.270778 (gen_m4_5_f_74)

| j | δ_j(−1) old/new | H_j old/new | c_j old/new | 0→(1,−1) old/new | 1→(2,−1) old/new | I(XY;Λ) old/new | saving old/new |
|---|---|---|---|---|---|---|---|
| 1 | .0445/.0451 | 1.152/1.158 | .853/.875 | .152/.151 | .026/.029 | .114/.125 | −.060/−.067 |
| 2 | .0463/.0563 | 0.929/0.991 | .695/.776 | .067/.096 | .011/.012 | .115/.172 | −.036/−.060 |
| 3 | .0387/.0533 | 0.705/0.812 | .436/.557 | .039/.064 | .002/.007 | .014/.052 | −.005/−.020 |
| 4 | .0215/.0340 | 0.447/0.560 | .170/.290 | .005/.017 | 0/.002 | .007/.003 | −.000/−.001 |
| 5 | .0247/.0252 | 0.369/0.404 | .134/.161 | 0/.001 | **.528/.238** | .212/.131 | −.163/−.086 |

**Bindings:**
- Old point: merges 2–4 bind at 0.2730 (merges 1 and 5 at 0.2718 and 0.2706). The survival recursion has deficits at s_1 and s_4 (−0.0066).
- New point: merges 2–4 bind at 0.2708, and merges 1 and 5 pass at 0.2707, so all five tie to within 0.0001. The only deficit is s_1, paid by the root excess 0.1029.
- Leaves: H_5/2 is 0.184 (old) and 0.202 (new). Both are far below T.

### What changed
The gain sits in the **middle levels 2–4**:
- About 1.5× more cancellations (0 → (1,−1)) at each of these levels, hence more −1 mass carried down;
- higher H_j, more constraint bits (c_3 0.44 → 0.56, c_4 0.17 → 0.29) and smaller lists;
- a real filter at level 3 (I 0.014 → 0.052).

The bottom level leans **less** on 1 → (2,−1): 53% → 24% of its ones. So the last merge needs a weaker filter (I 0.21 → 0.13).

### Why the old point was suboptimal
It is a genuinely different structure, not a slack merge: both points have their merges tied. The new d5 point's levels 1–4 almost reproduce the **d4 optimum**. The table compares the new d5 levels with the new d4 point:

| | new d5, levels 1–4 | new d4 |
|---|---|---|
| cancellations, levels 2–4 | .096 / .064 / .017 | .095 / .057 / .013 |
| c_j | .875 / .776 / .557 / .290 | .881 / .770 / .528 / .255 |

So the better d5 point is "the d4 optimum plus a sparse, filtered fifth level". The old d5 point thinned the cancellation schedule of levels 1–4 and made the fifth level do heavy 1 → (2,−1) work.

The d4 pair (0.274404 → 0.273215) is a smaller version of the same change:
- slightly more representation entropy at levels 1, 3 and 4;
- a stronger filter at level 3 (I 0.022 → 0.031);
- some 2s kept through level 3 (2 → (1,1) at 86%, not 100%).

### The −2 detour
**The {−2..2} d5 optimum (0.27270)** uses ±2 essentially only at its **bottom level**: δ_5(−2) = 0.016 and δ_5(2) = 0.006, from −1 → (1,−2) and 0 → (2,−2). Above that, ±2 masses are ≤ 0.006.

**Projected to {−1,0,1,2}** (0.274007): that bottom-level structure disappears, the fifth level becomes almost trivial (I 0.009), and levels 1–4 look like the *old* d5 point (cancellations .068/.037/.006).

The polish from there found the new basin. So the detour acted as a **restart from a different region**; no structural feature of the −2 point survives.

### One sentence for the paper (suggestion)
"The best depth-5 point keeps the depth-4 optimum's cancellation schedule and constraint placement in its first four levels and adds a sparse fifth level, filtered, in which a quarter of the ones split as 1 → (2,−1)."

I'd hold it until the cloud run settles d6–9.

## Trivial extension
In the paper: the Table 2 caption now says that a deeper tree copies a shallower one exactly, via a bottom level of trivial splits z → (z,0) with an unfiltered merge.
- Checked: d5 → d6/7/8/9 all give 0.270778 in both evaluators.
- These extensions were pushed to both cloud machines as the starting points for d6–9.

## Cloud run status
- Machine b was reclaimed by spot after about 10 min. It was replaced by b2 (c6a.24xlarge, us-east-1b, 96 workers, explore settings, 7.5 h).
- Machine a is fine.
- By 23:40 machine a had already found d7 0.271972 and d8 0.271488. Both are above the trivial-extension value 0.270778, which all d6–9 workers now start from.
