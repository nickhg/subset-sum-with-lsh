# Handoff for draft.tex — results from 31 Oct (chat session)

Please apply the changes below to `draft.tex`. Each item gives where it goes, what to add, and where the numbers come from. Keep the house conventions: put `\status{...}` annotations on every new claim, and leave the existing TODOs in place.

All exponents are log2(time)/n and rest on the same heuristics as the rest of the draft. The scripts listed at the end reproduce every number.

---

## 1. Related work: refute Li's 2^{0.2400n} claim

**Where:** at the end of the "Related work" paragraph in the Introduction, after the EM19 TODO.

**Content (suggested text):**

> Li~\cite{Li25} claims $\Ot(2^{0.2400n})$ with a ternary tree, in which each vector is written as a sum of three. Each three-list merge there is costed at the size of its output, $L^3/M$ (\cite[pp.~13--14]{Li25}). Finding all triples from three lists that satisfy one modular constraint requires enumerating pairs from two of the lists, at cost $L^2$, and no generic method does substantially better. With the published parameters the two upper merges then cost $2^{0.429n}$ and $2^{0.444n}$. Re-optimising the same ternary tree with merge cost $\max(2L,\,3L-\text{new bits})$ gives at best $2^{0.3929n}$ (Appendix~\ref{app:li}).

`\status{numerical; script ter_honest.py}`

**Evidence (for the record, not for the paper):**
- In Li's paper, eq. (2) on p. 12 defines the 3-way merge, and the objective on p. 13 is `max(l3, 2l3 - r2, 3l2 - (r1-r2), 3l1 - (1-r1))`. Page 14 says the time is "determined by the merged list size".
- The paper describes no algorithm for the 3-list merge. The only sorting it mentions is in the quantum section, for the level-3 lists.
- The 0.2400 comes out exactly as 3·0.2147 − 0.4039 and as 3·0.2221 − 0.4263, i.e. it is the output size.

**New appendix (`\appendix`, before the Acknowledgements):** "Honest costing of the ternary tree of [Li25]"
- We use Li's model unchanged:
  - l1 = H(1/6+w1, w1) − r1
  - l2 = H(1/18+w2, w2) − r2
  - l3 = H(1/18+w2, w2)/2
  - R(1) and R(2) as in Li's paper
  - r_i = ½·log R(i)
- Our reimplementation reproduces their figure: **0.2403** at the published rounded parameters (ε0=0.0066, ε1=0.0024, E0=0.0004, E1=0.0001, E−1=0) and **0.2399** after re-optimising.
- Adding the pair-enumeration terms 2·l2 and 2·l1:
  - **0.4439** at their parameters;
  - **0.3929** after re-optimising all five ε's;
  - **0.3927** if we also allow r_i < ½·log R(i).

**Bib entry:**
`\bibitem{Li25} Y.~Li, From subset-sum to decoding: improved classical and quantum algorithms via ternary representation technique, \emph{Information} \textbf{16} (2025), no.~10, 887.`
(Please check the format; the DOI is 10.3390/info16100887.)

---

## 2. New section "Other trees and digit sets" (before "What remains to be done")

### 2a. Table of filtered vs unfiltered exponents

| tree | no filters | with filters | digit set | accounting |
|---|---|---|---|---|
| HGJ, depth 2–3 | 0.3371 | 0.3269 | {0,1} | strict (every element keeps a surviving representation) |
| BCJ, depth 3 | 0.2909 | 0.2864 | {−1,0,1} | strict |
| BBSS, depth 3 | 0.2829 | 0.2793 | {−1,0,1,2} | BBSS (Heuristic 1) |
| BBSS, depth 3 | 0.2827 | 0.2792 | {−2,…,2} | BBSS |

The paper must state that the HGJ and BCJ rows use the stricter HGJ/BCJ accounting, not Heuristic 1. Each "no filters" figure matches the published exponent for that tree, which serves as a check of the model.

Further detail:
- **BCJ:** at BCJ's own ε values the filter gains nothing, because list sizes bind. The gain appears only when ε is re-optimised together with the filter. The optimum is at ε ≈ (0.0274, 0.0203, 0.0053), with the filter doing its work at the level-2 merge (0.3017 → 0.2864).
- **HGJ:** extra depth gives no gain beyond 2. The filtered optimum is 0.32693 from the closed form, and 0.32694 from an independent simulation (iterative proportional fitting) that maximises over all overlap sizes.

