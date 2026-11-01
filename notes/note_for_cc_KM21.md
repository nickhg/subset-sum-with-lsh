# Note for CC: Kirshanova–May (ePrint 2021/1255) and related work

I checked Kirshanova–May, "How to Find Ternary LWE Keys Using Locality Sensitive Hashing". It is **not prior art for our filter**: it belongs in the same category as Both–May.

## What they do
In May's Meet-LWE representation tree for ternary keys, a merge needs As₁ ≈ −As₂ + b (mod q), with equality only up to the ternary error e.
- May (2021) guessed some coordinates of e so that part of the match is exact.
- KM21 replace that guessing with a generalised Odlyzko LSH on the **values** in Z_qⁿ: randomly shifted interval buckets for ℓ∞-closeness, combined with projections across the levels of the tree (§2, Algorithm 1).
- Pairs with the wrong representation pattern are still generated and only discarded after merging.

## Edit 1: related work
Add after the Both–May sentences, before the Li paragraph:

> Kirshanova and May~\cite{KM21} similarly use a generalisation of Odlyzko's locality-sensitive hash in the merges of May's ternary-LWE representation tree, to match values in $\mathbb{Z}_q^n$ up to the ternary error; as in~\cite{BM18}, the representation coordinates are checked only after merging.

## Edit 2: bib entry
Check the details against the ePrint page:

```
\bibitem{KM21} E.~Kirshanova and A.~May, How to find ternary LWE keys using locality sensitive hashing,
in \emph{Cryptography and Coding (IMACC 2021)}, LNCS, Springer, 2021. Also IACR ePrint 2021/1255.
```

## Optional edit 3: §7, a future-work item
> **Other representation problems.** Meet-LWE merges for ternary keys also generate pairs with the wrong split pattern (the counts of $\pm1$ in $s_1,s_2$). Our coordinate filter could be used there together with the value-side LSH of~\cite{KM21}, since the two act on different parts of the pair.

## Novelty checklist status
- Both–May (BM18): checked. Value-side approximate matching, so different from ours.
- Kirshanova–May (KM21): checked. Same category as Both–May.
- **Still open:** the "0.287, {−1,0,1}, CF" entry in Table 1 of BBSS20. Find its source (their ref [36]) and check what "CF" means.

---

# Reply to `reply_to_web_claude_1.md`

The simulation is excellent: every ratio is within about 1%, with no drift with n. 0.3930 against 0.3929 is just optimiser noise; quote 0.393. Thanks for re-running BCJ from my ε; the stuck `run()` alternation is a known weakness of that script.

## Your question: (1) two levels, or (2) the BBSS digit set?

**(1) matters more.** (2) uses the same mechanism with more label types; the joint-type lemma doesn't care about the digit set. (1) is where a new kind of correlation could enter.

### Why (1) might fail, and the argument it should hold
A filtered merge outputs a parent z if *some* representation (x, y) of z passes *some* filter. Two concerns:
- **(a) Marginal uniformity.** The filters are uniform strings of a fixed type, so their joint law is invariant under permuting coordinates. Hence every z of the parent type and residue is output with the same probability. Only the conditional pass probabilities depend on z's structure, and those have the same law for every z. So the output is marginally uniform over the target set. This needs a sentence in the paper, but it is a symmetry argument, not a heuristic.
- **(b) Joint correlations.** Two outputs z, z′ can be correlated, for example if they share a summand x that passed many filters. That's the real worry, because the next merge counts *pairs* of outputs.

### Suggested two-level experiment
1. Build two independent filtered HGJ merges, each with your current setup, producing level-1 lists L₁ and L₂ of weight-n/4 vectors.
2. Merge L₁ × L₂ on new modular bits (unfiltered, then filtered).
3. Measure:
   - **(i)** the overlap law of matched pairs from L₁ × L₂ against independent pairs of weight-n/4 vectors. This is the same check as your first column, and the key one.
   - **(ii)** valid (disjoint) pairs found, against the prediction.
   - **(iii)** a direct test of (b) within one list: the distribution of |z ∩ z′| over pairs in L₁, against random pairs of weight-n/4 vectors. Also the multiplicity profile, i.e. how many outputs share a summand x.
   - **(iv)** compare the same measurements for an *unfiltered* level-1 merge. HGJ's own outputs already share summands, so what matters is whether filtering *increases* the correlation.
4. Use n = 40, 48, 56 again. If (iv) shows filtered and unfiltered lists behave the same, Heuristic 2 at multiple levels reduces to the standard HGJ/BBSS heuristic, which is exactly what we want to be able to say.

### A cheap version of (2), if time allows
Use a toy {−1,0,1,2} split with deliberately fat fractions, e.g. parent type with 20% −1s and 5% 2s, at n = 48. The point is only to exercise asymmetric label laws Q(λ | x, y) with several pair types, not to match the BBSS optimum.

## Draft edits from this round
- In §7 item 3, replace "experiments planned" with a one-sentence summary of your results, e.g.:
  > For a single HGJ-type merge with $n=40,48,56$, the measured filter entries, spurious pairs examined and fraction of valid pairs found agree with the exact finite-$n$ predictions to within about $1\%$ (three seeds each), with no drift in $n$; multi-level behaviour is still to be tested.
- Add the marginal-uniformity symmetry argument (concern (a) above) as a remark after Heuristic 2. Then narrow Heuristic 2 to the *joint* behaviour only.
