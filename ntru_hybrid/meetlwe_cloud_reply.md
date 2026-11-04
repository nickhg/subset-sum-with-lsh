# cc → wc: Meet-LWE cloud run results (handoff25 deliverable)

The run used 96 workers on c7i.24xlarge (spot) for about 9 h. The instance terminated itself at 09:58 UTC on 4 Nov.
The keys were 6 ω × d 3–7 × {unfiltered, filtered}, sharing bests. Points are in `ntru_hybrid/points/`.
`make_ml_numbers.py` generates the paper's macros and table from them.

## Checks (handoff26 1–4): all pass
1. `ml_recost.py` (the independent evaluator) agrees with `meetlwe_model` to 1e-6 on all 60 best points
   (`runs/ml_check_final.log`).
2. Every unfiltered point, run through `may_rep1.may` (May's §7 formulas, with ε_j read off the point), gives the same T
   to 1e-6.
3. Corner flags: no digit or pair-type masses below 1e-4 at any best. One flag: the filter at merge 3 is inactive at
   ω = 0.3, d3, f. That is harmless, since merge 3 is then an unfiltered merge, and it is not the best point at that ω.
   - Binding terms: in no case is the gain carried by the leaves or the root. The binding set is always merge 2 (the
     merge of the level-2 lists) plus entry/merge terms further down. The root (merge 1) binds only as an entry term at
     ω = 0.5, d5.
   - At ω = 0.667 (d6): the binding terms are entry2, merge2 and entry5. These are ordinary internal merges,
     p = −0.225 −0.177 −0.067 −0.025 −0.010 −0.002.
4. The bias sim is shaped like the binding level-2 merge at ω = 0.5 (`bias_sim_meetlwe2.py`): parents (4,4),
   children (3,3), one cancellation of each sign, n = 20, q = 67, r = 2, complete cosets, 400 draws.
   - Planted survival is 0.682 ± 0.023 against σ = 0.650 without filters, and 0.507 ± 0.025 against σ = 0.486 with
     filters. The ratio with/without filters is 0.744 for the planted parent and 0.748 for σ.
   - On your same-sign question: the baseline already uses 1 + (N−1)/q^r. A control run without filters
     (`runs/bias_sim_meetlwe2_control.log`) gives:
     - unplanted E|O|/E|V_t| = 0.6512 ± 0.0011;
     - planted, 1,600 fresh draws: 0.641 ± 0.012, now 0.9 SE *below*.
   - So the +0.03 was noise.

Extra check: May's own parameters with filters, split laws fixed, only the filters optimised (`ml_fixed_law.py`,
ω = 0.5, his depth 4). This gives 0.354823, exactly the unfiltered value: **no gain at all**. The paper uses this in
"Where filters do not pay".

## Results

| ω | May Table 5 | May re-opt. (his depth 4 / 5 / 6) | ours unfiltered, d = 3..7 | ours filtered, d = 3..7 | gain |
|---|---|---|---|---|---|
| 0.3 | 0.298 | 0.2972 / 0.2975 / 0.2975 | 0.2972 0.2975 0.2975 0.2975 0.2975 | 0.2936 0.2922 0.2917 0.2915 0.2915 | 0.0057 |
| 0.375 | 0.323 | 0.3208 / 0.3206 / 0.3206 | 0.3208 0.3206 0.3206 0.3206 0.3206 | 0.3177 0.3092 0.3082 0.3076 0.3076 | 0.0131 |
| 0.441 | 0.340 | 0.3393 / 0.3369 / 0.3369 | 0.3393 0.3369 0.3369 0.3369 0.3369 | 0.3364 0.3219 0.3198 0.3197 0.3197 | 0.0172 |
| 0.5 | 0.356 | 0.3548 / 0.3511 / 0.3511 | 0.3548 0.3511 0.3511 0.3511 0.3511 | 0.3518 0.3352 0.3343 0.3343 0.3343 | 0.0168 |
| 0.62 | 0.389 | 0.3878 / 0.3877 / 0.3877 | 0.3878 0.3877 0.3877 0.3877 0.3877 | 0.3830 0.3708 0.3701 0.3699 0.3698 | 0.0179 |
| 0.667 | 0.407 | 0.4068 / 0.4068 / 0.4068 | 0.4068 0.4068 0.4068 0.4068 0.4068 | 0.3970 0.3843 0.3843 0.3843 0.3843 | 0.0226 |

- **Depth convention:** our d = May's depth − 1.
- **Gain:** best unfiltered (any depth) minus best filtered. Against unfiltered at the same depth it is the same or
  larger, because unfiltered values are flat beyond d4.
- **Monotonicity:** unfiltered at ω = 0.3 is not monotone (d3 0.2972 < d4 0.2975). Under May's accounting a trivial
  bottom level is not an exact copy, unlike the subset-sum BBSS accounting.

**Where filters pay most:** the gain grows with ω: 0.006 at 0.3, 0.013 at 0.375, and 0.017–0.023 from 0.44 up. Denser
keys produce denser levels with more 0 → (1,−1) cancellations, and so more pattern waste.

**Depth once filtered:**
- Unfiltered trees stop improving at d4, or at d3 for ω = 0.3 and 0.667.
- Filtered trees improve to d5–d7. Most of the gain is already there at d4, and d5→d7 adds about 0.001 or less.
- So filters do make depth pay here, but the depth effect is modest. Most of the gain comes from being able to use
  denser, more wasteful upper levels at all.

The paper's section (`paper/meetlwe_section.tex`) is on, by Nick's decision. Its numbers are generated from these
points.
