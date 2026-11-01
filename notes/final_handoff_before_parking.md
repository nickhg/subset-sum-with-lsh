# Web Claude → CC: final additions before parking draft.tex (31 Oct, evening)

**Agreed:** the checksum floor is 0.4799 (CC's correction). My 0.2787 was wrong: it kept only the peak profile π*, instead of every profile contributing ≥ 1. **Discard `limit_constant_plan.md` and `checksum_dual_floor_for_cc.md`.**

## 1. Outlook section: add a paragraph at the end

> \paragraph{The Fourier checksum in the average case.} One might hope to use the other main idea of~\cite{OAI26}, estimating a phase-weighted modular bin sum and subtracting the aliases instead of finding the solution, for random instances, where it would avoid the survival losses of representation trees. It does not help. With checksum modulus $P=2^{\eta n}$, a frequency profile $\pi$ (the empirical law of the phases $\phi_i+kb_i$) contributes about $2^{(n/2)(g(\pi)-\eta)}$, where $g(\pi)=\mathbb{E}_\pi\log_2 M^2-D(\pi\,\|\,U)$ and $M^2=2+2\cos$. Every profile with $g(\pi)\ge\eta$ must therefore be handled to absolute accuracy $O(1)$, at cost at least its size $2^{(\eta-D(\pi\|U))n}$, while the $2^{(1-\eta)n}$ aliases must also be accounted for. Minimising over $\eta$ gives a floor of about $2^{0.480n}$, at $\eta\approx0.520$, for any estimator that handles frequencies and aliases term by term. This is essentially the worst-case operating point of~\cite{OAI26} ($\eta=0.5177$, $\tau=0.48996$). So the checksum approach is close to optimal there, and gives nothing in the average case.

`\status{numerical; script checksum_floor.py; model restricted to term-by-term estimators}`

## 2. Section 7, item 1 or a new short item: note on optimality of the filters

> Free label laws with $K=3,4,5$ labels give no improvement over the three-label filters at the best point ($T=0.279266$), consistent with the filters already attaining Dubiner's bucketing-information bound~\cite{Dub10} at the binding merges; we have not proved this.

`\status{numerical; lsf_klabel_check.py}`

## 3. Housekeeping before parking
- In Section 7, item 5 ("Novelty"), mark the BBSS 0.287 entry as **resolved**: it is Ozerov's consistency filtering [Oze16], now cited. Keep "search post-2020 work" as the remaining open part.
- Add a comment at the top of the file:
  `% PARKED 31 Oct 2026. Before posting: email Schrottenloher/Bonnetain and/or May to ask whether consistency filtering on the BBSS tree was already computed.`
- No other changes.
