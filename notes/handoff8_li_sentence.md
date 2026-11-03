# wc → cc: handoff8 (Nick's decision on item 5, Li's 0.24 claim)

Nick's decision: include a **short, neutral** statement in the related work that we could not reproduce Li's claim. No extended critique.

- Use one or two sentences, e.g.: "Li~\cite{Li25} claims $2^{0.24n}$ using a ternary-tree representation structure; we were not able to reproduce this exponent within the heuristics used here." If the literature search pinned down a specific step that fails, you may add a single clause naming it (e.g. "…; in our accounting the representation count at [level/step] does not support the stated list sizes"), but only if it is verified.
- **Accuracy condition:** only say "not able to reproduce" if we actually attempted it, i.e. re-derived the construction's exponents in our model. If we haven't, use "we have not been able to verify this claim" instead. Please say in your reply which of the two applies, and what was checked.
- Replace the current optional Li paragraph with this sentence, and make it unconditional (no \ifincludeLi switch). Keep \cite{Li25}.
- Please send wc the Li section of paper/litsearch.md, so the wording can be checked against it.

(Reminder: handoff7 removes the OAI26 sentence and reference entirely.)
