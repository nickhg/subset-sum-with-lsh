# cc → wc: handoff5 reply (2 Nov 2026)

## Literature verdict (details in `paper/litsearch.md`)

**(a) Filters on representation trees for subset sum: yes for HGJ and BCJ, not for BBSS.**
- May–Ozerov consistency filtering is in Ozerov's thesis (2016), Ch. 2 and §4.2, building on Dubiner: HGJ 0.329 at depth u = 2, BCJ 0.287 at u = 3.
- After Cor. 65, Ozerov leaves "new components like 2 or −2" as an open question.
- BBSS Table 1 lists constraint filtering as "not studied in this paper".
- I found nothing from 2020–2026 combining filters with the BBSS tree, and no accepted classical density-1 exponent below 0.283. A 2026 quantum paper (arXiv 2608.07309) still cites 0.283 as the classical state of the art.

**(b) "Filters make depth > 3 pay": new for subset sum, with a decoding precedent.**
- BBSS Remark 4 says depth saturates quickly because "adding one more level does not change the cost of the upper levels, which will remain the most expensive". Ozerov says the same for unfiltered ternary trees (§4.1, after Table 4.6).
- In decoding, Both–May (WCC 2017 "BM17b", and PQCrypto 2018 Fig. 6) show BJMM with near-neighbour search improving up to depth 4 (full distance 0.1003 / 0.0967 / 0.0953; their own algorithm 0.0982 / 0.0926 / 0.0885). Cite it as the nearest precedent. Their near-neighbour search does approximate value matching; ours does representation-coordinate (consistency) filtering with exact matching.

**Esser–May 0.255:** arXiv v2 is withdrawn, with the comment "Issue with counting duplicate representations". No follow-up found. It doesn't apply to us: we never sample, and outputs are de-duplicated exact-type sets.

**Li 0.24:** the break is the cost model, not the heuristics. Each 3-way merge is charged at its output size. Honest costing gives 0.4439 at Li's own parameters and 0.393 re-optimised. I found no published comment on it.

## Paper draft: `paper/main.tex` (builds cleanly, 9 pages)

`paper/draft.tex` (the parked 31 Oct note) is untouched; the new paper sits beside it in the same folder.

**Drafted:**
- §1 introduction: history table, the BBSS-Remark-4 story, contributions, related work.
- §2 preliminaries: digit set, (m,τ,w)-set, τ-merge, k-tree, BBSS heuristic.
- §3 filtered τ-merges: lemma, cost proposition, the π = Q_λ remark, label set.
- §4 accounting: the LP, the survival recursion with "S2 = B2", and the symmetry lemma with proof.
- §5 results: depth table, theorem, structure of the optimum, gain decomposition, saturation.
- §6 experiments: survival, bias, siblings.
- §7(a) the lattice + guessing remark.
- Conclusion; appendix with parameter tables and reproduction notes.
- Optional parts are toggled in `main.tex`, both **off**: `\includefloortrue` → `floor_section.tex` (remark b), and `\includeLitrue` → `li_paragraph.tex` (remark c). Nick decides.

**Generated numbers:** `floor/make_numbers.py` re-evaluates every saved point with `gen_lsf.Model.lp` and writes `numbers.tex` (macros), `depth_table.tex` and `params_d{4,5,6}.tex`. Rerun it when the optimisers finish.

Current values:
- {−1,0,1,2}: **d=4 0.2744, d=5 0.2730, d=6 0.2726**.
- {−2,…,2}: d=4 0.2740, d=5 0.2727.
- Gain decomposition: 0.0038 from the filters (36%), 0.0067 from depth (64%). Your 40/60 was close.

**Placeholders (`\todo`):**
- Authors and acknowledgements.
- Nick's definitions of (m,τ,w)-set and k-tree. I couldn't find his earlier definitions; his subexp paper uses "k-tree" with merge levels d = 1…k, so I set k = d + 1, counting the MITM leaf merge.
- Final wide-digit values, and whether −2 mass stays positive.
- K = 4, 5 label results.
- The d = 6 / d = 7 question.
- The filter-decoding argument (I carried over the open item from the parked note).
- The survival-experiment table.
- Bernstein's hybrid reference.
- Karenin–Kirshanova–May–Nowakowski first names.
- DLdW venue.
- The commit hash.

**Terminology:** I used "digit set", "label set", "τ-merge", "(m,τ,w)-set" and "k-tree" throughout, and the word "alphabet" doesn't appear in the new draft. The parked note still says "alphabet".

**Tone:** modest. The abstract and introduction say "small at BBSS depth", credit the mechanism to Dubiner, May–Ozerov and Ozerov, cite BM17b for the decoding analogue, and make no record claims beyond "improves on 0.2830".
