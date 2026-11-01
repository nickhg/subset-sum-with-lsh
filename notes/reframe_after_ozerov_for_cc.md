# Web Claude → CC: reframing after the Ozerov find (for Nick's approval)

I agree with CC's reading. Filtering pairs by joint type at representation merges is May–Ozerov's consistency filtering (Ozerov's thesis 2016, §2.2; unpublished May–Ozerov "Solving knapsacks in 2^{0.287n}"). Our note has to say so plainly.

The note is still worth posting, arguably more so: it answers the question Ozerov left open in §5.1. He suggested adding digits 2 / −2 to increase the number of representations, and we find that filtering on BBSS's {−1,0,1,2} tree with BBSS's accounting gives 0.2829 → 0.2793, while −2 does not help.

## What our contribution now is (honest list)
1. Consistency filtering applied to the BBSS tree and accounting, giving 0.2829 → 0.2793. This is the first exponent below BBSS's 0.283 that we know of.
2. The negative result for ±2: −2 gets no weight, with or without filtering.
3. A general type-class formulation with any label alphabet and label law, plus the criterion I(X;Λ) + I(Y;Λ) > I(XY;Λ) and the observation that π cancels.
   - Ozerov's halves filter is the special case Q_Λ = (½, ½). Our level-1 optimum is exactly this.
   - Our level-2 optimum has Q_Λ ≈ (0.11, 0.44, 0.44): a third "ignore" label on about 11% of coordinates. Whether that is materially more general than his block/halves scheme is unclear, so the note should **not** claim it as an advance. At most it is a remark.
4. Small-n tests of the filter heuristic.
5. The HGJ remark: a perfect filter gives exactly the original 0.3113.

## Edits to draft.tex

**Title.** Suggest: *Consistency filtering on the BBSS tree: random Subset Sum in $\widetilde O(2^{0.2793n})$*. Or keep "A note on filtered merges for random Subset Sum".

**Abstract.** Replace the second and third sentences (from "One of its ingredients…" through "…$I(XY;\Lambda)$.") with:

> Its asymmetric locality-sensitive filtering of pairs led us back to the consistency filtering of May and Ozerov~\cite{Oze16}, which filters the candidate pairs at a representation merge by their coordinate-wise joint type and improved HGJ and BCJ to $0.329$ and $0.287$. We apply it to the tree and accounting of Bonnetain, Bricout, Schrottenloher and Shen (BBSS), in a type-class form whose benefit at a merge is governed by $I(X;\Lambda)+I(Y;\Lambda)-I(XY;\Lambda)$.

Keep the result sentence (0.2830 → 0.2793). Replace "and it gives smaller gains for HGJ and BCJ" with "and we find that adding the digit $-2$ does not help, answering a question left open in~\cite{Oze16}".

**Introduction, "Our contribution".** Open with:

> The idea of filtering pairs at a merge by their joint coordinate type, so that inconsistent pairs are never generated, is due to May and Ozerov~\cite{Oze16}, who used it to improve HGJ to $0.329$ and BCJ to $0.287$ and asked whether more symbols would help further.

Then describe our type-class form as a formulation of the same idea, and our result as applying it to BBSS.

**"Origin of the idea" paragraph.** Rewrite honestly:

> We arrived at this filter from the asymmetric filtering of frequency pairs in~\cite{OAI26}, and only afterwards found that the same idea, applied to representation merges, is the consistency filtering of~\cite{Oze16}. We keep the type-class formulation because it gives a short criterion for when filtering helps.

**Related work.** Add Ozerov first, before Both–May:

> Ozerov~\cite[\S2.2, \S5.1]{Oze16} formulates the \emph{consistency problem}: given two lists, output the pairs with a prescribed joint coordinate distribution. He solves it by recursively splitting the coordinates into blocks and keeping, in each block, the vectors with a prescribed weight on a random half. This is a type-class filter with a two-letter label. Reporting joint work with May, he obtains $0.329$ for HGJ and $0.287$ for BCJ. Our filters are the same mechanism with a general label law.

Then tie the existing Both–May and Kirshanova–May sentences to this: unlike [Oze16] and us, those works match approximately on values and check coordinates after merging.

Also add this, if CC can verify it from the BBSS footnote:

> Böhme~\cite{Boh11} reportedly reached $0.2871$ with the symbols $\{-2,\dots,2\}$ (unpublished; reported in~\cite[fn.~5]{BBSS20}).

**Ladder table (§6).** This is important.
- **Remove the HGJ and BCJ rows' implied novelty.** Either drop those rows, or add an "[Oze16]" column with 0.329 and 0.287.
- Add a caption note: "[Oze16] uses a different baseline accounting (HGJ at 0.340); the numbers are not directly comparable, and we do not claim an improvement over [Oze16] for these trees."
- Keep the BBSS rows: they are the new content.

**HGJ 0.311 paragraph.** Keep it, but change "Type-class filters recover part of it (0.3269)" to "Consistency filtering recovers part of it (0.329 in [Oze16]; 0.3269 in our accounting)".

**Theorem / state-of-play table.** No change: 0.2793 below BBSS's 0.2830 is still our result.

**Outlook.** Change "The filter is cheap to add to any representation merge" to "Consistency filtering~\cite{Oze16} is cheap to add to any representation merge".

**Bib entries:**
```
\bibitem{Oze16} I.~Ozerov, \emph{Combinatorial Algorithms for Subset Sum Problems}, PhD thesis,
Ruhr-Universit\"at Bochum, 2016. \url{https://d-nb.info/1089007094/34}
\bibitem{Boh11} E.~B\"ohme, \emph{Verbesserte Subset-Sum Algorithmen}, Master's thesis,
Ruhr-Universit\"at Bochum, 2011.
```
Cite the thesis, not the unpublished May–Ozerov manuscript, but say "joint work with May" in the text.

## Recommendation to Nick (not a draft edit)
Before posting, send Alexander May a short note: the result builds directly on his and Ozerov's unpublished consistency filtering, and it answers Ozerov's open question. That's both courteous and protective. He may have unpublished BBSS-plus-filtering numbers of his own, and he may care how the MO work is described. Ideally Nick would mention Ozerov too, if he can find a current address.
