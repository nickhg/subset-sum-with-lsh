# wc → cc: handoff6. Review of paper/main.tex (draft of 2 Nov 2026)

The draft is in good shape and the tone is right. Below are the changes I'd make, most important first. Items marked **[Nick]** need his decision; don't change those without him.

## 1. Ozerov's depth observation — must be pinned down  [HIGH]
The intro says "Ozerov makes the same observation for ternary trees [§4.1]". The story only works if that observation was made for **unfiltered** trees, or for filtered trees at a different accounting.
- Check Oze16 §4.1: was the "more levels don't help" remark made for his *consistency-filtered* ternary trees?
- If yes, we must explain why our filtered {−1,0,1} tree does improve with depth (0.2852 at d=3 → 0.2814 at d=4 under B2). Is it the BBSS accounting (c > ρ) rather than the filters? If so, the framing changes to "filters + BBSS accounting".
- Either way, add our {−1,0,1} filtered rows (d=3, d=4) to Table 1 next to Ozerov's 0.287, with a note that the accounting differs (BBSS vs strict) and the strict-accounting value for comparison. Ozerov already filtered HGJ/BCJ trees, so the novelty is specifically: filters on the {−1,0,1,2} digit set, plus depth > 3. The abstract and contributions should say exactly that.

## 2. Symmetry lemma: state the residue hypothesis precisely  [HIGH]
In the planted model the right child's residue is t − τ, and t = ⟨a, x₀⟩ depends on a. The lemma is still correct, but the proof should say why:
- At every node, the node's residue is **marginally** uniform and independent of a, because τ is uniform and independent of (a, x₀), so t − τ is too. Descendants' residues are functions of the node residue and fresh independent randomness.
- The planted parent P* is a function of x₀ and the split choices, so it is independent of a. Then the lemma applies to P* at each node.
- The *joint* dependence between sibling residues (τ and t − τ) is exactly what the lemma does not cover. Point to the sibling-independence experiment as the check for it.
Add 2–3 sentences to the proof covering this, and say "per node" in the statement.

## 3. Filter decoding is a real gap, not a todo  [HIGH]
Theorem 1 is stated "modulo filter decoding". A referee will push on this. Please write out the standard argument:
- Product (block) construction: split the coordinates into b = Θ(log n) or ω(1) blocks. In each block, take a random code of the per-block type. A filter is a tuple of block codewords whose types sum to Q_Λ (enumerate type-splits across blocks; there are 2^{o(n)} of them).
- Decoding: per block, list the codewords a vector enters (a block code has size 2^{O(n/b)}). Then combine by a tree or meet-in-the-middle over blocks, at cost ≈ output + 2^{o(n)}.
- Concentration: show that per-block types of a random typical vector deviate by o(n) total, so the entry probabilities match Lemma 2 up to 2^{o(n)}.
Cite Dubiner's and BDGL's block constructions for the template. If this is already in Nick's parked note (open item 1), reuse it.
Then drop "modulo filter decoding" from the theorem, or keep it as an explicit Heuristic 3 if the argument isn't airtight.

## 4. Constant-fraction miss per filtered merge  [MEDIUM]
With F = 2^{I(XY;Λ)n} filters, a valid pair shares Θ(1) filters in expectation, so a constant fraction of valid pairs is missed at each merge. Either draw a polynomial factor more filters, so the miss probability is o(1), and say so, or note that the constant loss over d ≤ 6 levels is absorbed in Õ. One sentence after Proposition 3.

## 5. Li's 0.24 claim  [Nick]
Right now Li is cited in the bibliography but only discussed under the optional flag. Even if the full analysis stays out, a referee will ask, so I'd add one neutral sentence to the related work regardless. For example: "Li [Li25] claims 2^{0.24n} with a ternary-tree structure; we have not been able to reproduce this within the heuristics used here" (adjusted to whatever the literature search found). **Nick to decide the wording.**

## 6. The OAI26 sentence  [Nick]
"We came to these filters through the asymmetric filtering … of [OAI26]." Nick: is that how it happened? Your parked LSH-filtered BBSS note predates this. If the sentence isn't accurate, or you'd rather not say it, drop it. cc: please verify that the OAI26 reference exists as cited (title, date). Otherwise mark it \todo{check ref}.

## 7. Smaller edits
- Remark 4 (π = Q_Λ): move the parenthetical about π drifting to "34n and 128n" into the appendix or a footnote. It's an internal-model detail and reads oddly in the main text.
- Abstract: "the filters remove the reason why deeper trees did not help". Make this consistent with item 1 once resolved.
- Introduction: say explicitly which prior work filtered what. "Filtering representation trees: Ozerov (HGJ, BCJ digit sets, d ≤ 3). Filters + depth in decoding: Both–May. New here: {−1,0,1,2}, d ≥ 4, and the soundness analysis."
- Table 3 caption: define every column once. "Pairs", "passing" and "saving" are currently spread between the caption and the text.
- Theorem 1: say "depth \Tbestdepth" and also give the depth-4 value as the simplest good instance, since d=6 is still polishing.
- Section 6, survival paragraph: fill in the table from floor/runs/survival_*.log.
- The **[Nick]** todos for the definition of (m,τ,w)-set and the d vs k convention: leave them for Nick.

## 8. Please also send
- `paper/litsearch.md` (the literature-search deliverable). I haven't seen it yet, and items 1 and 5 depend on it.
- The compiled PDF, once numbers.tex is generated, so Nick can read it on his phone.
