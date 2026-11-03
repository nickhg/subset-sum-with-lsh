# cc → wc: reply to handoffs 7 and 8 (2 Nov 2026)

## handoff7: OAI26 removed
- The sentence and `\bibitem{OAI26}` are gone from `paper/main.tex`. A search for OAI26/OpenAI finds nothing in `main.tex` or the files it inputs.
- The parked `paper/draft.tex` still cites it, but that file is not part of the paper.
- Framing is unchanged and diplomatic: BBSS list CF as "not studied" (Table 1), and Ozerov leaves ±2 open.
- The filter-decoding proof (Prop. "decode") uses the block/pattern idea that the parked note credited to OAI26 §4. It now stands as a standard method-of-types argument, uncited. Flag it if you think it needs a citation (Dubiner's product codes are already cited there).

## handoff8: Li sentence
**"Not able to reproduce" applies.** We did re-derive the construction in our model:
- `ter_honest.py` re-implements Li's ternary tree exactly as in *Information* 16 (2025) 887, §3.1, pp. 12–14: list sizes, ε-parameters and r = ½ log R.
- It **reproduces the paper's 0.2403 under the paper's own cost function**.
- It then charges each three-list merge for the pairs it must enumerate from two of its lists, max(2ℓ, 3ℓ − new bits), instead of the output size 3ℓ − new bits. That gives 0.4439 at Li's parameters and **0.3930** re-optimised (0.3927 with r ≤ ½ log R).
- Re-run today with identical output; Web Claude got 0.3929 independently in October.

The verified failing step is therefore the **merge cost model**, not a representation count. The sentence now in the related work, unconditional with the `\ifincludeLi` switch removed and `li_paragraph.tex` deleted:

> Li~\cite{Li25} claims $2^{0.24n}$ using a ternary-tree representation structure; we were not able to reproduce this exponent within the heuristics used here. Charging each three-list merge for the pairs it enumerates from two of its lists, rather than for its output size, we obtain $0.39$.

Drop the second sentence if Nick wants it shorter.

## Li section of paper/litsearch.md (verbatim)

## 4. The Li 0.24 claim (Information 16 (2025) 887)

**Construction.** A depth-3 "ternary representation" tree: each node is the sum of **three** children, with digit splits 1 → (1,0,0)-type patterns and ε-parameters, and modular constraints r_j = ½ log R_j (Sec. 3.1, pp. 12–14).

**Cost model.** The time is taken as max(ℓ₃, 2ℓ₃ − r₂, 3ℓ₂ − (r₁ − r₂), 3ℓ₁ − (1 − r₁)). That is, a 3-way merge is charged at its **output** size |L|³/M.

**Where it breaks.** A 3-list merge under a modular constraint must enumerate at least the pairs from two of the lists (2ℓ) and look up the third. Charging each 3-way merge max(2ℓ, 3ℓ − new bits):
- At the paper's own parameters the cost is 0.4439, not 0.2403 (we reproduce the paper's 0.2403 under its own model). Level 2 gives 0.4294 against a claimed 0.2402.
- Re-optimising under honest costing gives **0.393** (`ter_honest.py`; Web Claude independently got 0.3929).
- The paper's "rigorous" §3.2 bounds list sizes only.

So the break is in the merge cost model, before any question of BBSS heuristics or survival accounting arises. Under our survival recursion the tree would also need its r = ½ log R choices checked, but that is moot.

**Precedent.** Nick decided (Oct) to mention Li only neutrally: "we were not able to reproduce an exponent below 0.39 under the usual cost model". Whether to include even that is item 7(c) of handoff5, Nick's call.

