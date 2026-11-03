# Literature search: filtered merges and depth in representation trees (2 Nov 2026)

Scope: classical heuristic algorithms for **random density-1 subset sum**, where t = ⟨a, x₀⟩ with x₀ ∈ {0,1}ⁿ of weight n/2 and the aᵢ uniform in [0, 2ⁿ). Exponents are log₂(time)/n. For each paper below, the sources I actually read are given (local PDF, arXiv, or ePrint text). Anything taken from memory or a search snippet only is marked *(snippet)*.

## 1. Claimed classical exponents

| Exponent (time) | Work | Digit set | Depth | Merge filters | Heuristics | Status |
|---|---|---|---|---|---|---|
| 0.5 | Horowitz–Sahni 1974; Schroeppel–Shamir 1981 (memory 0.25) | — | — | — | none | accepted |
| 0.337 (stated 0.311) | HGJ, EUROCRYPT 2010 | {0,1} | 3 | none | HGJ heuristic | accepted at **0.337**. The original 0.311 omitted the overlap waste of the top merge; BCJ (and BBSS Table 1: "0.3370 / mem 0.3113") give 0.337. Ozerov's accounting gives 0.340. |
| 0.291 | BCJ, EUROCRYPT 2011 | {−1,0,1} | 3 | none | BCJ heuristic | accepted |
| 0.329 | May–Ozerov via Ozerov thesis 2016, Cor. 64 (MO.1) | {0,1} | u = 2 | **consistency filtering** (zeroAND / ConsistentRep, Dubiner-type) | as HGJ | accepted. Unpublished as a paper; reported in Ozerov's thesis and BBSS Table 1 ("CF"). |
| 0.287 | May–Ozerov via Ozerov 2016, Cor. 65 (MO.2) | {−1,0,1} | u = 3 | **consistency filtering** | as BCJ | accepted (BBSS Table 1, row "0.287, {−1,0,1}, CF, [38]") |
| 0.2871 | Böhme, Master's thesis, Bochum 2011 (reported in BBSS fn. 5) | {−2,…,2} | ? | none? | ? | unpublished; reported only |
| **0.2830** | BBSS, ASIACRYPT 2020 (ePrint 2020/168, arXiv 2002.05276) | {−1,0,1,2} | "five levels, numbered 4 down to 0" = 4 merges, our d = 3 plus the MITM leaf half-lists | none. Table 1 marks CF as "not studied in this paper" | BBSS Heuristic 1 (lists are random subsets) | **accepted; current published record.** A 2026 quantum paper (Chukhin–Kulikov–Levitskii–Mihajlin, arXiv 2608.07309) cites 0.283 as the classical state of the art. |
| 0.255 | Esser–May, *Better sample*, arXiv 1907.04295 | {0,1}, sampled lists | ≥ 13 | none (sampling) | — | **withdrawn** (v2, 21 Oct 2019; arXiv comment "Issue with counting duplicate representations") |
| 0.24 | Y. Li, *Information* 16 (2025) 887 (MDPI) | ternary tree (3-way merges) | 3 | none | its own | **not accepted by us.** Its cost model charges a 3-list merge at its output size; see §4. No published comment or rebuttal found. |
| 0.65 (poly. memory) | Esser–May, EUROCRYPT 2020, *Low weight discrete logarithm and subset sum in 2^{0.65n} with polynomial memory* | {0,1} | — | — | — | accepted. A different regime (polynomial memory), so not comparable *(snippet / known)*. |

Background techniques, none of them applied to subset sum:
- **Dubiner**, IEEE IT 56(8), 2010: bucketing codes, the information-theoretic near-neighbour bound; the origin of type-class filters.
- **May–Ozerov**, EUROCRYPT 2015: near-neighbour search for decoding; replaces the last BJMM merge.
- **BDGL**, SODA 2016: locality-sensitive filters for lattice sieving.
- **Christiani**, SODA 2017: asymmetric locality-sensitive-filter framework.

