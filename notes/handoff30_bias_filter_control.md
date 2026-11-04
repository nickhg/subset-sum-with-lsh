# wc → cc: handoff30 (settle the +0.02 in the filter-on Meet-LWE bias simulation)

1. **Control first** (as for the no-filter arm): filter-on merge, **no planted parent**, 1,600+ draws. Compute E|O| / E|V_t| directly, with the same coset sizes, code K and label laws.
   - If ≈ 0.505: the "expected" σ in the filter arm (0.487) is computed slightly wrong, e.g. the planted-class correction not applied consistently, or filter-entry normalisation. Fix the σ formula and re-report. Nothing changes in the paper beyond the number.
   - If ≈ 0.487: run the extra 4,000 planted filter-on draws, as you offered. Report the pooled value and SE.
2. In the paper, report whatever is final with both arms at ≥ 2,000 draws. If a small residual remains, state it in one clause ("within 2 SE; in the favourable direction").
3. Typo in the worked example: "pairenters" → "pair enters".
