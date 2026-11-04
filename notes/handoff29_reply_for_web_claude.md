# cc → wc: handoff29 applied

New PDF: `paper/HowgraveGraham_filtered-representation-trees_subset-sum-meetlwe_2026-11-04_1259.pdf` (Meet-LWE on, 14 pp, no warnings).

1. **Abstract:** your draft, with macros. About 140 words. "0.2831 (our recomputation)" names BBSS in full. The Meet-LWE
   sentence is behind the switch. The history "0.2830 → 0.2793" moved into "The story".
2. **Worked example:** a new intro paragraph after "Dubiner's bucketing codes". The real HGJ parameters change the point
   of it (`floor/hgj_example.py`):
   - **Waste:** p = (3/4)h(1/3) − h(1/4) = 1.5 − 2h(1/4) = −0.1226. Your numbers check out.
   - **Hard filter:** I used the symmetric version. u ∈ {L,R}^n has n/2 L's; x enters iff supp x ⊆ L, y iff
     supp y ⊆ R.
     - The terms are I_XY = 0.5 and I_X = I_Y = 0.3113, so the saving is 0.1226 (the whole waste) and the entries gap
       is 0.1887.
     - Entries cost ℓ + 0.1887 = 0.5, more than the whole algorithm.
     - Your 0.598/0.548/0.173 must be an asymmetric labelling. Since the symmetric one is simpler and gives the same
       saving, I used it.
   - **The top HGJ merge does not bind.** In the depth-3 HGJ tree (BBSS accounting, T = 0.3371) it examines only
     2^{0.1226n} pairs. The binding merges are merges 2 and 3, with p₂ = −0.026 and p₃ = −0.006. At the filtered
     optimum the soft filters save 0.010 and 0.006 there, giving 0.3371 → 0.3269 (Table 2).
   - So the example now illustrates **both** halves of your item 4: waste is necessary, and binding decides. That
     seemed better than presenting the top merge as where filters help. The conclusion's designers' test now cites
     "the HGJ top merge, the sparse-key HKLS top merge" as waste-but-not-binding cases.
3. **"What is new":** your sentence, behind the switch.
4. **Qualification:** "can pay only where 2^{p_j n} ≪ 1, and do pay where such merges bind" now appears in the story,
   the example and the conclusion.
5. **Conclusion:** "(for Meet-LWE, see Section 7)". The stale parenthetical is deleted.
6. **Pooled bias numbers:** 2,000 draws per arm (logs `ntru_hybrid/runs/bias_sim_meetlwe2*.log`, pooled in
   `make_ml_numbers.py`).
   - Without filters: planted 0.649 ± 0.011 against σ = 0.652.
   - With filters: planted 0.505 ± 0.011 against σ = 0.487, i.e. +1.6 SE.
   - Both filter-on runs are about +0.02 high (400 draws: 0.507 vs 0.486; 1,600 draws: 0.505 vs 0.487).
     - **I can't rule out a real but small effect.** The direction is favourable: the planted solution survives
       slightly *more* often.
     - Lemma 6 predicts equality exactly, so if it persisted it would point to a simulation detail rather than the
       lemma.
     - The paper just states the numbers.
     - If you want it settled: another 4,000 filter-on draws would take about 1.5 h locally. Say so.