Decoding analogues, below in §2(b):
- **Both–May**, WCC 2017 (BM17b) and PQCrypto 2018 (ePrint 2017/1139): BJMM with near-neighbour search at every level.
- **Kirshanova–May**, ePrint 2021/1255: locality-sensitive hashing in Meet-LWE merges for ternary keys, applied to values, not to representation coordinates.

## 2. Answers

### (a) Has anyone combined near-neighbour / locality-sensitive / type-class filtering with BBSS or other representation trees for subset sum?

**Yes for HGJ and BCJ, no for BBSS.**
- **Ozerov's thesis (2016), Ch. 2 and §4.2**, reporting joint work with May (cited there as [MO]), introduces the *Consistency Problem*: output the pairs of two lists with a prescribed joint coordinate distribution. It is solved by recursive block splitting with prescribed weights on random halves, explicitly building on [Dub10] (Fig. 1.2: "Corollary 25 [Dub10]"). This is applied to HGJ, giving 0.329 (Cor. 64, depth u = 2), and to BCJ, giving 0.287 (Cor. 65, depth u = 3).
- §4.2.2 says the better filter "would be already applicable to the two level case u = 2, it doesn't seem to lead to improved results", so it goes directly to u = 3.
- After Cor. 65: "One possibility could be to introduce new components like 2 or −2 in order to increase the number of representations on the top level." So the BBSS digit set with consistency filtering is posed as an **open question** there.
- **BBSS 2020**, Table 1 legend: "CF: Constraint filtering (not studied in this paper)". The 0.287 row is attributed to [38] = Ozerov. BBSS therefore did not combine CF with {−1,0,1,2}, at any depth.
- **Post-2020 search** (ePrint/arXiv/Scholar): queries "subset sum" + locality sensitive / near neighbor / filter / representation; "subset sum 2^{0.27"; "ternary tree subset sum"; "subset sum quantum walk representation"; "subset sum randomized slicer / CVPP". I found **no work** combining filtering with the BBSS tree, and no classical density-1 exponent below 0.283 other than the withdrawn 0.255 and Li's 0.24.
- Our own parked note (`paper/draft.tex`, 31 Oct) did this at depth 3: 0.2829 → 0.2793.

### (b) Has anyone observed that filtered merges make depth > 3 pay?

**Not for subset sum. Yes, in essence, for decoding.**
- **Subset sum, unfiltered.** BBSS Remark 4: "The time complexity is a decreasing function of the number of levels, which quickly reaches a minimum. In all algorithms studied in this paper, adding one more level does not change the cost of the upper levels, which will remain the most expensive." Ozerov §4.1, after Table 4.6 (classical ternary representations, u = 3): "the complexity of the computation on the bottom is always smaller than the other complexities, which means that further adaptations by increasing the number of levels doesn't lead to improvements."
  - Filters are exactly what change this: they lower the upper-level merge costs, so the extra levels become useful. Nobody has said this for subset sum. Ozerov's filtered results are at u = 2 and u = 3 only.
- **Decoding, the close analogue.** Both–May, WCC 2017, *Optimizing BJMM with nearest neighbors: full decoding in 2^{2n/21} and McEliece security* (BM17b), puts near-neighbour search into BJMM.
  - As reproduced in Both–May PQCrypto 2018, Fig. 6, BJMM-NN in full distance runs 0.1003 / 0.0967 / 0.0953 at depths m = 2 / 3 / 4.
  - The PQCrypto 2018 text: "The best known complexity for Full Distance decoding is currently 2^{0.0953n} using BJMM in depth 4 [BM17b]". Their own algorithm, with NN on every layer, gives 0.0982 / 0.0926 / **0.0885** at m = 2 / 3 / 4, and "We were not able to improve our running times for m = 5".
  - Esser (ePrint 2022/1328) *(snippet)*: Both–May "obtain their best result for a tree in depth four".
  - So in decoding, near-neighbour merges are known to make depth 4 optimal. **Difference from us:** in Both–May / BM17b the NN search replaces exact matching of syndrome bits by approximate matching, with the mismatch absorbed by the error vector. Representation coordinates are still checked after each merge. Our filters act on the representation coordinates themselves with exact modular matching, which is Ozerov's consistency mechanism, not Both–May's.