### 2b. Paragraph: HGJ and the exponent 0.311

- In HGJ the binding cost is the level-2 merge: lists of 2^{0.2936n} weight-n/8 vectors, 2^{0.3371n} matching pairs, of which 2^{0.3113n} are disjoint. So only a fraction 2^{−0.0259n} of matching pairs are useful.
- A perfect filter (pay only for disjoint pairs) gives exactly **0.3113**, which is the exponent originally stated in HGJ10. The 0.311 → 0.337 correction is precisely this overlap waste.
- Type-class filters recover part of it: 0.3269.
- **Heuristic argument (not a proof) that 0.3113 is unreachable with filters.** Waste ≤ useful and entries within budget would together require, per filter, left and right families of n/8-sets, each of density ≥ 2^{−0.0436n}, in which almost all cross pairs are disjoint.
  - For spread families, the overlap concentrates around Σᵢ αᵢβᵢ·n. Making that o(n) forces near-partitioned supports, which caps the density at about 2^{−0.138n}.
  - An entropy/Shearer argument gives only the trivial bound, so a real proof needs a robust cross-disjointness (supersaturation) lemma.
  - Mark this `\status{heuristic argument, not a proof}`.
- **TODO(Nick):** citation for the 0.311 → 0.337 correction.

### 2c. Paragraph: larger digit sets

- With digit set {−2,…,2}, the additional splits are −2 → (0,−2),(−1,−1); −1 → (1,−2); and 0 → (2,−2).
- The optimiser puts mass below 10⁻⁴ on −2 at every level, with and without filters.
  - Without filters: 0.2827 (vs 0.2829).
  - With filters: 0.27921 (vs 0.27924 for {−1,0,1,2}).
- This held both when warm-starting from the {−1,0,1,2} optimum and when starting with −2 forced on (that run went from 0.48 back to 0.2793).
- Conclusion: at depth 3, −2 creates more waste than representations, and the filters don't change this. Depth 4 is untested.

`\status{numerical; warm-started from the {-1,0,1,2} optimum and from a point with -2 forced on}`

---

## 3. Checks on the existing text (no change needed, for your information)

- Proposition 2's "pairs examined" term, P + I(XY;Λ) − I(X;Λ) − I(Y;Λ), agrees exactly with the chat model's closed form when π = Q_Λ. The chat derivation solved the worst case over pair types as a max-entropy problem: x ⟂ y given λ.
- Lemma 1(3) is correct as written. Because type-class filters fix the label type, a fixed u gives exact independence.
- The restart values 0.27927, 0.27940 and 0.27969 are consistent with the chat runs (best 0.27921–0.27924).

---

## 4. Open items (add to Section 7 or keep as TODOs)

1. **Novelty.** BBSS's Table 1 lists a "0.287 {−1,0,1} RAM CF [36]" entry. Identify ref [36] and check that it isn't already merge filtering. Also search post-2020 work for near-neighbour or LSF merges in representation trees.
2. **Table 2 regeneration.** Regenerate it from a single saved optimum. The existing TODO about the BBSS leaf value 0.2738 still applies.
3. **Depth 4** with filters, including the ±2 digit set.

---

## Scripts (attached; Python 3 + numpy + scipy)

- `ter_honest.py`: the Li re-costing (section 1 and the appendix). Run it with `python3 ter_honest.py`.
- `gen_lsf.py`: generic digit-set tree with BBSS accounting and type-class LSF (closed-form worst case).
- `gen_opt.py`: optimiser.
  - Usage: `gen_opt.py DIGITS depth seed p|f [init.npy]`, e.g. `gen_opt.py -2,-1,0,1,2 3 7 f init5_f.npy`.
  - It runs slowly with 2 cores; run one or two processes at a time.
- `embed.py`: embeds a {−1,0,1,2} optimum into the {−2,…,2} parametrisation, with −2 switched off and filters copied type by type.
- `bcj_lsf.py`: BCJ/HGJ with filters under strict accounting (the HGJ and BCJ rows of table 2a).
- `gen_mm5_3_f_21.npy`: best {−2,…,2} filtered point (T = 0.27921).
