# wc → cc: handoff7 (Nick's decision on item 6)

Nick's decision: **remove every mention of OpenAI / [OAI26] from the paper.** It isn't relevant to the result.

- Delete the sentence "We came to these filters through the asymmetric filtering of frequency pairs in the recent worst-case algorithm of~\cite{OAI26}."
- Delete the \bibitem{OAI26} entry, and check that nothing else cites it (grep for OAI26).

Framing note from Nick: the gap is that BBSS didn't combine their tree with consistency filtering, which predates any recent work. Keep that diplomatic. The existing wording is about the right tone: BBSS list consistency filtering as "not studied" [Table 1], and Ozerov leaves ±2 open. No need to add anything sharper.
