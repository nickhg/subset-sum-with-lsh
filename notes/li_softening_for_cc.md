# Handoff for cc: soften the Li [Li25] material (Nick's decision)

Nick wants to mention Li's claim neutrally, without calling it false. Please make the following changes to `draft.tex`.

## 1. Related work: replace the whole Li paragraph and its footnote
Replace the paragraph that begins "Li~\cite{Li25} claims a classical exponent of $0.2400$..." (including its footnote and its `\status` line) with:

> We do not compare with~\cite{Li25}, which reports $2^{0.24n}$ using ternary trees. Its cost model charges each three-list merge at the size of its output; under the usual cost model, which enumerates pairs from two of the lists, we were not able to reproduce an exponent below $0.39$.

`\status{numerical; script ter_honest.py (not included in the paper)}`

## 2. Remove the appendix
Delete `\appendix` and the section "Honest costing of the ternary tree of [Li25]". If no other appendix remains, delete the `\appendix` command too. Check that nothing still references `app:li`.

## 3. Abstract and framing text
- If the abstract (or the new framing abstract from `framing_for_cc.md`) contains a sentence about Li, remove it. The abstract should not mention Li.
- If the optional state-of-play table from `framing_for_cc.md` is used, **drop the Li row**.
- Anywhere the text says "best known" or "best classical exponent", make sure the claim is about BBSS (e.g. "improves on the $0.2830$ of~\cite{BBSS20}"). Do not claim a record. The existing intro sentence "This gives $\Ot(2^{0.283n})$, the best classical exponent we know of" may stay as it is, since with Li handled neutrally above it reads as honest.

## 4. Keep
- The `Li25` bib entry. It is still cited.
- Everything else, including the other related-work paragraphs, the ladder table and the HGJ 0.311 paragraph.

## 5. Check
- Build twice and make sure there are no undefined references.
- Grep for `Li25`. It should appear only in the new related-work sentence and in the bibliography.