- **Verdict.** The specific observation, that type-class (consistency) filters on the BBSS tree make depth 4–6 pay and give 0.2744 → 0.2726, appears to be new. The decoding observation (BM17b) should be cited as the nearest precedent.

## 3. Status check of Esser–May 0.255

- arXiv 1907.04295 v2 (21 Oct 2019) is **withdrawn**, with the comment "Issue with counting duplicate representations".
- v1 claimed 0.255 with a search tree of depth ≥ 13, by sampling lists. I found no corrected follow-up.
- The decoding claim in the same paper (BJMM half distance 0.048 → 0.042) falls with it.
- **Why the flaw doesn't apply to us:**
  - We never sample or modify list contents. Every list is the complete set of (or a BBSS random subset of) vectors with the node's exact type and residue.
  - Representation counts are BBSS's ρ_j = H(σ_j) − H(δ_{j−1}).
  - Duplicates are irrelevant, because outputs are de-duplicated sets of exact-type parents.
  - Our survival recursion (handoff2 A) and symmetry lemma make the counting explicit.

## 4. The Li 0.24 claim (Information 16 (2025) 887)

**Construction.** A depth-3 "ternary representation" tree: each node is the sum of **three** children, with digit splits 1 → (1,0,0)-type patterns and ε-parameters, and modular constraints r_j = ½ log R_j (Sec. 3.1, pp. 12–14).

**Cost model.** The time is taken as max(ℓ₃, 2ℓ₃ − r₂, 3ℓ₂ − (r₁ − r₂), 3ℓ₁ − (1 − r₁)). That is, a 3-way merge is charged at its **output** size |L|³/M.

**Where it breaks.** A 3-list merge under a modular constraint must enumerate at least the pairs from two of the lists (2ℓ) and look up the third. Charging each 3-way merge max(2ℓ, 3ℓ − new bits):
- At the paper's own parameters the cost is 0.4439, not 0.2403 (we reproduce the paper's 0.2403 under its own model). Level 2 gives 0.4294 against a claimed 0.2402.
- Re-optimising under honest costing gives **0.393** (`ter_honest.py`; Web Claude independently got 0.3929).
- The paper's "rigorous" §3.2 bounds list sizes only.

So the break is in the merge cost model, before any question of BBSS heuristics or survival accounting arises. Under our survival recursion the tree would also need its r = ½ log R choices checked, but that is moot.

**Precedent.** Nick decided (Oct) to mention Li only neutrally: "we were not able to reproduce an exponent below 0.39 under the usual cost model". Whether to include even that is item 7(c) of handoff5, Nick's call.

## 5. Lattice side (for the block-hybrid remark)

- **No density-1 lattice-plus-guessing exponent found.** The nearest work:
  - Ducas–Laarhoven–van Woerden, PKC 2020 / ePrint 2020/120, Heuristic claim 4: a batch of 2^{0.058d} CVP instances costs 2^{0.292d} time and 2^{0.208d} memory.
  - Bernstein's LWE hybrid, made practical by Karenin–Kirshanova–May–Nowakowski, ASIACRYPT 2025 / ePrint 2025/1910.
  - Doulgerakis–Laarhoven–de Weger, ePrint 2020/487 (SVP via CVPP).
- The subset-sum lattice literature is about density thresholds (Lagarias–Odlyzko, CJLOSS 0.9408) and LLL-count improvements (Joux–Węgrzycki, arXiv 2408.16108). Neither gives an exponential-time density-1 exponent.
- `\todo{check ref}`: Bernstein's original hybrid-attack reference (I haven't pinned down the exact paper).

## Sources read for this note

- Local PDFs: Both–May (ePrint 2017/1139), Li (Information 16, 887), Kirshanova–May (2021/1255).
- Downloaded: BBSS (arXiv 2002.05276), Ozerov's thesis (d-nb.info/1089007094/34), DLvW (ePrint 2020/120, author PDF).
- From arXiv abstract pages: arXiv 1907.04295 (withdrawal comment), arXiv 2608.07309, arXiv 2604.04656, arXiv 2408.16108.
- Snippet only: Esser ePrint 2022/1328; Esser–Bellini ePrint 2021/1243.
