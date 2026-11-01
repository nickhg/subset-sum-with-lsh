# Web Claude → CC: review of draft.tex (the "A note on filtered merges…" version)

The draft reads well, and the framing is right. Below: one important novelty lead, then small fixes.

## A. Novelty: the "CF" entry in BBSS's Table 1 (IMPORTANT, do before posting)
- The caption of BBSS's Table 1 defines **CF = "constraint filtering"**, with the note "not studied in this paper".
- The row is: 0.287, {−1,0,1}, RAM, CF. In the arXiv version (2002.05276v4) the reference is **[38]**, not [36].
- The body text never discusses it, and I couldn't get the reference list through my fetch tool.
- **Please fetch the bibliography** from the arXiv TeX source or the ASIACRYPT PDF, identify [38], and read it.

"Constraint filtering" could be close to what we do, or it could be something different: for example, discarding list elements whose partial sums violate constraints, or a corrected Esser–May. We need to know which before posting. Depending on what it is, the related-work section will need either a sentence like "[38] filters by …; our filter differs in …", or a reframing.

## B. Small fixes to the draft
1. **Abstract, first sentence.** "gives the first worst-case Subset Sum algorithm with exponent below 1/2" states OpenAI's result as fact, while the table and §1 say "not yet independently verified". For consistency, use "reports the first worst-case…" or "claims…".
2. **Remark after Heuristic 2 (marginal uniformity).** Tighten the wording: the uniformity holds over the random instance as well as the filters. Suggested replacement for the middle sentence:
   > Hence, over a random instance and random filters, the probability that a given vector of the parent type is output, conditioned on it satisfying the parent constraint, does not depend on the vector, and the filtered output list is marginally uniform over that set, as in the unfiltered merge.
3. **§7 item 2.** There are still two `\status` lines in a row (`numerical check`, then `open`). Merge them into one.
4. **Theorem 1 says "time and memory".** Memory hasn't been computed separately. Either (a) add a sentence that filters are processed one at a time, so memory is the maximum list size plus one filter's entries (≈ 2^{0.2793n}), or (b) drop "and memory".
5. **Bib entry [OAI26].** Add the URL so readers can find it: `https://github.com/openai/math` (preprint directory `preprints/Subset-Sum-in-Time-2-power-0-49n-October-4-2026/`).
6. **Acknowledgements.** The second clause repeats the first. Suggested single sentence:
   > Since this note is prompted by AI-generated results, we say plainly that the numerical experiments and much of the drafting were done with Anthropic's Claude; all results and text were checked by the author, who takes full responsibility for the content.
7. **Date line.** Update it to the posting date.
8. **Table 2 TODO** (the BBSS leaf value 0.2738). Still open; regenerate from the saved optimum.

## C. Nothing else to change
The Li sentence, the related-work paragraphs, the state-of-play table and the Outlook are all fine as they are.
