# wc → cc: handoff5. Literature search, then a paper draft (2 Nov 2026)

Do the literature search (Part 1) first, because its answer can change the framing. Then draft the paper (Part 2) as LaTeX in a new folder `paper/`. Leave the running optimiser jobs alone. Where their results are still pending, put clearly marked placeholders `\todo{…}` in the draft.

Terminology (Nick's convention, please follow): say **digit set** (never "alphabet") for {−1,0,1,2} etc. Use **k-tree**, **τ-merge** and **(m,τ,w)-set** as in his earlier drafts. For filter labels say **label set**.

---

## Part 1. Literature search  [do first]

Goal: establish whether anyone has already (a) combined locality-sensitive / near-neighbour filtering (Dubiner, May–Ozerov, BDGL-type) with BBSS or other representation trees for **subset sum**, or (b) observed that filtered merges make depth > 3 pay.

1. Read the related-work and optimisation sections of these, and record each one's digit set, depth, whether merges use near-neighbour or filtering, and the claimed exponent:
   - HGJ (EUROCRYPT 2010)
   - BCJ (EUROCRYPT 2011)
   - BBSS, *Improved classical and quantum algorithms for subset-sum* (ASIACRYPT 2020, ePrint 2020/168)
   - Esser–May, *Low weight discrete logarithms and subset sum in 2^{0.65n} with polynomial memory* (EUROCRYPT 2020)
   - Esser–May, *Better sample – random subset sum in 2^{0.255n}…* (arXiv 1907.04295). **Check its status carefully**: errata, retractions, or follow-ups disputing the 0.255.
   - May–Ozerov (EUROCRYPT 2015)
   - Both–May (PQCrypto 2018)
   - Dubiner (IEEE IT 2010)
   - BDGL (SODA 2016)
2. Search ePrint, arXiv and Google Scholar for 2020–2026 work on: "subset sum" + "locality sensitive" / "near neighbor" / "filter" / "representation"; "ternary tree subset sum" (the MDPI 2025 paper *From Subset-Sum to Decoding: … Ternary Representation Technique*, which we think is Yang Li's 0.24 claim); "subset sum 2^{0.27"; "subset sum quantum walk representation". Also check the decoding literature (BJMM, MMT and their filtered or nearest-neighbour variants) for the same depth-plus-filter observation transferred from decoding.
3. Deliverable: `paper/litsearch.md` with:
   - a table of claimed classical exponents for random density-1 subset sum, each with its digit set, depth, filters (yes/no), heuristics, and status (accepted / disputed / retracted);
   - an explicit answer to (a) and (b), with quotes or section references wherever something comes close;
   - an assessment of the Li 0.24 claim: what the construction is, and where (if anywhere) it breaks under the BBSS heuristics or our survival accounting.

---

## Part 2. Paper draft

Tone (Nick's preference): modest and precise. This is a solid improvement within the standard heuristics: "big in our world, but not huge". No hype. Single author placeholder: **Nick Howgrave-Graham**. Leave a `\todo{authors / acknowledgements}`, because co-authorship is undecided.

Working title (Nick may change it): *Filtered merges make deeper representation trees pay: random subset sum in 2^{0.2726n}*. Update the number to the final best value.

### Suggested structure
1. **Introduction**
   - History table: HGJ 0.337, BCJ 0.291, BBSS 0.283, this work 0.2726 (d=6) / 0.2733 (d=5) / 0.2744 (d=4). Include the {−2,…,2} values if final.
   - The story: filters at BBSS's depth 3 give only ≈0.004, and BBSS showed that depth 4 doesn't help unfiltered. Together, filtered top merges make depth pay again, and the costs tie across all levels.
   - Contributions list.
2. **Preliminaries**: representation technique, digit sets, (m,τ,w)-sets, k-trees, τ-merges, and the BBSS heuristics (state them).
3. **Filtered τ-merges**: type-class bucket filters (Dubiner / May–Ozerov / LSF lineage, credited properly). Give the cost terms (entries, passing, bucket decoding) and the label set. Note the π = Q_λ reparametrisation, which shows the cost depends only on the label type.
4. **Accounting and soundness**
   - The optimisation program (variables, constraints, cost = max of terms).
   - The **survival recursion**: s_j = min(0, ρ_{j+1} − c_{j+1} + 2 s_{j+1}), root condition ρ_1 − c_1 + 2 s_1 ≥ 0. Explain why BBSS's c > ρ is sound exactly when deficits sit below excesses, and that every optimum we report satisfies it (S2 = B2).
   - The **symmetry lemma** (planted parent survives with probability exactly E[σ]), with its proof.
5. **Results**
   - Tables by depth and digit set (B1 against B2), with the best parameters in an appendix.
   - Structure of the optimum: costs tied across levels 1–4; filtering active only at the dense levels 1–2 (give the per-level savings); deep levels essentially unfiltered; the level-1 deficit (−0.064) paid for by the root excess (+0.128).
   - Gain decomposition: ≈40% from filters directly, ≈60% from the depth they make affordable.
   - Saturation with depth (0.2793 → 0.2744 → 0.2733 → 0.2726).
6. **Experimental validation**: the survival experiment (c = 1…4, n = 48 and 64; conservation within about 1 bit); the bias simulation (planted against average survival, filter on and off); sibling independence (n = 24–48, ±0.02 bits, no trend).
7. **Remarks**
   - (a) The lattice-plus-guessing figure 0.276 (DLvW randomised slicer, β ≈ 0.945, memory 0.197). Use your draft paragraph, with the heuristic caveats, citing Bernstein's hybrid, Karenin–Kirshanova–May–Nowakowski, and DLvW.
   - (b) **[OPTIONAL — Nick to decide whether to include]** The list-size floor for two-way-root, modular-filter trees (first-level 0.3113 / 0.1728 / 0.1701; recursive F0 about 0.20–0.21). Put it in a separate `\input{floor_section}` file so it can be dropped.
   - (c) **[OPTIONAL — Nick to decide]** A paragraph on the Li 0.24 claim, based on the Part 1 findings.
8. **Conclusion and open problems**: depth saturates near 0.272; the remaining gap to the list-size floor is all merge cost; non-two-way roots and non-enumerative top levels are open.
- **Appendix**: optimal parameters (digit laws, constraint bits c_j, representation counts ρ_j, filter label laws per level) for the reported points; reproduction commands and the commit hash.

### Notes
- Put every number in a macro file (`numbers.tex`) generated from the run outputs, so final values drop in automatically.
- Cite precisely; please don't invent references. Anything you can't verify gets `\todo{check ref}`.
- When done, write `paper/handoff5_reply_for_web_claude.md`: what's drafted, what's a placeholder, and the literature-search verdict on (a) and (b).
