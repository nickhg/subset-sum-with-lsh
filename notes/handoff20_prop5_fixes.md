# wc → cc: handoff20 (two fixes in the Proposition 5 proof)

1. **Exponent typo.** The displayed Hoeffding bound reads e^{−2(1−o(1)) log n}. With s ≍ √n and ε_n = n^{−1/4} log n we get s ε_n² = (1+o(1)) log² n, so it should read
   2 e^{−2 s ε_n²} = e^{−2(1−o(1)) log² n} = n^{−Θ(log n)}.
   (The stated conclusion is already correct; only the displayed exponent is missing the square.)

2. **Pattern families: weaken the claim and give the counting.** Replace "a vector enters only the family of its own pattern" with:
   - A vector determines only its own sequence of block types (its marginal pattern), not the joint pattern of a pair. It enters the filters of **every** family whose block marginals on its side equal its own sequence, and **no others**. In particular, vectors with atypical block types enter no family at all, since families are built only for near-typical joint patterns.
   - There are at most 2^{O(√n log n)} = 2^{o(n)} families in total, so the entry and decoding costs of a vector, summed over all families compatible with it, exceed the single-family cost by at most a factor of 2^{o(n)}. The passing-pair cost is counted per family, with the same factor.
   - The valid planted pair has a near-typical joint pattern with probability 1 − o(1) (item 1), so it is found in the family of its pattern.
   Keep the conclusion: every cost of Proposition 3 is achieved up to 2^{o(n)}.

Rebuild the PDF after this. (Nick's sending the a56b65b PDF to Alex. These fixes go into the ePrint version.)
