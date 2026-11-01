# Framing change for draft.tex: a short "state of play" note (from Web Claude, for Nick's approval)

Nick wants the paper framed modestly. It should be an ePrint note recording where Subset Sum stands after the OpenAI preprints, written quickly and expected to be superseded, not a paper that claims longevity. Below are suggested replacements; Nick should adjust the wording to his own voice.

## 1. Title (pick one)
- *Subset Sum after the OpenAI preprints: filtering the merges*
- *A note on filtered merges for random Subset Sum*
- *Where the OpenAI Subset Sum results leave the average case: a short note*

## 2. Abstract (replacement)

> The OpenAI preprint [OAI26] gives the first worst-case Subset Sum algorithm with exponent below $1/2$. One of its ingredients, an asymmetric locality-sensitive filter that keeps only the pairs worth examining, also applies to the average-case representation algorithms of Howgrave-Graham–Joux, Becker–Coron–Joux and Bonnetain–Bricout–Schrottenloher–Shen. At each merge we filter candidate pairs by their coordinate-wise joint type with a random label string. The filter helps exactly when $I(X;\Lambda)+I(Y;\Lambda)>I(XY;\Lambda)$. Under the usual heuristics this lowers the best known exponent for random Subset Sum from $0.2829$ to $0.2793$, and it gives smaller gains for HGJ and BCJ. We also note that a recent claim of $2^{0.2400n}$ [Li25] does not hold once its three-list merges are costed correctly. This is a short note recording where things stand; we expect it to be improved on soon.

## 3. New opening paragraph of the Introduction (before the current first paragraph)

> This note was written quickly after the appearance of~\cite{OAI26}, to record how one of its ideas carries over to the average case. The gain is small and we expect it to be improved on, by deeper trees, better filters, or ideas we have not thought of. We post it now because the filter seems to be the useful part, and others may take it further.

## 4. A short "state of play" table (end of the Introduction, optional)

| setting | before | now | source |
|---|---|---|---|
| worst case | $2^{n/2}/\mathrm{poly}(n)$ [CJRS23] | $2^{0.49n}$ | [OAI26], not yet independently verified |
| random, density 1 | $2^{0.2830n}$ [BBSS20] | $2^{0.2793n}$ | this note, heuristic |
| random, claimed | $2^{0.2400n}$ [Li25] | does not hold | §1 and Appendix A |

Two things to check before including it:
- **[CJRS23] needs a bib entry.** X. Chen, Y. Jin, T. Randolph and R. A. Servedio, "Subset Sum in time $2^{n/2}/\mathrm{poly}(n)$", APPROX/RANDOM 2023, LIPIcs 275, 39:1–39:18.
- **The "not yet independently verified" wording for [OAI26].** Nick may prefer to drop it, or to say "AI-generated, no Lean formalisation". The repo's own README describes the manuscripts as raw research data at various stages of verification.

## 5. Conclusion: a short closing section (replace or precede "What remains to be done")

> **Outlook.** The filter is cheap to add to any representation merge, and the criterion $I(X;\Lambda)+I(Y;\Lambda)>I(XY;\Lambda)$ says when it is worth it. In Subset Sum the gains shrink as the digit set grows ($0.010$ for HGJ, $0.0045$ for BCJ, $0.0036$ for BBSS), which suggests that larger digit sets and filters attack the same waste. Representation trees in decoding and in ternary-LWE key search have richer digit patterns, and the gain may be larger there.

## 6. Tone throughout
- Replace "we establish", "we prove" and similar with "we observe", "we find numerically".
- Keep the heuristic and status caveats visible. The work is honest about being numerical, and that's a strength in a note like this.
- The theorem can stay, labelled "heuristic" as now.
- Keep the acknowledgement about AI tools. Since the note is explicitly *about* AI-generated results, it's worth a line saying that the experiments and much of the drafting were done with Claude, and that the author checked them.

## 7. Things NOT to change
- Keep the Li refutation and appendix, the ladder table, the HGJ 0.311 paragraph, and the related-work paragraphs (Both–May, Kirshanova–May, Esser–May) as they are.
