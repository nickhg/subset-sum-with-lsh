# wc → cc: handoff9. Review of the compiled main.pdf (2 Nov 2026, 20:26 build)

I checked the numbers against your run reports and the survival recursion against Tables 3, 5 and 6. All three points satisfy s_j = min(0, ρ_{j+1} − c_{j+1} + 2s_{j+1}), and the root conditions are tight: 0.1185, 0.1177, 0.0987. The gain decomposition (0.0038 + 0.0067 = 0.0105, i.e. 36% / 64%) is consistent. OAI26 is already gone. The issues are below, most important first.

## 1. False sentence about code rates  [HIGH]
§3, "Decoding the filters": "At the reported optima I(XY;Λ) ≤ 0.17 (Table 3)." That holds for d=4, but not for d=5 (level 5: 0.2115) or d=6 (level 6: 0.2829). Change it to the true maximum over all reported points, or say "≤ 0.17 at depth 4 and ≤ 0.29 at depths 5–6". Prop 5 doesn't need the codes to be small anyway, so you could simply drop the clause.

## 2. "Deep levels essentially unfiltered" only holds at d=4  [HIGH]
In §5 "Structure of the optimum" (and in my own earlier summaries): at d=5 and d=6 the **deepest** merge is heavily filtered (I = 0.21, 0.28). It is also extremely sparse: at d=6, δ_6(1) = 0.0003 while δ_6(2) = 0.0137 and δ_6(−1) = 0.0199, so the bottom level is mostly 2s and −1s split from the level-5 1s via 1 → (2, −1). Please:
- restrict the "levels 3–4 trivial" statement explicitly to the d=4 point;
- add a sentence on the d=5/6 structure: filtering at the dense top levels **and** at the sparse bottom level, where 1 → (2, −1) splits dominate;
- note that Lemma 6 covers bias at every level, including these sparse ones. It is the reason we don't need a separate sparse-level argument;
- (optional, cheap) rerun the bias simulation shaped like the d=6 bottom merge (rare 1s, 2s and −1s), as a check in the regime where the filter is now strongest.

## 3. Prop 5 proof: make one point explicit  [MEDIUM]
The construction is fine. Since a vector can only enter a tuple whose block marginals equal its own block types, vectors with atypical block types enter **no** family (families exist only for near-typical patterns), and each vector enters only the family of its own pattern. That is what keeps atypical vectors from blowing up the entry cost. Please say it in one sentence. Also note that the concentration bound for a *fixed* vector (Chernoff per block, ε = n^{−1/4} log n) gives atypical-pattern probability 2^{−Θ(log² n)}. The atypical vectors cost nothing because they enter nothing, and the valid pairs lost this way are an o(1) fraction.

## 4. Stale or inconsistent text  [MEDIUM]
- §8 Conclusion: "Open: filter decoding in full (Section 3)". Prop 5 now handles it. Change to "a full proof of the concentration step in Proposition 5", or drop it.
- §5 "Label sets": fill in the result. With a 4-symbol label set, d=5 gains only 0.0001 (0.273224 vs 0.273335), so the 3-symbol filters appear essentially optimal.
- §5 "Wider digit sets": fill in the final values. Resolve the "[todo: does re-optimisation keep −2 mass positive?]" from the {−2,…,2} runs. State that {−4,…,4} did not converge and was stopped.
- §8: "whether wider digit sets add more than ≈ 0.0005". Update once final.
- Table 1 lists BBSS as 0.2830 (published) while Table 2 recomputes 0.2831. Add a footnote: "our recomputation of [6] gives 0.2831".
- Remark (a): "Bernstein's LWE attack [todo: check ref]". Find the right citation (the hybrid / "how to attack LWE with guessing" lineage), or drop the attribution and cite KKMN25 only.
- Bib [15]: fill in the authors' initials. Bib [9]: venue.

## 5. Li  [handoff8]
[17] Li is in the bibliography but not cited anywhere in the text yet. handoff8 adds the neutral sentence. Make sure it lands in Related work.

## 6. Abstract
Fine as is. Once item 1 of handoff6 is resolved (strict-accounting runs), check that "the filters remove the reason why deeper trees did not help" is still accurate. If the strict runs show depth gains only under BBSS accounting, change it to "filters, under the BBSS accounting, remove…".
