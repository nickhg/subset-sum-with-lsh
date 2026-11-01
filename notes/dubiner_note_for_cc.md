# Web Claude → CC: Dubiner 2010 (arXiv 0810.4182), how it relates to our filter, and an optimality check

## The correspondence (I've read the paper)
Dubiner's data model (Def. 3.1) is our merge setting:
- two sets of i.i.d. vectors with marginals P_{·*} and P_{*·};
- one special pair with joint law P per coordinate. In our case P = σ_j, and there are many special pairs; per pair it is the same thing.

His **bucketing codes** (Def. 5.1) are data-independent pairs of subsets (B_{0,t}, B_{1,t}). Their work is

  W = Σ_t max(n0·p_{B0,t}, n1·p_{B1,t}, n0·p_{B0,t}·n1·p_{B1,t}),

i.e. our left entries, right entries and pairs examined.

- **Theorem 6.3 (achievability).** For any planted law Q, a random code gives success ≥ 1 − ε with n0 = N^{K(Q_x‖P_x)}, n1 = N^{K(Q_y‖P_y)} and W ≤ N^{ε+K(Q‖P)}. That is our type-class filter: per-side pass exponents and a filter count.
- **Definition 9.1 (bucketing information I(P, λ0, λ1, μ)).** This mixes planted laws R_i indexed by i. That index **is our label Λ**, and Dubiner shows at most b0·b1 indices are needed.
- **Theorem 10.1 (lower bound) and 10.2 (tightness).** These characterise the **optimal** trade-off over *all* data-independent bucketing codes, and random codes achieve it.

So our "type-class filters with labels" are Dubiner's random bucketing codes. Our criterion I(X;Λ) + I(Y;Λ) > I(XY;Λ) is the regime in which his codes beat the trivial code (he calls this sub-conjugacy, Def. 6.2). The note should say this plainly.

## Suggested text (related work, next to Ozerov)
> The type-class filters we use are the random bucketing codes of Dubiner~\cite{Dub10}, whose bucketing-information function characterises the optimal cost of any data-independent filter for a given joint law; the consistency algorithms of~\cite{Oze16} build on the same work. Our criterion $I(X;\Lambda)+I(Y;\Lambda)>I(XY;\Lambda)$ is the condition under which such a code beats exhaustive pairing at a merge.

Bib:
```
\bibitem{Dub10} M.~Dubiner, Bucketing coding and information theory for the statistical high-dimensional
nearest-neighbor problem, \emph{IEEE Trans.\ Inf.\ Theory} \textbf{56} (2010), no.~8, 4166--4179. arXiv:0810.4182.
```

## An optimality check worth running
Theorem 10.1 gives a **lower bound for every data-independent filter**. We can therefore test whether our label filters are already optimal at the binding merges (levels 1 and 2 of the 0.27927 point).

1. Our setting differs from Dubiner's in one respect: the pair term is restricted to residue-matching pairs. In exponents, the pair term is P_j + (pass exponents) instead of 2L_j + (pass exponents). That only shifts the cost of the third term; the code family is the same. So redo the bound with a cost triple of left entries, right entries and pair term scaled by 2^{−Δc·n}. The proof of Thm 10.1 goes through with that weight (it is a Hölder-type argument; check Appendix II).
2. Compute the resulting optimum for P = σ_j by maximising over (λ0, λ1, μ), using I(P, λ0, λ1, μ) from Def. 9.1 / Lemma 9.1. For μ ≤ 1 a single planted Q suffices, which makes it a small convex program.
3. Compare with our merge costs: 0.2793 at level 2 and 0.2698/0.2661 at level 1.
   - If they match, the note can say: *"at the binding merges our filters attain Dubiner's bound, so no data-independent filter can do better for this tree and these digit parameters."* That is a clean statement to include.
   - If Dubiner's bound is lower, there is a better filter to find.

Observation: in my runs, 3-label and 4-label filters gave the same optimum (0.32694 for HGJ), and the 4th label was unused. This suggests we are already at the bound, but it is not a proof.
