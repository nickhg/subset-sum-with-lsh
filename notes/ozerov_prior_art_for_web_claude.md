# CC → Web Claude: the BBSS "CF" entry is May–Ozerov consistency filtering (31 Oct, ~20:40)

## Sources (fetched by CC)
- BBSS arXiv 2002.05276v4. The 0.287 / {−1,0,1} / CF row cites **[38] = I. Ozerov, *Combinatorial Algorithms for
  Subset Sum Problems*, PhD thesis, Ruhr-Universität Bochum, 2016** (advisor A. May). The full text is at
  https://d-nb.info/1089007094/34 (128 pp).
- BBSS footnote 5: "Alexander May has informed us that the thesis [15] contains unpublished results using more
  symbols, with the best exponent of 0.2871 obtained with the symbol set {−2,−1,0,1,2}". Here [15] = E. Böhme,
  *Verbesserte Subset-Sum Algorithmen*, Master's thesis, RUB 2011. Not checked whether that used filtering.

## What the thesis does
- **§2.2 "Consistency Problem".** Given lists L1 ⊆ Zⁿ[w1] and L2 ⊆ Zⁿ[w2], output the pairs with a prescribed joint
  distribution Γ. That is exactly our "find the splits of type σ".
- **Algorithm `ConsistencySieve` / `ConsistencyRecursive`** (attributed to [Dub10, MO, MO15]):
  - split [n] into t blocks;
  - in each block pick a random half J;
  - keep the list vectors with weight distribution h1 (left) or h2 (right) on J;
  - recurse over the blocks, then finish naively.
  - It has a coverage lemma (I-lemma, J-lemma) and rigorous analysis under a "concentrated lists" assumption.
- **This is a type-class filter** with a binary label of marginal (½, ½) and asymmetric pass types h1, h2. Our
  level-1 optimum has Q_Λ = (0, ½, ½), i.e. exactly this.
- **§5.1, results from [MO] = A. May, I. Ozerov, "Solving knapsacks in 2^{0.287n}" (unpublished):**
  - MO.1: HGJ → **0.329** (their HGJ baseline is 0.340), "by finding inconsistent vectors more efficiently";
  - MO.2: BCJ → **0.287**.
- **The open question at the end of §5.1, verbatim:** "One possibility could be to introduce new components like 2 or
  -2 in order to increase the number of representations on the top level. Another possibility could be to try to
  improve the underlying inconsistency algorithm for the zeroAND Problem and its generalizations."
- **BBSS's own caption** says CF is "not studied in this paper".

## Consequences
1. Filtering inconsistent pairs at merges is **May–Ozerov's idea**, not new with us and not new from OAI26. The draft's
   "Our contribution" and "Origin of the idea" paragraphs claim too much as written.
2. Our genuine contribution is narrower:
   - answering Ozerov's open question: his filtering on the BBSS {−1,0,1,2} tree with BBSS accounting gives
     0.2829 → 0.2793;
   - a slightly more general filter (any label alphabet and label law) with the clean criterion
     I(X;Λ) + I(Y;Λ) > I(XY;Λ);
   - two-level simulations of the heuristic.
3. **Ladder comparison.** Ours gives HGJ 0.3269 vs MO.1 0.329, and BCJ 0.2864 vs MO.2 0.287. The accounting differs
   (their HGJ baseline is 0.340, not 0.337), so **we must not claim a better filter** until both are run under the
   same accounting. Their binary-halves filter is a special case of ours, so ours should be at least as good under
   equal accounting.
4. A May–Ozerov citation would point to an unpublished manuscript; citing the thesis is safer.

CC has *not* yet changed the paper's framing; that is Nick's decision.
