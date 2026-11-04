# wc → cc: handoff25. Cloud run for filtered Meet-LWE (Nick approves the spend)

Launch **one separate** c7a/c6a.24xlarge spot instance (don't take workers from the two subset-sum machines). 8 h, self-terminating at 9 h, with the same safeguards and 15-min rsync as the subset-sum run.

## Grid
- ω ∈ {0.3, 0.375, 0.441, 0.5, 0.62, 0.667} (May's Table 5 points).
- Depths (our convention) d = 3…7.
- Both **unfiltered** (Rep-1-equivalent general split laws) and **filtered**, with May's accounting (c_j ≤ ρ_j), asymptotic (q → ∞, guessing ignored), as in meetlwe_model / ml_hop.
- Worker split: weight mid-ω (0.441, 0.5) and d = 4–6 most, since that's where the gains are.

## Method (as in the subset-sum polish)
- canonicalise logits before jittering, with random jitter scales;
- per (ω, d), restart from the global best;
- seed depth d+1 by trivial extension (exact copy) **and** by nested seeds (best d + a sparse filtered bottom level);
- share bests across workers every 15 min, so every (ω, d+1) is ≤ (ω, d).

## Post-run checks
For every best:
- recompute with ml_recost.py;
- unfiltered bests also via may_rep1.py (May's own formulas) where expressible;
- corner flags.

## Deliverable
`ntru_hybrid/meetlwe_cloud_reply.md` with a table per ω:
- May's published value;
- May's formulas re-optimised at depth 4 / 5 / 6;
- our unfiltered best;
- our filtered best (with depth);
- the filter gain against the best unfiltered value at equal depth.

Plus one sentence on where in ω the filters pay most, and whether depth keeps helping once filtered.

Still a separate note (ntru_hybrid/), not the subset-sum paper.
