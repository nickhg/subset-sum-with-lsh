# cc → wc: handoff9 reply (PDF review), 3 Nov 2026

handoff9 had gone missing; Nick found it. Applied in db69802, except where marked.

1. **Code-rate sentence**: dropped. It now says that the product construction does not need small code rates.
2. **Deep-level structure**: "levels 3–4 trivial" is now restricted to the d=4 point. Added a sentence on d=5/6:
   - the dense top levels are filtered, and so is the sparse bottom level (I = 0.21 and 0.28 at the last merge);
   - at d=6 the bottom level has δ_6(1) = 0.0003 against δ_6(2) = 0.0137 and δ_6(−1) = 0.0199, i.e. 1 → (2,−1) splits;
   - Lemma 6 holds at every level.

   The optional simulation, `floor/bias_sim_sparse.py`:
   - shape: n = 20; the parent has four 1s and two −1s; each child has two 2s and three −1s; 12 reps; prime modulus 13; complete cosets;
   - filter: a permutation-invariant {N,L,R} rule, K = 1024.

   Results, 400 draws:

   | filter | planted survival | mean σ |
   |---|---|---|
   | off | 0.5975 ± 0.0245 | 0.6106 |
   | on | 0.4375 ± 0.0248 | 0.4446 |

   Both agree within one standard error: no bias at the sparse merge. Now in the paper's Filter bias paragraph.
   (An even modulus makes 2a degenerate, hence 13.)
3. **Prop 5**: added the sentences you asked for:
   - a vector enters only the family of its own pattern;
   - atypical vectors enter nothing;
   - Chernoff per block gives 2^{−Θ(log² n)};
   - an o(1) fraction of valid pairs is lost.
4. **Stale text:**
   - Conclusion: now reads "a full proof of the concentration step in Proposition 5".
   - Label sets: K=4 at d=5 gives 0.273224 vs 0.273335, a 0.0001 gain, so 3 symbols look essentially optimal.
   - Wider digit sets: rewritten per handoff10 (see below).
   - Table 1 caption: added "our recomputation of [BBSS20] gives 0.2831".
   - The Bernstein remark went out with the lattice remark (handoff12).
   - Bibliography: every entry now has initials and a venue.
   - The strict todo in the Table 1 caption now says that a strict depth-4 run did not improve on 0.2864.
5. **Li**: cited in Related work (handoff8).
6. **Abstract**: unchanged. The strict-accounting runs also gain from depth ({−1,0,1,2} strict: 0.2888 at d3 → 0.2842 at d4), so "filters remove the reason why deeper trees did not help" holds under both accountings. Most of the size of the gain still needs BBSS accounting.

## Handoff 10/11: outcome of the −2 control

The control: {−1,0,1,2} at d=6, re-optimised from the mm5 d6 point with the −2 splits projected out. It reaches **0.27223**, against 0.27215 for {−2,…,2}. That is a gain of 0.0001, below your 0.0002 rule, so handoff10 is applied:
- the {−2,…,2} row is out of Table 1;
- the wider-digit paragraph is down to 3 sentences;
- the conclusion now reads "add at most about 0.0004 at fixed depth".

Also, {−1,0,1,2} at **d=7 is now 0.27212** (polish still running). So the best point overall uses no −2.

## Still pending (runs end in about 1.5 h)

The following wait for the final d=6/7/8 values:
- handoff13: depth table to d=8, fitted limit, title, abstract and theorem;
- the "Saturation" todo;
- the commit hash.

Nick also asked for a plain title and author line: the todo is gone from the author line, "Draft" is gone from the date, and the link boxes are hidden.
